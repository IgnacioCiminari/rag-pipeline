import sys
import io
import re
import logging
from typing import BinaryIO, Any

from .._base_converter import DocumentConverter, DocumentConverterResult
from .._stream_info import StreamInfo
from .._exceptions import MissingDependencyException, MISSING_DEPENDENCY_MESSAGE

# Pattern for MasterFormat-style partial numbering (e.g., ".1", ".2", ".10")
PARTIAL_NUMBERING_PATTERN = re.compile(r"^\.\d+$")


def _merge_partial_numbering_lines(text: str) -> str:
    """
    Post-process extracted text to merge MasterFormat-style partial numbering
    with the following text line.

    MasterFormat documents use partial numbering like:
        .1  The intent of this Request for Proposal...
        .2  Available information relative to...

    Some PDF extractors split these into separate lines:
        .1
        The intent of this Request for Proposal...

    This function merges them back together.
    """
    lines = text.split("\n")
    result_lines: list[str] = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        # Check if this line is ONLY a partial numbering
        if PARTIAL_NUMBERING_PATTERN.match(stripped):
            # Look for the next non-empty line to merge with
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1

            if j < len(lines):
                # Merge the partial numbering with the next line
                next_line = lines[j].strip()
                result_lines.append(f"{stripped} {next_line}")
                i = j + 1  # Skip past the merged line
            else:
                # No next line to merge with, keep as is
                result_lines.append(line)
                i += 1
        else:
            result_lines.append(line)
            i += 1

    return "\n".join(result_lines)


# Load dependencies
_dependency_exc_info = None
try:
    import pdfminer
    import pdfminer.high_level
    import pdfplumber
except ImportError:
    _dependency_exc_info = sys.exc_info()


ACCEPTED_MIME_TYPE_PREFIXES = [
    "application/pdf",
    "application/x-pdf",
]

ACCEPTED_FILE_EXTENSIONS = [".pdf"]


def _to_markdown_table(table: list[list[str]], include_separator: bool = True) -> str:
    """Convert a 2D list (rows/columns) into a nicely aligned Markdown table.

    Args:
        table: 2D list of cell values
        include_separator: If True, include header separator row (standard markdown).
                          If False, output simple pipe-separated rows.
    """
    if not table:
        return ""

    # Normalize None → ""
    table = [[cell if cell is not None else "" for cell in row] for row in table]

    # Filter out empty rows
    table = [row for row in table if any(cell.strip() for cell in row)]

    if not table:
        return ""

    # Column widths
    col_widths = [max(len(str(cell)) for cell in col) for col in zip(*table)]

    def fmt_row(row: list[str]) -> str:
        return (
            "|"
            + "|".join(str(cell).ljust(width) for cell, width in zip(row, col_widths))
            + "|"
        )

    if include_separator:
        header, *rows = table
        md = [fmt_row(header)]
        md.append("|" + "|".join("-" * w for w in col_widths) + "|")
        for row in rows:
            md.append(fmt_row(row))
    else:
        md = [fmt_row(row) for row in table]

    return "\n".join(md)


