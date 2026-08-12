import pdfplumber
import sys
import os
import glob
import re

class ImageCounterSingleton:
    _instance = None

    def __new__(cls, output_dir):
        if cls._instance is None:
            cls._instance = super(ImageCounterSingleton, cls).__new__(cls)
            cls._instance.output_dir = output_dir
            cls._instance._initialize_counter()
        return cls._instance

    def _initialize_counter(self):
        os.makedirs(self.output_dir, exist_ok=True)
        files = glob.glob(os.path.join(self.output_dir, "cajas_dibujadas_*.png"))
        max_n = -1
        for f in files:
            basename = os.path.basename(f)
            match = re.search(r"cajas_dibujadas_(\d+)\.png", basename)
            if match:
                n = int(match.group(1))
                if n > max_n:
                    max_n = n
        self.current_n = max_n + 1

    def get_next_filename(self):
        filename = f"cajas_dibujadas_{self.current_n}.png"
        self.current_n += 1
        return os.path.join(self.output_dir, filename)

def visualize_boxes(pdf_path, page_num=0):
    # Setup the output directory path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "visualized_pdfs")
    
    counter = ImageCounterSingleton(output_dir)
    output_png_path = counter.get_next_filename()

    with pdfplumber.open(pdf_path) as pdf:
        if page_num >= len(pdf.pages):
            print(f"La página {page_num} no existe.")
            return
            
        page = pdf.pages[page_num]
        
        # Obtener todas las palabras y sus cajas (Bounding Boxes)
        words = page.extract_words()
        
        # Convertir la página a una imagen con alta resolución
        im = page.to_image(resolution=150)
        
        # Dibujar rectángulos explícitos rojos alrededor de cada palabra
        im.draw_rects(words, stroke="red", stroke_width=2, fill=None)
        
        # Guardar la imagen para que la puedas visualizar
        im.save(output_png_path, format="PNG")
        print(f"¡Cajas dibujadas! Revisá el archivo: {output_png_path}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: uv run visualize_boxes.py <input.pdf>")
    else:
        visualize_boxes(sys.argv[1])
