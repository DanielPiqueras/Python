#1 Import
import antigravity

#2 Print
print("Hola mundo!")

#3 Comentarios
def func():
    """Esto es un docstring"""
    pass

#4 Bloques de código
if condition:
    #Si la condición es cierta
    call_to_some_complicated_stuff()

#Fuera del condicional
do_always_the_same_stuff()

#5 Inputs
answer = input("¿Cuál es la respuesta a la vida, el universo y todo lo demás?") 

#6 Excepciones
try:
    function_raises_exception()
except Exception:
    handle_exception()

#7 Operadores
"""
Operación	Resultado
x and y	si x es False entonces x, si no, y
x or y	si x es True entonces x, si no, y
not x	si x es False entonces True, si no, False
"""

#Operadores Aritméticos
"""
Símbolo	Operación
+	suma
-	resta
/	división
//	división entera
*	producto
**	potencia
%	módulo
"""

#Operadores de Comparación
"""
Símbolo	Operación
<	menor que
>	mayor que
<=	menor o igual que
>=	mayor o igual que
==	igual a
"""

#8 Variables
#Las variables no se definen, se se les asigna un valor usando el operador =.

#9 Cadenas de texto
"""
Se considera una cadena de texto cualquier sucesión de caracteres entre comillas dobles, ", o comillas simples, '.
Se puede usar \ para escapar las comillas.
Se considera que una cadena es una secuencia, de caracteres, y por tanto se puede acceder a un caracter usando su índice, aunque es un tipo de datos inmutable, por lo que no puede ser modificado de esta forma.
"""

#10 Operacines sobre cadenas de texto
"""
str.capitalize()

Devuelve una copia de la cadena con la primera letra en mayúscula y el resto en minúscula.

str.count(sub[, start[, end]])

Cuenta el número de veces que sub se encuentra en la cadena, desde start a end.

str.endswith(suffix[, start[, end]])

Devuelve si la cadena de texto termina con suffix.

str.isalnum()

Comprueba si la cadena de texto es alfanumérica.

Slide Type
str.isalpha()

Comprueba si la cadena de texto sólo tiene caracteres alfabéticos.

str.isdecimal()

Comprueba que todos los dígitos son decimales.

str.join(iterable)

Devuelve una cadena que es la concatenación de las cadenas en iterable usando la propia cadena como separador.

str.lower()

Devuelve una copia de la cadena con todos los caracteres en minúsculas.

str.replace(old, new)

Devuelve una copa de la cadena de texto reemplazando new por old.

Slide Type
str.split(sep=None, maxsplit=-1)

Devuelve una lista resultado de dividir la cadena usando sep como separador.

str.splitlines([keepends])

Devuelve una lista resultado de dividir la cadena usando saltos de línea como separadores.

str.startswith(prefix[, start[, end]])

Devuelve si la cadena de texto empieza con prefix.

Slide Type
str.strip([chars])

Devuelve una copia de la cadena eliminando del principio y del final los caracteres indicados en char. Si no se indican, se eliminan los espacios en blanco.

str.upper()

Devuelve una copia de la cadena con todos los caracteres en mayúsculas.
"""

#11 Raw Strings
#Los caracteres especiales, como saltos de línea, tabulaciones, etc. se introducen de la forma habitual, \n, \t. Pero, si no se quiere que se tengan en cuenta, se puede usar una raw string, añadiendo r delante de las comillas iniciales.

#12 String multilíneas
#Podemo crear una cadena de texto que tenga más de una líena. Para ello, se declara el literal usando las triples comillas.

#13 Format Strings
"""
Para mostrar valores de variables en cadenas de texto podemos usar format strings. Estas se pueden definir usando f como prefijo del literal de cadena de texto o usando el método format.

Las variables se sustituirán en los lugares que se indiquen entre llaves, {}.
"""

#14 Concatenación de Cadenas
#Las cadenas de texto se pueden concatenar usando el operador +, y se pueden repetir usando el operador *.

#15 Listas
"""
Una lista es una estructura de datos mutable compuesta por varios elementos que pueden ser de diferentes tipos. Se escribe con sus elementos separados por comas, y entre corchetes.

Ejemplos:
squares = [1, 4, 9, 16, 25]
squares = list("hola")
"""