def _extract_form_content_from_words(page: Any, font_stats: dict | None = None) -> str | None:
    """
    Extract form-style content from a PDF page by analyzing word positions.
    This handles borderless forms/tables where words are aligned in columns.

    Returns markdown with proper table formatting:
    - Tables have pipe-separated columns with header separator rows
    - Non-table content is rendered as plain text (with hierarchy if font_stats is provided)

    Returns None if the page doesn't appear to be a form-style document,
    indicating that pdfminer should be used instead for better text spacing.
    """
    logging.info(f"[NATIVE_TABLE] Iniciando _extract_form_content_from_words para la página actual.")
    words = page.extract_words(keep_blank_chars=True, x_tolerance=3, y_tolerance=3, extra_attrs=["size"])
    if not words:
        logging.info("[NATIVE_TABLE] No se extrajeron palabras en esta página.")
        return None
    logging.info(f"[NATIVE_TABLE] Se extrajeron {len(words)} palabras.")

    # Group words by their Y position (rows)
    y_tolerance = 5
    rows_by_y: dict[float, list[dict]] = {}
    for word in words:
        y_key = round(word["top"] / y_tolerance) * y_tolerance
        if y_key not in rows_by_y:
            rows_by_y[y_key] = []
        rows_by_y[y_key].append(word)

    # Sort rows by Y position
    sorted_y_keys = sorted(rows_by_y.keys())
    page_width = page.width if hasattr(page, "width") else 612

    # First pass: analyze each row
    row_info: list[dict] = []
    for y_key in sorted_y_keys:
        row_words = sorted(rows_by_y[y_key], key=lambda w: w["x0"])
        if not row_words:
            continue

        first_x0 = row_words[0]["x0"]
        last_x1 = row_words[-1]["x1"]
        line_width = last_x1 - first_x0
        combined_text = " ".join(w["text"] for w in row_words)

        # Count distinct x-position groups (columns)
        x_positions = [w["x0"] for w in row_words]
        x_groups: list[float] = []
        for x in sorted(x_positions):
            if not x_groups or x - x_groups[-1] > 50:
                x_groups.append(x)

        # Determine row type
        is_paragraph = line_width > page_width * 0.55 and len(combined_text) > 60

        # Check for MasterFormat-style partial numbering (e.g., ".1", ".2")
        # These should be treated as list items, not table rows
        has_partial_numbering = False
        if row_words:
            first_word = row_words[0]["text"].strip()
            if PARTIAL_NUMBERING_PATTERN.match(first_word):
                has_partial_numbering = True

        row_info.append(
            {
                "y_key": y_key,
                "words": row_words,
                "text": combined_text,
                "x_groups": x_groups,
                "is_paragraph": is_paragraph,
                "num_columns": len(x_groups),
                "has_partial_numbering": has_partial_numbering,
            }
        )

    logging.info(f"[NATIVE_TABLE] Se analizaron {len(row_info)} filas horizontales potenciales.")

    # Collect ALL x-positions from rows with 3+ columns (table-like rows)
    # This gives us the global column structure
    all_table_x_positions: list[float] = []
    for info in row_info:
        if info["num_columns"] >= 3 and not info["is_paragraph"]:
            all_table_x_positions.extend(info["x_groups"])

    if not all_table_x_positions:
        logging.info("[NATIVE_TABLE] No se encontraron filas con 3 o más columnas. Se asume que no hay tablas.")
        return None

    logging.info(f"[NATIVE_TABLE] Se encontraron posiciones X para columnas: {len(all_table_x_positions)}")

    # Compute adaptive column clustering tolerance based on gap analysis
    all_table_x_positions.sort()

    # Calculate gaps between consecutive x-positions
    gaps = []
    for i in range(len(all_table_x_positions) - 1):
        gap = all_table_x_positions[i + 1] - all_table_x_positions[i]
        if gap > 5:  # Only significant gaps
            gaps.append(gap)

    # Determine optimal tolerance using statistical analysis
    if gaps and len(gaps) >= 3:
        # Use 70th percentile of gaps as threshold (balances precision/recall)
        sorted_gaps = sorted(gaps)
        percentile_70_idx = int(len(sorted_gaps) * 0.70)
        adaptive_tolerance = sorted_gaps[percentile_70_idx]

        # Clamp tolerance to reasonable range [25, 50]
        adaptive_tolerance = max(25, min(50, adaptive_tolerance))
    else:
        # Fallback to conservative value
        adaptive_tolerance = 35

    # Compute global column boundaries using adaptive tolerance
    global_columns: list[float] = []
    for x in all_table_x_positions:
        if not global_columns or x - global_columns[-1] > adaptive_tolerance:
            global_columns.append(x)

    logging.info(f"[NATIVE_TABLE] Se estimaron {len(global_columns)} columnas globales con tolerancia {adaptive_tolerance}.")

    # Adaptive max column check based on page characteristics
    # Calculate average column width
    if len(global_columns) > 1:
        content_width = global_columns[-1] - global_columns[0]
        avg_col_width = content_width / len(global_columns)

        # Forms with very narrow columns (< 30px) are likely dense text
        if avg_col_width < 30:
            logging.info(f"[NATIVE_TABLE] Las columnas son muy angostas ({avg_col_width}px). Abortando detección de tabla.")
            return None

        # Compute adaptive max based on columns per inch
        # Typical forms have 3-8 columns per inch
        columns_per_inch = len(global_columns) / (content_width / 72)

        # If density is too high (> 10 cols/inch), likely not a form
        if columns_per_inch > 10:
            logging.info(f"[NATIVE_TABLE] Densidad de columnas demasiado alta ({columns_per_inch} cols/inch). Abortando.")
            return None

        # Adaptive max: allow more columns for wider pages
        # Standard letter is 612pt wide, so scale accordingly
        adaptive_max_columns = int(20 * (page_width / 612))
        adaptive_max_columns = max(15, adaptive_max_columns)  # At least 15

        if len(global_columns) > adaptive_max_columns:
            logging.info(f"[NATIVE_TABLE] Supera el máximo de columnas permitidas ({adaptive_max_columns}). Abortando.")
            return None
    else:
        # Single column, not a form
        logging.info("[NATIVE_TABLE] Solo hay 1 columna, por lo tanto no es tabla.")
        return None

    # Now classify each row as table row or not
    # A row is a table row if it has words that align with 2+ of the global columns
    for info in row_info:
        if info["is_paragraph"]:
            info["is_table_row"] = False
            continue

        # Rows with partial numbering (e.g., ".1", ".2") are list items, not table rows
        if info["has_partial_numbering"]:
            info["is_table_row"] = False
            continue

        # Count how many global columns this row's words align with
        aligned_columns: set[int] = set()
        for word in info["words"]:
            word_x = word["x0"]
            for col_idx, col_x in enumerate(global_columns):
                if abs(word_x - col_x) < 40:
                    aligned_columns.add(col_idx)
                    break

        # If row uses 2+ of the established columns, it's a table row
        info["is_table_row"] = len(aligned_columns) >= 2

    # Find table regions (consecutive table rows)
    table_regions: list[tuple[int, int]] = []  # (start_idx, end_idx)
    i = 0
    while i < len(row_info):
        if row_info[i]["is_table_row"]:
            start_idx = i
            while i < len(row_info) and row_info[i]["is_table_row"]:
                i += 1
            end_idx = i
            table_regions.append((start_idx, end_idx))
        else:
            i += 1

    # Check if enough rows are table rows (at least 5%)
    total_table_rows = sum(end - start for start, end in table_regions)
    logging.info(f"[NATIVE_TABLE] Hay {total_table_rows} filas de tabla en {len(table_regions)} regiones, sobre un total de {len(row_info)} filas.")
    if len(row_info) > 0 and total_table_rows / len(row_info) < 0.05:
        logging.info(f"[NATIVE_TABLE] Menos del 5% son filas de tabla ({total_table_rows/len(row_info)}). Abortando.")
        return None

    logging.info("[NATIVE_TABLE] ¡Tabla válida detectada! Procediendo a renderizarla en Markdown.")
    # Build output - collect table data first, then format with proper column widths
    result_lines: list[str] = []
    num_cols = len(global_columns)

    # Helper function to extract cells from a row
    def extract_cells(info: dict) -> list[str]:
        cells: list[str] = ["" for _ in range(num_cols)]
        for word in info["words"]:
            word_x = word["x0"]
            # Find the correct column using boundary ranges
            assigned_col = num_cols - 1  # Default to last column
            for col_idx in range(num_cols - 1):
                col_end = global_columns[col_idx + 1]
                if word_x < col_end - 20:
                    assigned_col = col_idx
                    break
            if cells[assigned_col]:
                cells[assigned_col] += " " + word["text"]
            else:
                cells[assigned_col] = word["text"]
        return cells

    # Process rows, collecting table data for proper formatting
    idx = 0
    while idx < len(row_info):
        info = row_info[idx]

        # Check if this row starts a table region
        table_region = None
        for start, end in table_regions:
            if idx == start:
                table_region = (start, end)
                break

        if table_region:
            start, end = table_region
            # Collect all rows in this table
            table_data: list[list[str]] = []
            for table_idx in range(start, end):
                cells = extract_cells(row_info[table_idx])
                table_data.append(cells)

            # Calculate column widths for this table
            if table_data:
                col_widths = [
                    max(len(row[col]) for row in table_data) for col in range(num_cols)
                ]
                # Ensure minimum width of 3 for separator dashes
                col_widths = [max(w, 3) for w in col_widths]

                # Format header row
                header = table_data[0]
                header_str = (
                    "| "
                    + " | ".join(
                        cell.ljust(col_widths[i]) for i, cell in enumerate(header)
                    )
                    + " |"
                )
                result_lines.append(header_str)

                # Format separator row
                separator = (
                    "| "
                    + " | ".join("-" * col_widths[i] for i in range(num_cols))
                    + " |"
                )
                result_lines.append(separator)

                # Format data rows
                for row in table_data[1:]:
                    row_str = (
                        "| "
                        + " | ".join(
                            cell.ljust(col_widths[i]) for i, cell in enumerate(row)
                        )
                        + " |"
                    )
                    result_lines.append(row_str)

            idx = end  # Skip to end of table region
        else:
            # Check if we're inside a table region (not at start)
            in_table = False
            for start, end in table_regions:
                if start < idx < end:
                    in_table = True
                    break

            if not in_table:
                # Non-table content
                text = info["text"]
                if font_stats and text.strip():
                    base = font_stats['base']
                    h3_min = font_stats.get('h3_min')
                    h2_min = font_stats.get('h2_min')
                    h1_min = font_stats.get('h1_min')
                    
                    # Compute dominant size for the row
                    sizes = [round(w.get('size', 0)) for w in info["words"] if w.get('size', 0) > 0]
                    if sizes:
                        dominant_size = max(set(sizes), key=sizes.count)
                        if dominant_size > base and len(text.strip()) < 150:
                            if h1_min is not None and dominant_size >= h1_min:
                                text = f"# {text}"
                            elif h2_min is not None and dominant_size >= h2_min:
                                text = f"## {text}"
                            elif h3_min is not None and dominant_size >= h3_min:
                                text = f"### {text}"

                result_lines.append(text)
            idx += 1

    return "\n".join(result_lines)


