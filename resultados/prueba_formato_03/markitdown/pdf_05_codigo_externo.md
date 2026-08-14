### ECMAScript 6 y la palabra resevada class

Ahora con la sintaxis de ECMAScript (ES6), se puede usar la palabra class para definir un tipo de objeto. Esta sintaxis implicitamente define objetos por medio de funciones constructoras, ya que el concepto de clases no existe en JS y la creación de objetos se termina haciendo a través de prototype. Lo que realmente nos facilita ES6 es una sintaxis amigable conocida como syntactic sugar o lenguaje más dulce para los programadores.

Ejemplo en archivo objetos-es6.js

class Persona {

constructor(nombre, correo, profesion, fechaNacimiento) { this.nombre = nombre;

this.correo = correo;

this.profesion = profesion;

this.fechaNacimiento = fechaNacimiento;

}

saludar() {

console.log('Hola soy ' + this.nombre);

}

edad() {

const hoy = new Date();

return hoy.getFullYear() - this.fechaNacimiento.getFullYear(); }

}

nodejs js/objetos-es6.js #ver ejemplo con es6

Una de las cosas nuevas que aporta ES6 es que al declarar tipos de objetos si o si, es necesario instanciarlos con la palabra reservada new sino lanza un error:

const maria = Persona('María', 'maria@gmail.com', 'Ingeniero en Sistemas de Información', new Date(2012, 9, 1));

// lanza el error: TypeError: Class constructor Persona cannot be invoked without 'new'

nodejs js/objetos-es6.js #Ver Inicialización de objetos sin new

Ademas algunas características de sintaxis y semantica de ES6 no son compartidas con es5. Por ello es importante tener en cuenta tanto las versiones de los lenguajes como los estándares.