#16 Métodos de Listas
"""
list.append(x)

Añade un elemento al final de la lista. Es equivalente a a[len(a):] = [x].

list.extend(iterable)

Extiende la lista añadiendo todos los elementos del argumento. Es equivalente a a[len(a):] = iterable.

list.insert(i, x)

Inserta un elemento en la posición indicada. El primer argumento es el índice del elemento antes del cual se va a insertar, por lo tanto a.insert(0, x) inserta en principio de la lista, y a.insert(len(a), x) es equivalente a a.append(x).

list.remove(x)

Elimina el primer elemento de lista cuyo valor sea x. Da un error si no existe el elemento.

list.pop([i])

Elimina el elemento en la posición dada y lo devuelve. Si no se especifica un índice, a.pop() elimina y devuelve el último elemento de la lista.

list.clear()

Elimina todos los elementos de la lista. Es equivalente a del a[:].

Slide Type
list.index(x[, start[, end]])

Devuelve el índice en la lista del primer elemento cuyo valor es x. Los argumentos opcionales start y end se usan para buscar solo en el segmento de la lista limitado por ellos, y en caso de usarlos, el índice devuelto es relativo a la lista entera, no al segmento.

list.count(x)

Devuelve el número de veces que x aparece en la lista

Slide Type
list.sort(key=None, reverse=False)

Ordena los elementos de la lista.

list.reverse()

Da la vuelta a la lista.

list.copy()

Devuelve una copia de la lista. Es equivalente a a[:].
"""

#17 Tuplas
"""
Las tuplas funcionan de la misma forma que las listas, pero son estructuras de datos inmutables, es decir, una vez declarada una tupla, no se puede modificar su contenido. Se declara separando los valores con comas.

Ejemplo:
squares = 1, 4, 9, 16, 25
empty = ()
one = 'lonely'
"""

#18 Sets
"""
Los sets funcionan como las listas, solo que ésta estructura de datos se asegura de que no hayan valores repetidos. El set es una colección de elementos no ordenada. Existen dos versiones de set, la mutable, set y la no mutable, frozenset.

Se crea usando las llaves, {}.

Ejemplos:

squares = {1, 4, 9, 16, 25}
print(squares)

squares.add(1)
print(squares)

squares.add(36)
print(squares)
"""

#Operaciones con Sets
"""
Estas operaciones son compatibles con los set y los frozenset.

isdisjoint(other)

Devuelve True si el set no tiene elementos en común con el otro.

issubset(other), set <= other, set < other

Comprueba si todos los elementos del set están en el otro. is, set <= other and set != other.

issuperset(other), set >= other, set > other

Comprueba si todos los elementos del otro están el set.

union(*others) , set | other | ...

Devuelve un nuevo set con los elementos del set y de los otros.

Slide Type
intersection(*others), set & other & ...

Devuelve un nuevo set con todos los elementos en común con el set y los otros.

difference(*others), set - other - ...

Devuelve un nuevo set con los elementos del set que no están en los otros.

symmetric_difference(other), set ^ other

Devuelve un nuevo set con los elementos que están en un set o en otro, pero no en los dos.

copy()

Devuelve una copia del set.

Slide Type
Las siguientes operaciones solo son compatibles con los set.

add(elem)

Añade un elemento.

remove(elem)

Borra el elemento, y da un error si no existe.

discard(elem)

Borra el elemento si existe.

pop()

Borra un elemento aleatorio del set, y da error si está vacío.

clear()

Borra los elementos de un set.
"""

#19 Diccionarios
"""
Los diccionarios son una estructura de datos mutable que permiten almacenar datos de una forma parecida a las listas, pero en vez de usar un número, el índice, para referenciar el dato, se puede usar prácticamente cualquier cosa. Es como una base de datos para guardar y organizar información.

Se pueden crear declarando una lista de elementos key: value separados por comas y rodeados de {}. También se puede usar dict() para crear el diccionario.

Ejemplos:

person = {'name': 'Antonio', 'age': 42}
print(person['name'])
"""