def _extract_tables_from_words(page: Any) -> list[list[list[str]]]:
    """
    Extract tables from a PDF page by analyzing word positions.
    This handles borderless tables where words are aligned in columns.

    This function is designed for structured tabular data (like invoices),
    not for multi-column text layouts in scientific documents.
    """
    words = page.extract_words(keep_blank_chars=True, x_tolerance=3, y_tolerance=3)
    if not words:
        return []

    # Group words by their Y position (rows)
    y_tolerance = 5
    rows_by_y: dict[float, list[dict]] = {}
    for word in words:
        y_key = round(word["top"] / y_tolerance) * y_tolerance
        if y_key not in rows_by_y:
            rows_by_y[y_key] = []
        rows_by_y[y_key].append(word)

    # Sort rows by Y position
    sorted_y_keys = sorted(rows_by_y.keys())

    # Find potential column boundaries by analyzing x positions across all rows
    all_x_positions = []
    for words_in_row in rows_by_y.values():
        for word in words_in_row:
            all_x_positions.append(word["x0"])

    if not all_x_positions:
        return []

    # Cluster x positions to find column starts
    all_x_positions.sort()
    x_tolerance_col = 20
    column_starts: list[float] = []
    for x in all_x_positions:
        if not column_starts or x - column_starts[-1] > x_tolerance_col:
            column_starts.append(x)

    # Need at least 3 columns but not too many (likely text layout, not table)
    if len(column_starts) < 3 or len(column_starts) > 10:
        return []

    # Find rows that span multiple columns (potential table rows)
    table_rows = []
    for y_key in sorted_y_keys:
        words_in_row = sorted(rows_by_y[y_key], key=lambda w: w["x0"])

        # Assign words to columns
        row_data = [""] * len(column_starts)
        for word in words_in_row:
            # Find the closest column
            best_col = 0
            min_dist = float("inf")
            for i, col_x in enumerate(column_starts):
                dist = abs(word["x0"] - col_x)
                if dist < min_dist:
                    min_dist = dist
                    best_col = i

            if row_data[best_col]:
                row_data[best_col] += " " + word["text"]
            else:
                row_data[best_col] = word["text"]

        # Only include rows that have content in multiple columns
        non_empty = sum(1 for cell in row_data if cell.strip())
        if non_empty >= 2:
            table_rows.append(row_data)

    # Validate table quality - tables should have:
    # 1. Enough rows (at least 3 including header)
    # 2. Short cell content (tables have concise data, not paragraphs)
    # 3. Consistent structure across rows
    if len(table_rows) < 3:
        return []

    # Check if cells contain short, structured data (not long text)
    long_cell_count = 0
    total_cell_count = 0
    for row in table_rows:
        for cell in row:
            if cell.strip():
                total_cell_count += 1
                # If cell has more than 30 chars, it's likely prose text
                if len(cell.strip()) > 30:
                    long_cell_count += 1

    # If more than 30% of cells are long, this is probably not a table
    if total_cell_count > 0 and long_cell_count / total_cell_count > 0.3:
        return []

    return [table_rows]

def _calculate_global_margins(pdf: Any) -> tuple[float | None, float | None]:
    """
    Scans the first 10 pages of the PDF to find consistent horizontal lines
    that act as header/footer separators.
    
    Returns a tuple (header_y, footer_y).
    """
    max_pages = min(10, len(pdf.pages))
    if max_pages == 0:
        return None, None
        
    header_candidates = []
    footer_candidates = []
    
    for page_idx in range(max_pages):
        try:
            page = pdf.pages[page_idx]
            page_width = float(page.width)
            page_height = float(page.height)
            
            min_line_length = page_width * 0.60
            
            if not hasattr(page, "lines") or not page.lines:
                continue
                
            for line in page.lines:
                # Check if line is horizontal
                if abs(line.get('top', 0) - line.get('bottom', 0)) <= 2:
                    length = abs(line.get('x1', 0) - line.get('x0', 0))
                    if length >= min_line_length:
                        y_pos = (line.get('top', 0) + line.get('bottom', 0)) / 2
                        
                        if y_pos <= page_height * 0.15:
                            header_candidates.append(y_pos)
                        elif y_pos >= page_height * 0.85:
                            footer_candidates.append(y_pos)
        except Exception:
            continue
                        
    # Find consensus (mode with tolerance)
    def find_consensus(candidates: list[float]) -> float | None:
        if not candidates:
            return None
        # Group candidates within 5 points of each other
        groups = []
        for c in candidates:
            added = False
            for g in groups:
                if abs(g['avg'] - c) <= 5:
                    g['values'].append(c)
                    g['avg'] = sum(g['values']) / len(g['values'])
                    added = True
                    break
            if not added:
                groups.append({'avg': c, 'values': [c]})
        
        # Find group with highest count
        best_group = max(groups, key=lambda g: len(g['values']))
        # Require it to appear in at least 2 pages
        min_required = max(2, int(max_pages * 0.3))
        if len(best_group['values']) >= min_required:
            return best_group['avg']
        return None
        
    return find_consensus(header_candidates), find_consensus(footer_candidates)

