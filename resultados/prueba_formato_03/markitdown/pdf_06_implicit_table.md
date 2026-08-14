Un volumen en Docker es una sección del sistema de archivos del host (o sistema de archivos anfitrión)
que se monta dentro del contenedor. Esta estrategia permite que los datos sobrevivan al ciclo de vida del
contenedor, habilita el intercambio de archivos entre contenedores y mejora el rendimiento en ciertos
entornos.
### Fundamento Conceptual
Cuando creamos un contenedor, por ejemplo con  , si ese contenedor genera archivos en su
docker run
sistema de archivos interno, dichos archivos vivirán dentro de su estructura UnionFS (el sistema de
archivos por capas). Sin embargo, esa información no estará disponible si el contenedor se elimina o si otro
contenedor requiere acceso a los mismos datos.
Comparativa: Volúmenes Docker vs Montajes NFS
Los volúmenes son la respuesta de los contenedores docker a lo que haríamos con NFS (Network File
System) si estuvieramos trabajando con equipos físicos o máquinas virtuales, la diferencia es que el
UnionFS al ser declarativo y convivir en el mismo quernel lo vuelve natural.
Además nada impide que las estrategias de Docker se complementen con estrategias NFS para montar los
archivos reales en un Storage separado del SO anfitrión por ejemplo:
| Característica | Volúmenes Docker | Montajes NFS |
| -------------- | ---------------- | ------------ |
Requiere configuración externa y
| Creación y gestión | Integrada con Docker CLI |     |
| ------------------ | ------------------------ | --- |
permisos
|     | Persisten tras eliminación del | Igual, si está correctamente |
| --- | ------------------------------ | ---------------------------- |
Persistencia
|     | contenedor                    | montado                          |
| --- | ----------------------------- | -------------------------------- |
|     | Dentro del área de gestión de | Carpeta específica en el sistema |
Ubicación
|     | Docker                     | anfitrión                      |
| --- | -------------------------- | ------------------------------ |
|     | Fácil con Docker Compose y | Requiere montar manualmente en |
Portabilidad
|     | backups | cada host |
| --- | ------- | --------- |
Rendimiento Rápido (local al host) Más lento por depender de red
| Acceso concurrente entre |     | Sí (diseñado para entornos |
| ------------------------ | --- | -------------------------- |
No (por defecto)
| hosts |     | distribuidos) |
| ----- | --- | ------------- |
Depende de permisos de sistema y
| Seguridad | Controlada por Docker |     |
| --------- | --------------------- | --- |
red
| Requiere configuración |     | Sí (exports, permisos, montaje en |
| ---------------------- | --- | --------------------------------- |
No
| extra? |     | cada host) |
| ------ | --- | ---------- |
Clústeres o entornos multi-host
| Ideal para... | Apps en un solo host con Docker |     |
| ------------- | ------------------------------- | --- |
compartidos
Los volúmenes permiten salvar esa barrera, al montar directorios del sistema anfitrión en puntos
específicos del sistema de archivos del contenedor.
Esto los hace imprescindibles para: