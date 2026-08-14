# EXP-003 - Prueba Exhaustiva de Tablas para el Parser MarkItDown

Fecha: 14-08-2026

# Pregunta o Decisión que se Quiere Investigar

En experimentos anteriores se observó que MarkItDown modificado obtiene muy buenos resultados al procesar tablas y que, en general, genera documentos Markdown con una buena estructura e indentación. Sin embargo, en una prueba anterior no logró procesar correctamente un documento que contenía código, aunque esto podría estar relacionado con el formato particular del archivo utilizado.

Por este motivo, se busca determinar qué tan bien se comporta el parser al procesar código y verificar si los buenos resultados obtenidos anteriormente con tablas son consistentes o si estuvieron condicionados por las características particulares de los documentos utilizados.

En particular, interesa comprobar si MarkItDown modificado puede reconocer y representar correctamente código conservando su estructura e indentación, y si puede procesar correctamente tablas que contienen múltiples líneas dentro de una misma celda.

# Objetivos de Esta Actividad

Determinar qué tan bien MarkItDown modificado procesa y representa código y tablas.

Se busca, por un lado, evaluar si el parser es capaz de reconocer correctamente bloques de código y conservar su indentación y estructura. Por otro lado, se pretende comprobar si los buenos resultados obtenidos previamente con tablas son reproducibles utilizando documentos con estructuras de tabla más variadas.

El objetivo final es determinar si MarkItDown modificado continúa siendo la herramienta con mejores resultados entre las alternativas evaluadas hasta el momento para detectar y representar tablas, y establecer sus capacidades y limitaciones al procesar código.

# Contexto y Motivación

Esta prueba surge a partir de dos observaciones realizadas en experimentos anteriores.

En primer lugar, las tablas procesadas por MarkItDown modificado en la prueba anterior fueron representadas correctamente. Sin embargo, existe la posibilidad de que estos resultados hayan estado sesgados por las características de los documentos utilizados, ya que las tablas evaluadas tenían una estructura relativamente simple.

En segundo lugar, en una de las pruebas anteriores se utilizó un documento que contenía código, pero el parser no logró procesarlo correctamente. Esto impidió determinar si MarkItDown modificado tiene dificultades para procesar código o si el problema estuvo relacionado específicamente con el formato del archivo utilizado.

Por lo tanto, esta actividad busca aislar ambas cuestiones mediante documentos diseñados para evaluar específicamente el procesamiento de código y de diferentes estructuras de tablas.

# Documentos Utilizados

Se utilizaron tres documentos pertenecientes al corpus versionado, correspondientes a documentos utilizados habitualmente durante el cursado de la carrera de Ingeniería en Sistemas de Información de la UTN FRC:

* `LED-2025-comisiones dias horarios.pdf`
* `pdf_05_codigo_externo.pdf`
* `pdf_06_implicit_table.pdf`

Estos documentos permiten evaluar tanto el procesamiento de código como diferentes tipos de estructuras tabulares.

## Herramientas

El parser utilizado en esta prueba es **MarkItDown modificado**.

# Código Utilizado

Se utilizó la versión correspondiente al commit 6 del repositorio `rag-pipeline`.

La ejecución se realizó en Windows mediante:

```bash
uv run ./codigo/main.py
```

utilizando las dependencias especificadas en el `pyproject.toml` del repositorio.

# Resultados Observados

El código fue reconocido y procesado correctamente. Sin embargo, el parser no conservó la indentación original. Si bien esto no representa un problema importante en el documento evaluado, ya que el código corresponde a JavaScript, podría resultar problemático al procesar lenguajes en los que la indentación forma parte de la estructura del programa, como Python, donde reconstruir correctamente el código a partir del Markdown generado podría ser considerablemente más difícil.

En cuanto a las tablas, los resultados fueron diferentes entre los documentos evaluados. Una de las tablas fue reconocida y representada correctamente, tal como se esperaba. Sin embargo, la otra tabla fue procesada incorrectamente y su estructura se perdió.

Al analizar la causa de este comportamiento, se observó que las pruebas anteriores estaban parcialmente sesgadas: las tablas utilizadas anteriormente tenían una sola línea de contenido en todas sus celdas. La nueva tabla, en cambio, contenía celdas con dos o tres líneas de contenido junto con otras que tenían una sola línea. Esta diferencia permitió identificar una limitación del parser en el procesamiento de tablas con distinta cantidad de líneas dentro de las celdas de una misma fila.

Por lo tanto, los buenos resultados obtenidos en las pruebas anteriores no eran completamente representativos de la capacidad general del parser para procesar tablas, sino que estaban condicionados por la estructura particular de las tablas utilizadas.

# Decisiones

Por el momento, se decide continuar trabajando con MarkItDown modificado, ya que los resultados obtenidos siguen siendo prometedores, especialmente en el reconocimiento general de tablas.

La próxima modificación estará orientada a mejorar el reconocimiento de tablas con celdas de múltiples líneas, de manera que varias líneas pertenecientes a una misma celda sean interpretadas como un único bloque de contenido y no como filas o elementos independientes.

Además, se detectó que el parser actualmente solo reconoce tablas que poseen al menos tres columnas, por lo que esta limitación también deberá ser considerada en futuras modificaciones.

# Próximo Paso

Modificar MarkItDown modificado para mejorar el reconocimiento de tablas en las que distintas celdas de una misma fila contienen diferentes cantidades de líneas.

Para evaluar sistemáticamente este comportamiento, se utilizará la convención de música de piano propuesta para clasificar las diferentes combinaciones de cantidad de líneas por celda:

* `1v1`
* `2v1`
* `3v1`
* `3v2`
* `4v1`
* `4v3`

El objetivo será utilizar estas combinaciones como casos de prueba controlados para determinar exactamente qué estructuras de tabla puede reconocer correctamente el parser y cuáles requieren modificaciones adicionales.
