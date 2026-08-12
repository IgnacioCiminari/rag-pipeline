## PDF 3: Símbolos Matemáticos y Listas

## Referencia rápida —Matemática por materia

## 1. Cálculo 1 —Derivadas

## Conceptos clave

•Definición de derivada como límite

•Reglas básicas: potencia, producto, cociente

•Regla de la cadena (composición de funciones)

•Derivadas de funciones trascendentes (trig, exp, log)

•Aplicaciones: máximos/mínimos, puntos de inflexión

## Fórmulas

Definición:

f(c+h)- f(x)

f'(x) = lim

h

h→0

Regla de la cadena:

d

[(g(x)]=F(g(x)）-g(x)

## 2. Cálculo 2 —Integrales

## Conceptos clave

•Integral definida como área /suma de Riemann

•Teorema fundamental del cálculo

•Técnicas: sustitución, por partes

•Integrales múltiples (dobles, triples)

•Cambio de variable (Jacobiano)

## Fórmulas

Integral doble con cambio de variable:

0(x, y)

f(x(u,v),y(u,v))

dudu

dA

(u,v)

Integral triple en coordenadas esféricas:

f(p, 0, Φ) p² sin Φ dp d0 dΦ

## 3. Cálculo 3 /Vibraciones —Ecuaciones diferenciales

## Conceptos clave

•EDO lineales de primer y segundo orden

•Homogéneas vs. no homogéneas

•Oscilador armónico amortiguado (subamortiguado, crítico, sobreamortiguado)

•Solución particular +solución general

•Condiciones iniciales /de contorno

## Fórmulas

EDO 2do orden general:

ay" + by'+ cy= f(t)

Oscilador amortiguado:

x(t) = e-t(Acos(wat) + Bsin(wat))

m + c + kc = 0

## 4. Álgebra Lineal —Matrices

## Conceptos clave

•Operaciones matriciales (suma, producto, transpuesta)

•Determinante y su interpretación geométrica

•Autovalores y autovectores

•Sistemas lineales (Gauss, Gauss-Jordan)

•Diagonalización

## Fórmulas

Ecuación característica (autovalores):

det(A - XI) = 0

Sistema lineal en forma matricial:

Ax = b

## 5. Fourier —Series y transformadas

## Conceptos clave

•Descomposición de señales periódicas en senos/cosenos

•Coeficientes de Fourier (ortogonalidad)

•Forma exponencial compleja

•Transformada de Fourier (paso de dominio tiempo a frecuencia)

•Aplicaciones: filtrado, análisis espectral

## Fórmulas

Serie de Fourier:

2πnt

f(t) = ao + )

+ bn sin

an cos

Transformada de Fourier:

iwtdt

F(w

## 6. Mecánica 1 —Ecuaciones vectoriales de movimiento

## Conceptos clave

•Posición, velocidad, aceleración como vectores

•Segunda ley de Newton en forma vectorial

•Movimiento relativo (marcos de referencia)

•Trabajo y energía (producto punto)

•Torque y momento angular (producto cruz)

## Fórmulas

Segunda ley de Newton:

d2r

ma=m-

F

dt2

Torque:

=F

## 7. Electromagnetismo —Operadores vectoriales

## Conceptos clave

•Gradiente (campo escalar →vector)

•Divergencia (fuentes/sumideros de un campo)

•Rotor (circulación de un campo)

•Ecuaciones de Maxwell en forma diferencial

•Teoremas de Gauss y Stokes (relación integral-diferencial)

## Fórmulas

Divergencia y rotor:

VxE=-

V·E=

at

E0

## Gradiente:

V=

(0c' 0y' 0z)

## 8. Probabilidad y Estadística

## Conceptos clave

•Variable aleatoria (discreta/continua)

•Función de distribución y densidad de probabilidad

•Esperanza (valor esperado)

•Varianza y desviación estándar

•Distribuciones notables (normal, binomial, Poisson)

## Fórmulas

Esperanza y varianza:

E[X]=

(x) dx

C;P(;)

Var(X) = E[x²] - (E[x])²

## Anexo —Lógica proposicional y grafos

## Lógica proposicional

## Conceptos clave

•Proposiciones y conectores (∧, ∨, ¬, →, ↔)

•Tablas de verdad

•Cuantificadores (∀, ∃)

•Equivalencias lógicas (De Morgan, contrapositiva)

•Inferencia (modus ponens, modus tollens)

## Tabla de verdad —Implicación (p →q)

Ip| q|p→q||------|------||V|V|V||V|F|F|| F|V|V||F|F|V]

## Grafos

## Conceptos clave

•Representación: matriz de adyacencia vs. lista de adyacencia

•Grafos dirigidos vs. no dirigidos, ponderados vs. no ponderados

•Recorridos: BFS (amplitud)y DFS (profundidad)

•Caminos mínimos: Dijkstra

•Complejidad (BFS/Dijkstra con cola de prioridad)

## Matriz de adyacencia (ejemplo)

/0 1 0 1

1 0 1 0 

A=

0 1 0 1 

[1 0 1 0 

## Pseudocódigo —BFS

```BFS(grafo, nodo_inicio): visitados ={nodo_inicio}cola =[nodo_inicio]

while cola no vacía: actual =cola.pop(0)procesar(actual)for vecino in grafo[actual]:

if vecino not in visitados: visitados.add(vecino)cola.append(vecino)```

## Pseudocódigo —Dijkstra

```Dijkstra(grafo, nodo_inicio): dist[nodo_inicio]=0 dist[otros]=infinito Q =

cola_prioridad(todos los nodos, key=dist)while Q no vacía: u =Q.extraer_min()for (v,

peso)in vecinos(u): if dist[u]+peso <dist[v]: dist[v]=dist[u]+peso Q.actualizar(v,

dist[v]）"