def _crop_page(page: Any, page_num: int, global_header_y: float | None, global_footer_y: float | None) -> Any:
    page_height = float(page.height)
    page_width = float(page.width)
    
    # 1. Base margins from global lines if they exist
    top_margin = global_header_y if global_header_y is not None else 0.0
    bottom_margin = global_footer_y if global_footer_y is not None else page_height
    
    # 2. If no global line, use conservative percentages, BUT NOT on special pages
    is_special_page = False
    
    # Check if TOC
    try:
        text = page.extract_text()
        if text:
            text_lower = text.lower()
            if "índice" in text_lower or "tabla de contenido" in text_lower or "table of contents" in text_lower or "contenido" in text_lower[:500]:
                is_special_page = True
    except Exception:
        pass
            
    if not is_special_page:
        if global_header_y is None:
            top_margin = page_height * 0.05
        if global_footer_y is None:
            bottom_margin = page_height * 0.95
            
    # Apply small offset if using line, to ensure the line itself is cut out
    if global_header_y is not None:
        top_margin += 2
    if global_footer_y is not None:
        bottom_margin -= 2
        
    # Safety clamp
    top_margin = max(0.0, min(top_margin, page_height * 0.3))
    bottom_margin = max(page_height * 0.7, min(bottom_margin, page_height))
    
    if top_margin > 0 or bottom_margin < page_height:
        bbox = (0, top_margin, page_width, bottom_margin)
        return page.crop(bbox)
    
    return page

