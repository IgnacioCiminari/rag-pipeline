## PDF 2: Código de Programación

A continuación se presentan snippets de código en múltiples lenguajes para

probar la retención de indentación y símbolos.

## Snippet en Python

# -*- coding: utf-8 -*-

I 1I II

Python: lo raro acá no es un simbolo, es la AUSENCIA de simbolos.

No hay { } que delimiten bloques - la identacion ES la sintaxis.

Ademas, Python permite identificadores con caracteres unicode (itildes

incluidas!).

II 1I II

from dataclasses import dataclass

@dataclass

class Jugador:

nombre: str

# ← identificador normal, pero string con tilde

pais: str

dorsal: int

def clasificacion(jugadores: list[Jugador]） -> dict[str, int]:

tabla = {}

for j in jugadores:

# el for no lleva llaves, ni fin,

ni end

if j.pais not in tabla:

# el bloque se define por la

indentacion

tabla[j.pais] = 0

tabla[j.pais] += j.dorsal

return tabla

# Un poco de azucar sintáctica: list comprehension + walrus operator (:=)

def resumen(jugadores: list[Jugador]) -> str:

if (n := len(jugadores)) == 0:

return "sin jugadores "

nombres = [j.nombre for j in jugadores if j.dorsal < 10]

return f"{n} jugadores, {len(nombres)} con dorsal < 10 → {nombres}"

iff _name_ == "_main__":

equipo = [

Jugador("Nono Fernandez", "Argentina", 9),

Jugador("Francois Dupont", "France", 7),

Jugador("Bjorn Muller", "Deutschland", 4),

print(clasificacion(equipo))

print(resumen(equipo))

## Snippet en Smalltalk

dobles."Smalltalk: lo raro acá es que ToDo, absolutamente todo, es un objetoLos simbolos (#simbolo) y los caracteres especiales ($n, $e) son ciudadanosy toda accion es enviar un mensaje a un objeto. No hay operadoresespeciales',hasta el '+' ées un mensaje binario. Los comentarios van entre comillas
deObject subclass: #JugadorJugador class >> nombre: unNombre pais: unPais dorsal: unDorsal [1.Jugador >> setNombre: unNombre pais: unPais dorsal: unDorsal [primera clase."j := self new.package: 'Mundial'.j setNombre: unNombre pais: unPais dorsal: unDorsal.nombre := unNombre.pais := unPais.instanceVariableNames: 'nombre pais dorsal'classVariableNames:Ijl1
1.dorsal := unDorsal.
Jugador >> saludar [
Transcript showCr: nombre, ′(#', dorsal printString, ')-'， pais,
"Mensaje unario: se envia sin argumentos, con un simple punto y aparte"
ivamos quipo!'.
"Envio de mensajes en cascada (;), caracteristica muy propia de Smalltalk"
equipo := OrderedCollection new.」equipo 丨
equipoequipo do: [ :cadaJugador I cadaJugador saludar ].yourself.add:add: (Jugador nombre: 'Asa Lofgren' pais: 'Sverige' dorsal: 8);(Jugador nombre: 'Nandu Pérez' pais: 'Argentina' dorsal: 10);

## Snippet en Prolog

% Prolog: lo raro acá es que no "programás" pasos, declarás HECHoS y REGLAS,

% y es el motor de inferencia (unificacion + backtracking) el que "resuelve"

% ias preguntas por vos. No hay asignacion de variables tradicional.

% Los átomos con tildes/n hay que encerrarlos entre comillas simples.

% --- Hechos ---

jugador('Nono Fernández',

'argentina', 9) .

jugador('Francois Dupont', 'francia', 7).

jugador('Bjorn Muller', 'alemania', 4).

jugador('Asa Lofgren', 'suecia', 8).

campe6n('argentina'， 2022).

campe6n('francia', 2018).

campe6n('alemania', 2014) .

% --- Regla: un jugador es "campeon vigente" si su pais gano el último

mundial ---

% El operador ':-' se lee "si". La coma es "y". Todo termina en punto.

campeon_vigente(Jugador) :-

jugador(Jugador, Pais, _),

campeon(Pais, Ano),

Ano >= 2022.

% --- Regla recursiva clásica: icuantos jugadores hay en la lista? ---

cantidad([l, 0).



cantidad([_|Resto], N) :-

cantidad(Resto, No),

N is No + l.

% Consultas de ejemplo (se tipearian en el intérprete):

% ?- campeon_vigente(X) .

X = 'Nono Fernandez':

%

% ?- jugador(Nombre, 'francia', Dorsal).

Nombre = 'Francois Dupont', Dorsal = 7.

% 

## Snippet en Haskell

Haskell: lo raro acá es que es puro (sin efectos secundarios ocultos),

 perezoso (una lista puede ser infinita y no pasa nada) y fuertemente

tipado

con inferencia de tipos. Con {-# LANGUAGE UnicodeSyntax #-} hasta se puede

escribir 入 en vez de "\" y → en vez de "->".

{-# LANGUAGE UnicodeSyntaX #-}

module Mundial where

data Jugador = Jugador

{ nombre :: String

，pais、::String

dorsal :: Int

} deriving (Show, Eq)

 Pattern matching en la definicion de la funcion, sin ifs explicitos

esTitular :: Jugador → Bool

esTitular j

| dorsal j <= ll = True

= False

| otherwise

 Lambda con sintaxis unicode (入 y →) en vez de \ y ->

dorsales :: [Jugador] → [Int]

dorsales = map (入j → dorsal j)

-- Lista infinita de fibonacci, gracias a la evaluacion perezosa -

- esto en un lenguaje "estricto" jamas terminaria de construirse

fibonacci :: [Integer]

fibonacci = θ : l : zipWith (+） fibonacci (tail fibonacci)

main : I0 ()

main = do

let equipo =

[ Jugador "Nono Fernandez""Argentina" g

Jugador "Francois Dupont" "France"

7

8

Jugador "Asa Lofgren"

"Sverige"

1

putStrLn $ "Titulares → " ++ show (filter esTitular equipo)

→ " ++ show (dorsales equipo)

putStrLn $ "Dorsales 

putStrLn $ "Fibonacci (10) →" ++ show (take i0 fibonacci)

## Snippet en Marcado

<!DOCTYPE html>
<!-
HTML: lo raro acá es que No es un lenguaje de programaci6n (no hay l6gica,
no hay variables) sino de MARcADo: describe estructura, no comportamiento.
Además usaa "entidades" (&ntilde; &eacute; &euro;） para representar
caracteres
especiales cuando la codificaci6n no está garantizada.
>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Selecci&oacute;n &ntilde;andufuerte</title>
</head>
<body>
<header>
<h1>Plantel Mundialista &euro;2026</h1>
</header>
<main>
<section id="jugadores">
<ul>
<li data-dorsal="9">&Ntilde;o&ntilde;o Fern&aacute;ndez - Argentina</
li>
<li data-dorsal="7">Fran&ccedil;ois Dupont - France</li>
<li data-dorsal="8">&Aring;sa L&ouml;fgren - Sverige</li>
</ul>
</section>
</main>
<footer>
&lt;div&gt;.</p><p>&copy; 2026 - Hecho con cari&ntilde;0 y demasiadas etiquetas
</footer>
</body>
</html>

## Snippet en Estilos

/*

CSS: tampoco es un lenguaje de programacion clasico - no hay funciones

propias (aunque calc() y las custom properties se le acercan) y su l6gica

central es LA CASCADA y LA ESPECIFICIDAD: quién le "gana" a quién.

El pseudo-elemento ::before puede inyectar contenido, incluso con

caracteres especiales, directo en el css con content: ".",

* /

:root {

- -color-argentina: #75AADB;

--color-francia: #0055A4;

- -color-alemania: #FFCE00;

}

 jugador {

font-family: "Segoe UI", sans-serif;

padding: 0.5rem 1rem;

border-left: 4px solid var(--color-argentina);

}

. jugador[data-pais="Sverige"] {

border-left-color: #006AA7;

了

. jugador::before {

content: "★ ";

/* carácter especial directo en el css */

了



.jugador::after {

content: " - ivamos!";

 /* signos de apertura/cierre espanoles, sin drama

*/

}

@media (max-width: 600px） {

.jugador {

font-size: 0.9rem;

}

## Snippet en Componente

// JS/JSX: lo raro acá es que JSX mezcla HTML *dentro* del propio c6digo JS

// (no es valido JS puro, necesita un compilador tipo Babel) y que JS tiene

// azucar sintactica rarisima: destructuring, template literals con ^${}`,

I/ spread operator (...), y optional chaining (?.).

import { useState } from "react";

const jugadores = [

{ nombre: "Nono Fernández", pais: "Argentina", dorsal: 9 },

{nombre: "Francois Dupont", pais: "France", dorsal: 7 },

{ nombre: "Asa Lofgren", pais: "Sverige", dorsal: 8 },

1;

// Destructuring + template literal con interpolacion ${...}

const presentar = ({ nombre, pais， dorsal }） =>

#${dorsal} → ${nombre} （${pais}） ;

export default function Plantel() {

const [seleccionado, setSeleccionado] = useState(null);

return （

<section className="plantel">

<h2>Seleccion Nandu Fuerte</h2>

<ul>

{jugadores.map((j） =>（

<li

key={j.dorsal}

onClick={() => setSeleccionado(j)}

V

{presentar(j)}

</li>

))}

</ul>

{seleccionado?.nombre && （

<p>Elegiste a: {seleccionado.nombre} - iqué crack! </p>

)}

</section>

):

}

## Snippet en Jugador

// Java: lo raro acá es lo VERBoso que es todo - no existe una sola linea

// suelta de codigo, ToDo tiene que vivir dentro de una clase, hasta el

// método main(). Ademas es fuertemente tipado y compilado (no interpretado

// como Python), asi que muchos errores se detectan antes de correr nada.

import java.util.List;

import java.util.stream.Collectors;

public class Jugador {

private final String nombre;

private final String pais;

// los identificadores unicode están

permitidos

private final int dorsal;

public Jugador(String nombre, String pais, int dorsal) {

this.nombre = nombre;

this.pais = pais;

this.dorsal = dorsal;

}

public String presentar() {

return String.format("#%d → %s (%s) - icrack total!", dorsal, nombre,

pais);

}

public static void main(String[] args) {

List<Jugador> equipo = List.of(

 new Jugador("Nono Fernandez",

"Argentina", 9),

new Jugador("Francois Dupont"， "France", 7),

new Jugador("Asa Lofgren", "Sverige", 8)

);

// Streams + lambdas: la parte "moderna" y menos verbosa de Java

String resumen = equipo.stream()

.filter(j -> j.dorsal < 10)

.map(Jugador: :presentar)

.collect(Collectors.joining("\n"));

System.out.println(resumen) ;

## Snippet en Mundial

// Go: lo raro acá es la concurrencia integrada en el propio lenguaje:

// goroutines (go func()) y channels para comunicarlas, sin necesidad de

// librerias externas. Además, las funciones pueden devolver MULTIPLES

// valores a la vez (muy poco comun en otros lenguajes de esta lista),

// y el manejo de errores es explicito (if err != nil), no con try/catch.

package main

import "fmt"

type Jugador struct {

Nombre string

Pais

string // identificador unicode permitido también en Go

Dorsal int

// Retorno múltiple: valor + error, patron idiomatico de Go

func buscarPorDorsal(equipo []Jugador, dorsal int) (Jugador, error) {

for _, j := range equipo {

if j.Dorsal == dorsal {

return j, nil

}

return Jugador{}, fmt.Errorf("no se encontr6 jugador con dorsal %d",

dorsal)

了

func saludar(j Jugador, canal chan string) {

canal <- fmt.Sprintf("iVamos %s! #%d - %s ", j.Pais, j.Dorsal,

j .Nombre)

了

func main() {

equipo := []Jugador{

{"Nono Fernandez", "Argentina", 9},

{"Francois Dupont", "France", 7},

{"Asa Lofgren", "Sverige", 8},

}

canal := make(chan string, len(equipo))

// Se lanzan goroutines concurrentes, cada una manda su saludo al

channel

for_,j := range equipo {

go saludar(j, canal)

}

for range equipo {

fmt.Println(<-canal)

}

if jugador, err := buscarPorDorsal(equipo, 7); err == nil {

fmt.Println("Encontrado:", jugador.Nombre)

}

## Snippet en Mundial

// C#: lo raro acá, comparado con Java, es lo integrado que está LINQ

// (consultas estilo SQL directamente sobre colecciones) y las "propiedades"

// (get/set) que evitan escribir getters/setters manuales a lo Java.

// También permite interpolacion de strings con $"..." y unicode sin drama.

using System;

using System.Collections.Generic;

using System.Linq;

namespace Mundial

public class Jugador

public string Nombre { get; set; }

public string Pais { get; set; }

// propiedad auto-implementada

public int Dorsal { get; set; }

public string Presentar() => $"#{Dorsal} → {Nombre} ({Pais}) - ia

ganar!";

}

public class Program

public static void Main(string[] args)

3

var equipo = new List<Jugador>

S

new() { Nombre = "Nono Fernandez", Pais = "Argentina", Dorsal

= 9 },

new() { Nombre = "Francois Dupont", Pais = "France", Dorsal =

7},

new() { Nombre = "Asa Lofgren", Pais = "Sverige", Dorsal =

8},

// LINQ: consulta declarativa, muy parecida a SQL

var titulares = from j in equipo

where j.Dorsal <= 11

orderby j.Dorsal

select j.Presentar();

foreach (var linea in titulares)

Console.WriteLine(linea) ;

## Snippet en Mundial

// C++: lo raro acá, comparado con casi todos los anteriores, es que ExPoNE

// la memoria: punteros, referencias, gesti6n manual (o semi-manual con

// smart pointers). Ademas permite templates (genéricos "de verdad", con

// generaci6n de c6digo en tiempo de compilaci6n) y sobrecarga de operadores,

// algo que muy pocos lenguajes de esta lista permiten tan libremente.

#include <iostream>

#include <vector>

#include <string>

#include <memory>

struct Jugador {

std::string nombre;

std::string pais;

// si, los identificadores/strings unicode entran sin

drama 

int dorsal;

// Sobrecarga del operador << para poder hacer std::cout << jugador

friend std::ostream& operator<<(std::ostream& os, const Jugador& j)

os << "#" << j.dorsal << " →" << j.nombre << "（" << j.pais << "）

ivamos!";

return os;

}

// Template genérico: funciona para cualquier tipo comparable, no solo

Jugador

template

e<typename T>

T maximo(const std::vector<T>& valores, bool (*comparar)(const T&, const T&))

S

T mejor = valores.front();

for (const auto& v : valores) {

if (comparar(v, mejor)) mejor = v;

}

return mejor;

}

int main(） {

std::vector<Jugador> equipo = {

{"Nono Fernandez", ""Argentina", 9},

{"Francois Dupont"， "France", 7},

{"Asa Lofgren", "Sverige", 8},

// std::unique_ptr: gesti6n de memoria "moderna", sin new/delete manual

expuesto

auto capitán = std::make_unique<Jugador>(equipo.front());

for (const auto& jugador : equipo）{

std::cout << jugador << '\n';

}

std::cout << "Capitán elegido → " << *capitan << '\n';

return 0;

}

## Snippet en Sql

# SQL - el idioma que le habla a los datos

*Lo raro acá, comparado con los ll anteriores: SQL es **declarativo** -vos

decis

QUE querés, no coMo conseguirlo (no hay loops explicitos, el motor decide el

plan de ejecucion). Ademas mezcla varios "sub-lenguajes" en uno solo: DDL

(estructura), DML (datos) y DCL/TCL (permisos/transacciones). Acá van DDL,

DML completo (INSERT/UPDATE/DELETE)， un SELECT con JOIN + subconsulta +

agregacion, y un TRIGGER.*

## 1. DDL - Creacion de la estructura

sgl

DDL: Data Definition Language. Define la "forma" de los datos,

no los datos en si. CREATE, ALTER, DROP viven acá.

CREATE TABLE pais（

id_pais

SERIAL PRIMARY KEY,

VARCHAR(6O) NOT NULL,

 admite tildes/n sin drama si la

nombre

DB usa UTF-8

confederaci6n VARCHAR(2O) NOT NULL,

BOOLEAN DEFAULT FALSE

campeon

)；

CREATE TABLE jugador(

id_jugador

SERIAL PRIMARY KEY,

nomb re

VARCHAR(8O) NOT NULL,

dorsal

SMALLINT CHECK (dorSal BETWEEN 1 AND 99),

id_pais

INTEGER NOT NULL REFERENCES pais(id_pais) ON DELETE CASCADE,

goles

INTEGER DEFAULT 0,

aCtualizado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

Indice extra sobre la columna de busqueda mas frecuente

CREATE INDEX idx_jugador_pais ON jugador(id_pais);

## 2. INSERT - Alta de datos

`sql

 INSERT: puede cargar una fila o varias en un solo statement (multi-row

insert)

INSERT INTO pais (nombre, confederaci6n, campeon) VALUES

('Argentina',

'CONMEBOL'，

TRUE),

TRUE),- ojo: nombre con la grafia original,

('Franca'

'UEFA',

con cedilla

('Deutschland',

'UEFA',

TRUE),

'UEFA',

FALSE);

('Sverige',

INSERT INTo jugador (nombre, dorsal, id_pais, goles） VALUES

('Nono Fernández'， 9， (SELECT id_pais FROM pais WHERE nombre =

'Argentina'), 12),

('Francois Dupont', 7, (SELECT id_pais FROM pais WHERE nombre =

8),

Franca'),

('Bjorn Muller',

4, (SELECT id_pais FROM pais WHERE nombre =

'Deutschland'), 3),

('Asa Lofgren' ,

8, (SELECT id_pais FROM pais WHERE nombre =

'Sverige'),

5);

## 3. UPDATE - Modificacion de datos existentes

sal

-- UPDATE siempre con WHERE, si no querés actualizar la tabla entera

-- (clásico accidente de un DBA a las 3 de la manana).

UPDATE jugador

SET goles = goles + 1,

actualizado_en = CURRENT_TIMESTAMP

WHERE nombre = Nono Fernandez';

UPDATE masivo pero controlado, con subconsulta correlacionada

UPDATE pais

SET campeon = TRUE

WHERE id_pais IN (

SELECT id_pais FROM jugador

GROUP BY id_pais

HAVING SUM(goles) > 10

)

## 4. DELETE - Baja de datos

sal

DELETE también necesita WHERE por la misma razon que UPDATE.

Como_ jugador tiene ON DELETE CASCADE hacia pais, borrar un pais

-- se lleva puestos a sus jugadores automaticamente.

DELETE FROM jugador

WHERE goles = θ AND dorsal > 20;

-- Ejemplo de baja en cascada (comentado a proposito, para no volar todo

Suecia):

-- DELETE FROM pais WHERE nombre = 'Sverige';

## 5. SELECT completo - JoIN + subconsulta + agregaci6n

`sgl

Trae, por pais, el goleador con mas goles, pero solo de paises campeones,

-- y solo si el equipo entero super6 los 10 goles en total (HAVING).

SELECT

AS pais,

p.nombre

AS goleador,

j.nombre

j.goles,

(SELECT COUNT(*)

FROM jugador j2

 AS cantidad_jugadores

WHERE j2.id_pais = p.id_pais)

FROM pais p

JOIN jugador j ON j.id_pais = p.id_pais

WHERE p. campeOn = TRUE

AND j.goles = （

SELECT MAX(j3.goles)

FROM jugador j3

WHERE j3.id_pais = p.id_pais

GROUP BY p.nombre, j.nombre, j.goles, p.id_pais

HAVING SUM(j.goles） OVER (PARTITION BY p.id_pais) > 10

ORDER BY j.goles DESC;

## 6. TRIGGER - Efecto automatico ante un evento

、`sgl 

TRIGGER: codigo que la propia base de datos ejecuta sola,

sin que ninguna aplicacion se lo pida explicitamente.

Acá, cada vez que se actualiza el dorsal de un jugador,

 se registra el cambio en una tabla de auditoria.

CREATE TABLE auditoria_dorsal (

id_auditoria SERIAL PRIMARY KEY,

id_jugador  INTEGER NOT NULL,

dorsal_viejo SMALLINT,

dorsal_nuevo SMALLINT,

modificado_en TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)；

CREATE OR REPLACE FUNCTIoN registrar_cambio_dorsal()

RETURNS TRIGGER AS $$

BEGIN

IF OLD.dorsal IS DISTINCT FROM NEW.dorSal THEN

INSERT INTo auditoria_dorsal (id_jugador, dorsal_viejo, dorsal_nuevo)

VALUES (OLD.id_jugador, OLD.dorsal, NEW.dorsal);

END IF;

RETURN NEW;

END ;

$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_auditar_dorsal

AFTER UPDATE OF dorsal ON jugador

FOR EACH ROW

EXECUTE FUNCTIoN registrar_cambio_dorsal();

 Con esto activo, algo tan simple como esto ya queda auditado solo:

-- UPDATE jugador SET dorsal = li WHERE nombre = 'Asa Lofgren';

### Nota sobre caracteres especiales

Se usaron tildes, n y c_directamente en nombres e identificadores (^pais`,

auditoria_dorsal`,^goleon`... perdon,^goleador`), algo que la mayoria de

los motores modernos (PostgreSQL, MySQL 8 con ^utf8mb4^） toleran sin drama

siempre que la codificaci6n de la base esté bien configurada - cosa que en

la vida real rara vez es gratis.

