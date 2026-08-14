# EXP-002 - Prueba de Nuevo Parser OpenDataLoader

Fecha: 12-08-2026

# Pregunta o Decisión que se Quiere Investigar

¿Qué estructuras y tipos de contenido de los documentos PDF es capaz de reconocer y representar el parser OpenDataLoader?

En particular, se analizará su capacidad para identificar y preservar elementos como títulos, bloques de texto, listas, tablas, fórmulas, código, imágenes y contenido distribuido en múltiples columnas. Para realizar la evaluación, se utilizarán los mismos documentos PDF empleados en el experimento anterior, permitiendo comparar el comportamiento del nuevo parser con los resultados obtenidos previamente.

A partir de los resultados se busca determinar si OpenDataLoader reconoce adecuadamente las estructuras relevantes de los documentos y si su comportamiento aporta ventajas o limitaciones respecto de los parsers ya seleccionados para la investigación.

# Objetivo de Esta Actividad

Evaluar el comportamiento del parser OpenDataLoader frente a los mismos documentos PDF utilizados en las pruebas anteriores, identificando qué estructuras y tipos de contenido es capaz de reconocer y extraer correctamente.

El objetivo es obtener una caracterización de sus capacidades de parseo y determinar si presenta características suficientemente adecuadas como para ser incorporado como una alternativa adicional en las siguientes etapas de la investigación.

# Contexto y Motivación

Esta prueba surge luego de haber seleccionado dos parsers que cumplen con los requisitos considerados en el experimento anterior y ante la posibilidad de incorporar OpenDataLoader como una alternativa adicional.

Para mantener la comparabilidad con las pruebas realizadas previamente, se utilizarán los mismos documentos PDF y se analizarán las mismas estructuras: títulos, texto, listas, tablas, fórmulas, código, imágenes y columnas.

La prueba permitirá determinar de manera preliminar qué elementos del documento son reconocidos por OpenDataLoader, cuáles presentan dificultades y si existen diferencias relevantes respecto de las herramientas ya evaluadas. Esta información permitirá decidir si resulta conveniente incorporar este parser a las etapas posteriores de la investigación o descartarlo.

# Documentos Utilizados

Estoy usando 4 documentos generados sintéticamente, que se encuentran el el corpus original. Estos son: "pdf_01_idioma.pdf", "pdf_02_codigo.pdf", "pdf_03_matematica.pdf" y "pdf_04_layout.pdf". 

# Herramientas 

El parser que estoy utilizando es OpenDataloader. 

# Código Utilizado

Uso la versión del código del commit 4 del repositorio https://github.com/IgnacioCiminari/rag-pipeline.git, levantando el compose en ./parsers/engines/opendataloader-pdf/ y luego ejecutando ```uv run ./codigo/main.py``` en Windows con las dependencias del pyproject.toml del mismo repo. 

# Resultados Observados

Los resultados de la prueba se encuentran disponibles en ./codigo/prueba_formato_02.

A partir de las pruebas realizadas, se observaron los siguientes resultados:
- Símbolos especiales: OpenDataLoader maneja correctamente los símbolos especiales presentes en los documentos evaluados.
- Columnas: reconoce correctamente el contenido distribuido en múltiples columnas, preservando adecuadamente su estructura.
- Listas: reconoce el contenido de las listas, aunque no las representa de forma explícita como listas estructuradas.
- Tablas: reconoce las tablas y, en general, logra expresarlas correctamente. Sin embargo, presenta dificultades al procesar tablas implícitas que no cuentan con una indentación correcta en el documento.
- Fórmulas: detecta correctamente las fórmulas presentes en los documentos, aunque su representación en la salida obtenida presenta importantes diferencias respecto de la fórmula original.
- Código: no reconoce explícitamente los bloques de código ni conserva adecuadamente su formato, por lo que el contenido es interpretado y presentado principalmente como texto.
- Tipografía: el resultado del parseo puede verse afectado por el tipo de fuente utilizado en el documento PDF, generando diferencias en el reconocimiento del contenido.

# Decisiones

Se decide mantener OpenDataLoader como una alternativa válida para las siguientes etapas de la investigación.

La principal razón es que presenta características que no se encontraban adecuadamente resueltas por los otros parsers evaluados. En particular, permite reconocer correctamente el contenido distribuido en múltiples columnas y detectar fórmulas dentro de los documentos.

Si bien la representación de las fórmulas obtenidas no es adecuada, su correcta detección permite considerar la posibilidad de realizar un procesamiento específico posterior sobre este tipo de contenido. De esta manera, el parser podría utilizarse como etapa inicial de reconocimiento y extracción, complementándolo posteriormente con mecanismos específicos para mejorar la representación de determinados elementos.

# Próximo Paso

Se considera conveniente evaluar la fidelidad con la que el MarkItDown modificado reconoce y preserva bloques de código.

En particular, se buscará determinar si la correcta preservación de la indentación permite obtener una representación suficientemente fiel del código original como para utilizarla como base para un procesamiento posterior. En una prueba anterior, el parser no logró leer correctamente el código presente en uno de los documentos PDF, por lo que será necesario repetir la prueba con documentos adecuados y determinar las posibles causas de este comportamiento.

Además, se realizarán pruebas adicionales sobre el reconocimiento y representación de tablas utilizando otros documentos PDF que contengan diferentes tipos de tablas. Esto permitirá determinar si los resultados positivos observados con anterioridad corresponden a un mérito del parser o fueron una anomalía que se presentó particularmente en las tablas que se presentaron.