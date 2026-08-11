# Problema de investigación

Los sistemas de Retrieval-Augmented Generation (RAG) dependen de la calidad del contenido recuperado para generar respuestas precisas. Cuando la información proviene de documentos PDF, es frecuente que el proceso de extracción introduzca errores, omita información o altere la estructura original del documento. Como consecuencia, los fragmentos de texto utilizados como contexto por el modelo de lenguaje pueden no representar fielmente el contenido del documento fuente, afectando la calidad de las respuestas generadas.

Dado que existen múltiples herramientas para realizar la extracción de texto desde archivos PDF, surge la necesidad de evaluar cuál de ellas produce una representación más fiel del contenido original y, por lo tanto, resulta más adecuada para ser utilizada en un sistema RAG.

# Pregunta principal de investigación

¿Cuál de los parsers de documentos PDF evaluados permite obtener una representación más fiel del contenido original del documento para su utilización en un sistema RAG?

# Objetivo general

Evaluar y comparar diferentes parsers de documentos PDF para determinar cuál ofrece la extracción de texto más fiel al contenido original, con el fin de mejorar la calidad de la información utilizada por un sistema RAG.

# Objetivos específicos

- Identificar y seleccionar distintos parsers de PDF que puedan utilizarse como alternativa al parser actualmente implementado.
- Definir criterios que permitan evaluar la fidelidad de la información extraída por cada parser.
- Comparar el desempeño de los parsers seleccionados sobre un conjunto representativo de documentos PDF.
- Analizar las ventajas y limitaciones de cada alternativa en función de la calidad del texto obtenido.
- Determinar, a partir de los resultados obtenidos, si resulta conveniente mantener el parser actual, reemplazarlo por otro o adoptar una estrategia híbrida.

# Alcance

La evaluación se realizará sobre documentos PDF de carácter predominantemente textual, tales como artículos científicos, documentación técnica y manuales. Los documentos podrán contener títulos, bloques de texto, listas, tablas, imágenes y contenido organizado en múltiples columnas.

Se incluirán tanto documentos PDF de origen digital como documentos escaneados, considerando que las herramientas evaluadas pueden incorporar mecanismos de reconocimiento óptico de caracteres (OCR) como parte de su proceso de extracción.

Quedan fuera del alcance de este trabajo los documentos cuyo contenido dependa principalmente de expresiones matemáticas, fórmulas o código fuente, debido a que estos requieren criterios de extracción y evaluación específicos que exceden los objetivos de esta investigación.

# Definición operativa de un buen parseo

- Se considerará que un parser realiza un buen parseo cuando el contenido extraído represente de forma fiel la información presente en el documento PDF original. Para ello se evaluará que:

- El texto conserve su contenido sin omisiones, alteraciones o incorporaciones incorrectas.
- La estructura lógica del documento, incluyendo títulos, párrafos, listas, tablas y columnas, se preserve de la manera más fiel posible.
- Las imágenes y otros elementos no textuales sean identificados y referenciados adecuadamente cuando corresponda.
- Se minimicen errores derivados del proceso de extracción, tales como caracteres incorrectos, fragmentación de palabras, desorden en la secuencia del contenido o pérdida de información.

# Hipótesis inicial

Se plantea que existen diferencias significativas en la calidad del parseo entre los distintos parsers de documentos PDF y que al menos una de las alternativas evaluadas, o una combinación de ellas, ofrecerá una representación del contenido más fiel que la obtenida con el parser actualmente utilizado.

# Métricas de evaluación

La comparación entre los distintos parsers se realizará considerando métricas que permitan evaluar la fidelidad del contenido extraído respecto del documento PDF original. En particular, se analizarán aspectos como:

- La preservación del contenido textual.
- La conservación de la estructura lógica del documento (títulos, párrafos, listas, tablas y columnas).
- La cantidad y el tipo de errores introducidos durante el proceso de extracción.
- La capacidad para representar correctamente elementos no textuales cuando corresponda.

Las métricas específicas y su forma de cálculo podrán ajustarse durante el desarrollo de la investigación en función de los resultados obtenidos y de las necesidades que surjan en la etapa experimental.

# Corpus o conjunto de documentos

El corpus de evaluación estará compuesto por documentos PDF de carácter predominantemente textual, incluyendo artículos científicos, documentación técnica y manuales. Se procurará que el conjunto represente diferentes estructuras de documento, incorporando casos con títulos, listas, tablas, imágenes, fórmulas, código y múltiples columnas.

Durante el desarrollo de la investigación, el corpus podrá ajustarse o ampliarse con el fin de incorporar nuevos casos de prueba o reemplazar documentos que no se encuentren alineados con el alcance definido.

# Herramientas y parsers candidatos

Se evaluará el parser actualmente utilizado por el proyecto (DeepDoc) y se lo comparará con distintas alternativas disponibles (MarkItDown). La selección de herramientas podrá ampliarse o reducirse a medida que surjan nuevos parsers o tecnologías de extracción que resulten relevantes para la investigación.

La lista definitiva de herramientas se establecerá antes de la etapa de evaluación experimental, procurando incluir alternativas representativas y actualizadas.