#Operaciones sobre Diccionarios
"""
d[key]

Accede al elemento con clave key del diccionario d. Lanza un error si key no existe en el diccionario.

d[key] = value

Guarda value en la clave key del diccionario d.

del d[key]

Borra d[key] del diccionario.

key in d

Comprueba si d tiene la clave key.

Slide Type
key not in d

Comprueba si d no tiene la clave key.

iter(d)

Devuelve un iterador sobre las claves del diccionario.

d.clear()

Borra todos los elementos del diccionario.

d.copy()

Copia el diccionario.

Slide Type
d.get(key[, default])

Devuelve el contenido de d[key] en caso de que key esté en el diccionario, y en caso contrario, devuelve el valor de default, o None si no se ha concretado.

d.items()

Devuelve una el diccionario como una lista de tuplas (key, value).

d.keys()

Devuelve una lista con las claves del diccionario.

pop(key[, default])

Si la clave está en el diccionario, la elimina y devuelve su valor, si no, devuelve el valor de defaul.

Slide Type
popitem()

Elimina y devuelve un elemento aleatorio (key, value) del diccionario.

setdefault(key[, default])

Si la clave está en el diccionario, devuelve el valor, si no, inserta en la clave el valor dado en default, o None si no se ha dado ningún valor.

update([other])

Actualiza el diccionario con las claves y valores del otro diccionario dado, sobreescribiendo las existentes.

values()

Devuelve una lista de los valores del diccionario.
"""

#20 Estructuras de Control, Condicionales, Bucles y Excepciones
#IF
"""
La instrucción para ejecutar bloques de forma condicional. Puede estar compuesta a su vez de cero o más partes de elif, que son las diferentes alternativas. En Python no hay instrucción switch como en otros lenguajes, y la sucesión de diferentes elif partes lo sustituyen.
"""

#FOR
"""
La instrucción para realizar bucles for es un poco diferente de otros lenguajes de programación. En vez de iterar sobre una progresión aritmética de números, dando al usuario la posibilidad de establecer el incremento en cada iteración, el bucle for de Python itera sobre los elementos de cualquier secuencia (lista o cadena de texto) en el orden que estos elementos aparecen en la secuencia.

La función range() permite generar secuencias de números. Se puede utilizar para iterar sobre los índices de una lista

La instrucción break, como en otros lenguajes, rompe la ejecución de la iteración más interna, mientras que continue pasa a la siguiente iteración del bucle.

En un bucle se puede definir la instrucción else, que se ejecutará siempre que el bucle termine sin que se salga usando una instrucción break

La instrucción pass no hace nada, y se usa para cuando necesitamos que un programa sea sintácticamente correcto pero no requiere ninguna acción.

while True:
    pass  # Espera infinita, hasta que se cancele la ejecución desde teclado (Ctrl + C)
"""

#21 Funciones, ciudadanos de primeer orden, declaración, funciones lambda
"""
Como hemos comentado en la introducción, todo en Python es un objeto, y también lo son las funciones.

Una función se define con la palabra reservada def seguida del nombre de la función que queremos crear, y poniendo a continuación, entre paréntesis, los argumentos de la función.

Las funciones son ciudadanos de primera clase, esto es que pueden ser tratadas como si fueran objetos, y ser pasadas por ejemplo, como argumentos de otras funciones. Se puede hacer referencia a la función con el nombre de esta, sin usar paréntesis.

Una función puede recibir cualquier número de argumentos, pudiendo definir valores por defecto.

Se pueden pasar argumentos a las funciones de dos formas:

Posicionalmente, donde cada valor pasado como argumento se asociará al argumento que esté en la misma posición en la declaración.
Por nombre, donde indicamos a que argumento se asocia cada valor, usando el operador de asignación =.

Podemos declarar una función que reciba un número de argumentos arbitrario. Para ello solo tenemos que poner como argumentos *args y **kwargs. En este caso, args contendrá en una tupla los argumentos pasados posicionalmente, mientras que kwargs contendrá en un diccionario todos los argumentos que se le han pasado por nombre.

Además de las funciones normales, Python nos permite declarar funciones anónimas, o funciones lambda, Para hacerlo, basta con untilizar la palabra reservada lambda.
"""



