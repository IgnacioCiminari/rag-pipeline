import os
import glob
import sys

# Agregar el directorio raíz al path para que pueda importar la carpeta 'parsers'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers.deepdoc_parser import parse_with_deepdoc
from parsers.markitdown_parser import parse_with_markitdown

def main():
    # Directorios de entrada y salida
    input_dir = os.path.join("datos", "corpus_original")
    output_base_dir = "resultados/prueba_formato"
    
    dd_out_dir = os.path.join(output_base_dir, "deepdoc")
    mkd_out_dir = os.path.join(output_base_dir, "markitdown")
    
    os.makedirs(dd_out_dir, exist_ok=True)
    os.makedirs(mkd_out_dir, exist_ok=True)
    
    # Obtener todos los archivos PDF del corpus original
    pdf_files = glob.glob(os.path.join(input_dir, "*.pdf"))
    
    if not pdf_files:
        print(f"No se encontraron archivos PDF en '{input_dir}'.")
        return
        
    for pdf_file in pdf_files:
        base_name = os.path.basename(pdf_file)
        name_without_ext = os.path.splitext(base_name)[0]
        
        print(f"\n--- Procesando: {base_name} ---")
        
        # 1. DeepDoc
        out_dd = os.path.join(dd_out_dir, f"{name_without_ext}.md")
        print("Ejecutando DeepDoc...")
        try:
            parse_with_deepdoc(pdf_file, out_dd)
            print(f"  -> Éxito. Guardado en: {out_dd}")
        except Exception as e:
            print(f"  -> Error con DeepDoc: {e}")
        
        # 2. MarkItDown
        out_mkd = os.path.join(mkd_out_dir, f"{name_without_ext}.md")
        print("Ejecutando MarkItDown...")
        try:
            parse_with_markitdown(pdf_file, out_mkd)
            print(f"  -> Éxito. Guardado en: {out_mkd}")
        except Exception as e:
            print(f"  -> Error con MarkItDown: {e}")
            
    print("\nProcesamiento finalizado.")

if __name__ == "__main__":
    main()
