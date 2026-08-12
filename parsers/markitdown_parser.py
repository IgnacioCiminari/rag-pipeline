from parsers.engines.prueba_markitdown.markitdown import MarkItDown
from openai import OpenAI
import os

def parse_with_markitdown(input_pdf_path, output_md_path):
    ollama_client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )
    md = MarkItDown(
        enable_plugins=False,
        llm_client=ollama_client,
        llm_model="moondream"
    )
    

    result = md.convert(input_pdf_path)
    
    os.makedirs(os.path.dirname(output_md_path), exist_ok=True)
    with open(output_md_path, "w", encoding="utf-8") as f:
        f.write(result.text_content)
    
    return True
