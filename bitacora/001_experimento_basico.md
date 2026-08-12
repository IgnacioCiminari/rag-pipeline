# EXP-001 - Prueba de Formato de Salida de los Parsers

Fecha: 03-08-2026

# Pregunta o Decisión que se Quiere Investigar
¿Qué características presenta la salida en formato Markdown generada por el parser actualmente utilizado y en qué medida las alternativas evaluadas son capaces de preservar esas mismas características?

En particular, se analizará cómo cada parser representa distintos elementos del documento, como títulos, bloques de texto, listas, tablas, fórmulas, código, imágenes y contenido distribuido en múltiples columnas. A partir de esta comparación se busca determinar si las alternativas producen una salida suficientemente consistente con la estructura y el contenido del documento original como para ser consideradas en las siguientes etapas de la investigación.

# Objetivo de Esta Actividad

Evaluar preliminarmente dos parsers de documentos PDF, analizando la calidad y estructura del contenido obtenido en formato Markdown. El objetivo es determinar si el formato de salida resulta adecuado para representar la información extraída y si las herramientas evaluadas presentan características que permitan considerarlas como alternativas para las etapas posteriores de la investigación.

# Contexto y motivación

Esta prueba surge de la necesidad de evaluar distintas alternativas al proceso de parseo utilizado actualmente. Antes de realizar una comparación más amplia, se busca obtener una primera aproximación al comportamiento de los parsers seleccionados y detectar posibles limitaciones en la extracción y representación del contenido.

La prueba permitirá identificar problemas relacionados con la preservación de la estructura del documento y con el tratamiento de distintos tipos de contenido, proporcionando información para definir qué herramientas y qué tipos de documentos serán considerados en las siguientes etapas de la investigación.

# Documentos Utilizados

Estoy usando 4 documentos generados sintéticamente, que se encuentran el el corpus original. Estos son: "pdf_01_idioma.pdf", "pdf_02_codigo.pdf", "pdf_03_matematica.pdf" y "pdf_04_layout.pdf". 

# Herramientas 

Los parsers que estoy utilizando son el DeepDoc de RAGFlow y un MarkItDown modificado. 

# Código Utilizado

Uso la versión del código del commit 2 del repositorio https://github.com/IgnacioCiminari/rag-pipeline.git, ejecutando ```uv run ./codigo/main.py``` en Windows con las dependencias del pyproject.toml del mismo repo. 

# Resultados Observados

Los resultados generados se encuentran en ./resultados/prueba_formato. 
En esta prueba pude observar que DeepDoc maneja, a grandes rasgos, de forma regular los símbolos especiales del lenguaje, que no es capaz de reconocer columnas. Las listas las reconoce pero no de forma explícita. Además, las tablas utiliza un formato dificil de parsear que puede llegar a ser un problema en el futuro. Las fórmulas ni las detectó al igual que el código.....

# Decisiones

Por lo pronto vamos a mantener los dos parsers como alternativas, el DeepDoc porque es el parser base y el MarkItDown modificado porque reconoce y devuelve tablas a niveles excepcionales. Por lo pronto considero positivo descartar la idea de reconocer las fórmulas por el momento al igual que el código, principalmente por la dificultad de testear su existencia y su fiabilidad. Por lo tanto debería eliminar los pdfs 02 y 03, y agregar otro pdf que contenga listas. 

# Próximo Paso

Voy a agregar otro parser que tengo en la mira: Opendataloader, que tiene muy buena pinta. 