def _calculate_font_statistics(pdf: Any) -> dict | None:
    """
    Scans up to the first 10 pages to build a histogram of font sizes.
    Returns thresholds for H1 / H2 / H3 detection, or None if not enough data.
    """
    max_pages = min(10, len(pdf.pages))
    size_counts: dict[int, int] = {}

    for page_idx in range(max_pages):
        try:
            for char in pdf.pages[page_idx].chars:
                size = round(char.get('size', 0))
                if size > 0:
                    size_counts[size] = size_counts.get(size, 0) + 1
        except Exception:
            continue

    if not size_counts:
        return None

    # Base = most frequent size (moda)
    base_size = max(size_counts, key=lambda s: size_counts[s])
    logging.info(f"[HIERARCHY] Tamaño de fuente base (moda): {base_size}pt")

    # All unique sizes strictly above base, sorted ascending
    above_base = sorted(s for s in size_counts if s > base_size)
    if not above_base:
        logging.info("[HIERARCHY] No hay tamaños por encima de la base. Sin jerarquía.")
        return None

    # Remove top 1% outliers (by sorted position, not frequency)
    cutoff = max(1, int(len(above_base) * 0.99))
    above_base = above_base[:cutoff]

    # Split into up to 3 buckets: smallest → H3, middle → H2, largest → H1
    n = len(above_base)
    if n == 1:
        thresholds = {'h3_min': above_base[0], 'h2_min': None, 'h1_min': None}
    elif n == 2:
        thresholds = {'h3_min': above_base[0], 'h2_min': above_base[1], 'h1_min': None}
    else:
        third = n // 3
        thresholds = {
            'h3_min': above_base[0],
            'h2_min': above_base[third],
            'h1_min': above_base[2 * third],
        }

    logging.info(
        f"[HIERARCHY] Umbrales calculados: "
        f"H1>={thresholds['h1_min']}pt, "
        f"H2>={thresholds['h2_min']}pt, "
        f"H3>={thresholds['h3_min']}pt"
    )
    return {'base': base_size, **thresholds}


