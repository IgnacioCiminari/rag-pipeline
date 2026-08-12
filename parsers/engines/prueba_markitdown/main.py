from markitdown import MarkItDown
from openai import OpenAI
import markitdown_ocr
import logging

def main():
    # Configuramos el logging para que sobrescriba el archivo cada vez ("w")
    logging.basicConfig(
        filename="trace.log",
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    logging.info("Iniciando ejecución principal del script de MarkItDown.")

    ollama_client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama" # Ollama no pide key, pero la librería exige que no esté vacía
    )

    md = MarkItDown(
        enable_plugins=False,
        llm_client=ollama_client,
        llm_model="moondream"
    )
    
    # Registramos el plugin OCR local
    #markitdown_ocr.register_converters(md, llm_client=ollama_client, llm_model="moondream")

    result = md.convert("despliegue_con_compose.pdf")
    safe_preview = result.text_content.encode("cp1252", errors="replace").decode("cp1252")
    print(f"El contenido extraido es: {safe_preview}")

    with open("archivo_prueba.md", "w", encoding="utf-8") as f:
        f.write(result.text_content)

if __name__ == "__main__":
    main()
