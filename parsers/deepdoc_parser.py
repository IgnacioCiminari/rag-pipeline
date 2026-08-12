from deepdoc.parser.pdf_parser import RAGFlowPdfParser, extract_pdf_outlines
import os

def parse_with_deepdoc(input_pdf_path, output_md_path):
    parser = RAGFlowPdfParser()
    zoomin = 3
    
    # Run the internal pipeline step by step to intercept the structured boxes
    parser.outlines = extract_pdf_outlines(input_pdf_path)
    parser.__images__(input_pdf_path, zoomin)
    parser._layouts_rec(zoomin)
    parser._table_transformer_job(zoomin, auto_rotate=True)
    parser._text_merge()
    parser._concat_downward()
    parser._filter_forpages()
    
    # Extract tables and figures with their positions (need_position=True)
    tbls = parser._extract_table_figure(need_image=False, ZM=zoomin, return_html=False, need_position=True, separate_tables_figures=False)
    
    elements = []
    
    # 1. Process tables and figures
    for item in tbls:
        # tbls contains list of ((img, data), poss)
        res_tuple, poss = item
        img, data = res_tuple
        if not poss:
            continue
        # poss is [(page_index, left, right, top, bottom), ...]
        page_idx, left, right, top, bott = poss[0]
        # Make page number 1-indexed to match text boxes
        pn = page_idx + 1
        elements.append({
            "type": "table_or_figure",
            "page_number": pn,
            "top": top,
            "data": data
        })
        
    # 2. Process text boxes
    for box in parser.boxes:
        pn = box["page_number"]
        # box["top"] is cumulative, we subtract the cumulative height of previous pages
        ht = parser.page_cum_height[pn - 1]
        local_top = box["top"] - ht
        
        layout_type = box.get("layout_type", "text")
        # Optional: skip headers and footers to keep MD clean
        if layout_type in ["header", "footer"]:
            continue
            
        elements.append({
            "type": layout_type,
            "page_number": pn,
            "top": local_top,
            "data": box.get("text", "")
        })
        
    # 3. Sort all elements by page number, then by vertical position
    elements.sort(key=lambda x: (x["page_number"], x["top"]))
    
    # 4. Generate final Markdown
    md_content = ""
    for el in elements:
        t = el["type"]
        data = el["data"]
        
        if isinstance(data, list):
            content = "\n".join([str(d) for d in data])
        else:
            content = str(data)
            
        if t == "title":
            md_content += f"## {content}\n\n"
        elif t == "table_or_figure":
            md_content += f"{content}\n\n"
        else:
            md_content += f"{content}\n\n"
            
    os.makedirs(os.path.dirname(output_md_path), exist_ok=True)
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    return True