def _extract_text_with_hierarchy(page: Any, font_stats: dict | None) -> str:
    """
    Extracts text from a page while applying Markdown heading markers
    based on font analysis.

    Algorithm:
    1. Group characters into lines by Y coordinate.
    2. Enrich each line with dominant font size, font name, and left margin.
    3. Group consecutive lines into semantic blocks:
       - Heading block   -> one or more lines with above-base font size
       - Paragraph block -> consecutive body lines with similar left margin
    4. Render each block:
       - Headings  -> # / ## / ### prefix (length < 150 chars)
       - Paragraph -> lines joined with a single space (no mid-sentence newlines)
    """
    chars = page.chars
    if not chars:
        return page.extract_text() or ''

    # --- Step 1: Group chars into lines by Y position (5px tolerance) ---
    y_tol = 5
    lines_by_y: dict[float, list] = {}
    for char in chars:
        y_key = round(char['top'] / y_tol) * y_tol
        if y_key not in lines_by_y:
            lines_by_y[y_key] = []
        lines_by_y[y_key].append(char)

    raw_lines: list[dict] = []
    for y_key in sorted(lines_by_y.keys()):
        line_chars = sorted(lines_by_y[y_key], key=lambda c: c['x0'])
        text = ''.join(c['text'] for c in line_chars)

        # Dominant size (mode)
        size_freq: dict[int, int] = {}
        for c in line_chars:
            s = round(c.get('size', 0))
            if s > 0:
                size_freq[s] = size_freq.get(s, 0) + 1
        dominant_size = max(size_freq, key=lambda s: size_freq[s]) if size_freq else 0

        # Dominant font name (mode)
        font_freq: dict[str, int] = {}
        for c in line_chars:
            fn = c.get('fontname', '') or ''
            if fn:
                font_freq[fn] = font_freq.get(fn, 0) + 1
        dominant_font = max(font_freq, key=lambda f: font_freq[f]) if font_freq else ''

        # Left and right margins of the line
        x0 = line_chars[0]['x0'] if line_chars else 0.0
        x1 = line_chars[-1]['x1'] if line_chars else 0.0

        raw_lines.append({
            'text': text,
            'size': dominant_size,
            'fontname': dominant_font,
            'x0': x0,
            'x1': x1,
            'y': y_key,
        })

    if not raw_lines:
        return ''

    # If no font stats, fall back to a simple joined output
    if not font_stats:
        return '\n'.join(line['text'] for line in raw_lines)

    base = font_stats['base']
    h3_min = font_stats.get('h3_min')
    h2_min = font_stats.get('h2_min')
    h1_min = font_stats.get('h1_min')

    def _heading_prefix(size: int, text: str) -> str:
        """Return the Markdown heading prefix for a line, or '' if not a heading."""
        if size > base and len(text.strip()) < 150:
            if h1_min is not None and size >= h1_min:
                return '# '
            if h2_min is not None and size >= h2_min:
                return '## '
            if h3_min is not None and size >= h3_min:
                return '### '
        return ''

    # --- Step 2: Group lines into semantic blocks ---
    blocks: list[list[dict]] = []
    current: list[dict] = [raw_lines[0]]

    for i in range(1, len(raw_lines)):
        prev = raw_lines[i - 1]
        curr = raw_lines[i]

        gap = curr['y'] - prev['y']
        line_height = max(prev['size'], base, 10)

        prev_heading = bool(_heading_prefix(prev['size'], prev['text']))
        curr_heading = bool(_heading_prefix(curr['size'], curr['text']))

        # Keep consecutive same-level heading lines together; split otherwise
        same_heading_level = (
            prev_heading and curr_heading and prev['size'] == curr['size']
            and len(' '.join(l['text'].strip() for l in current + [curr])) < 150
        )

        page_width = float(page.width) if hasattr(page, 'width') else 612.0
        prev_width = prev['x1'] - prev['x0']
        is_prev_short = prev_width < (page_width * 0.6)

        starts_with_bullet = bool(re.match(r'^[\-\•\*\>]\s|^[0-9]+\.\s', curr['text'].strip()))

        should_break = (
            gap > line_height * 2.2                          # big vertical gap (increased to 2.2 for double spacing)
            or (curr_heading and not same_heading_level)     # new heading starts
            or (prev_heading and not curr_heading)           # heading just ended
            or (is_prev_short and not same_heading_level)    # previous line ended early (hard break / list item)
            or starts_with_bullet                            # explicit list item
        )

        if should_break:
            blocks.append(current)
            current = [curr]
        else:
            current.append(curr)

    blocks.append(current)

    # --- Step 3: Render each block as Markdown ---
    result: list[str] = []

    for block in blocks:
        if not block:
            continue

        first = block[0]
        is_heading = bool(_heading_prefix(first['size'], first['text']))

        if is_heading:
            # Merge all lines into a single heading (multi-line title support)
            combined = ' '.join(l['text'].strip() for l in block).strip()
            prefix = _heading_prefix(first['size'], combined)
            result.append(f"{prefix}{combined}" if prefix else combined)

        else:
            # Regular paragraph: join lines with spaces (no mid-sentence breaks)
            paragraph = ' '.join(l['text'].strip() for l in block if l['text'].strip())
            if paragraph:
                result.append(paragraph)

    # Blocks are separated by a blank line for clean Markdown structure
    return '\n\n'.join(result)


class PdfConverter(DocumentConverter):
    """
    Converts PDFs to Markdown.
    Supports extracting tables into aligned Markdown format (via pdfplumber).
    Falls back to pdfminer if pdfplumber is missing or fails.
    """

    def accepts(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> bool:
        mimetype = (stream_info.mimetype or "").lower()
        extension = (stream_info.extension or "").lower()

        if extension in ACCEPTED_FILE_EXTENSIONS:
            return True

        for prefix in ACCEPTED_MIME_TYPE_PREFIXES:
            if mimetype.startswith(prefix):
                return True

        return False

    def convert(
        self,
        file_stream: BinaryIO,
        stream_info: StreamInfo,
        **kwargs: Any,
    ) -> DocumentConverterResult:
        if _dependency_exc_info is not None:
            raise MissingDependencyException(
                MISSING_DEPENDENCY_MESSAGE.format(
                    converter=type(self).__name__,
                    extension=".pdf",
                    feature="pdf",
                )
            ) from _dependency_exc_info[1].with_traceback(
                _dependency_exc_info[2]
            )  # type: ignore[union-attr]

        assert isinstance(file_stream, io.IOBase)

        # Read file stream into BytesIO for compatibility with pdfplumber
        pdf_bytes = io.BytesIO(file_stream.read())

        try:
            # Single pass: check every page for form-style content.
            # Pages with tables/forms get rich extraction; plain-text
            # pages are collected separately. page.close() is called
            # after each page to free pdfplumber's cached objects and
            # keep memory usage constant regardless of page count.
            markdown_chunks: list[str] = []
            form_page_count = 0
            plain_page_indices: list[int] = []

            with pdfplumber.open(pdf_bytes) as pdf:
                logging.info(f"[NATIVE] PDF abierto exitosamente. Total de páginas: {len(pdf.pages)}")

                global_header_y, global_footer_y = _calculate_global_margins(pdf)
                logging.info(f"[NATIVE] Consenso de márgenes globales calculado: Header Y={global_header_y}, Footer Y={global_footer_y}")

                font_stats = _calculate_font_statistics(pdf)

                for page_idx, page in enumerate(pdf.pages):
                    page_num = page_idx + 1
                    logging.info(f"[NATIVE] Extrayendo contenido de la página {page_num}...")

                    cropped_page = _crop_page(page, page_num, global_header_y, global_footer_y)

                    page_content = _extract_form_content_from_words(cropped_page, font_stats)

                    if page_content is not None:
                        form_page_count += 1
                        if page_content.strip():
                            markdown_chunks.append(page_content)
                    else:
                        plain_page_indices.append(page_idx)
                        text = _extract_text_with_hierarchy(cropped_page, font_stats)
                        if text and text.strip():
                            markdown_chunks.append(text.strip())

                    page.close()  # Free cached page data immediately

            # If no pages had form-style content, use our hierarchical
            # extractor across all pages (better than raw pdfminer for prose).
            if form_page_count == 0:
                logging.info("[NATIVE] No se detectaron tablas. Usando extractor jerárquico sobre todo el documento.")
                if font_stats:
                    # Already processed above, markdown_chunks has the hierarchy
                    markdown = "\n\n".join(markdown_chunks).strip()
                    if not markdown:
                        pdf_bytes.seek(0)
                        markdown = pdfminer.high_level.extract_text(pdf_bytes)
                else:
                    pdf_bytes.seek(0)
                    markdown = pdfminer.high_level.extract_text(pdf_bytes)
            else:
                logging.info(f"[NATIVE] Se extrajeron {form_page_count} páginas con contenido tabular o de formulario estructurado.")
                markdown = "\n\n".join(markdown_chunks).strip()

        except Exception:
            # Fallback if pdfplumber fails
            pdf_bytes.seek(0)
            markdown = pdfminer.high_level.extract_text(pdf_bytes)

        # Fallback if still empty
        if not markdown:
            pdf_bytes.seek(0)
            markdown = pdfminer.high_level.extract_text(pdf_bytes)

        # Post-process to merge MasterFormat-style partial numbering with following text
        markdown = _merge_partial_numbering_lines(markdown)

        return DocumentConverterResult(markdown=markdown)
