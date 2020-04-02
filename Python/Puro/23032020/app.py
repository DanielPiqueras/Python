import winpty

# 1 Variables en Python

"""
print("Hola buenas tardes")
print('o----')
print(' |||| ')
print('Esto se multiplica' * 10)
"""

# 2 Ejercicio con Variables
"""
# Creamos una variable
name = 'John Smith'
years_old = 20
patient = True

# Para que nos muestre el nombre del paciente, su edad, y si el paciente es nuevo o no
if patient == True:
    print('El nombre del paciente es ' + name +
          ', tiene ' + str(years_old) + ' años y es un paciente nuevo.')
else:
    print('El nombre del paciente es ' + name +
          ', tiene ' + str(years_old) + ' años y no es nuevo en el hospital.')
"""

# 3 Input
"""
name = input('What is your name? ')
print('Hi ' + name)
"""

# 4 Ejercicio con Input
"""
# Creamos una variable
name = input('Introuduce el nombre del paciente: ')
years_old = input('Introduce la edad del paciente: ')
patient = input('Indica si es un paciente o no con "True" o "False": ')


# Para que nos muestre el nombre del paciente, su edad, y si el paciente es nuevo o no
def comprobar_paciente(variable, years_old, name):
    while variable != 'True' and variable != 'False':
        print('Error, vuelve a itroducir el tipo del paciente')
        variable = input('Indica si el paciente es nuevo o no: ')

    if variable == "True":
        print('El nombre del paciente es ' + name +
              ', tiene ' + str(years_old) + ' años y es un paciente nuevo.')
    elif variable == "False":
        print('El nombre del paciente es ' + name +
              ', tiene ' + str(years_old) + ' años y no es nuevo en el hospital.')

comprobar_paciente(patient, years_old, name)
"""

# 5 Ejercicio 2 con Input, conversión de variables
"""
pounds = input('Introduce tu peso en libras: ')
kilograms = round(int(pounds)/2.20462, 3)
print('Tu peso en kilos es: ' + str(kilograms))
"""

# 6 Comillas y cadenas de texto
"""
#Para poder usar las comillas simples
course = "Python´s for beginners"
print(course)

#Para poder poner algo con comillas dobles
course2 = 'Python for "Beginners"'
print(course2)

#Para mostrar un mensaje largo como un correo
long_message = '''
Hola buenas tardes, me llamo Dani.
Estoy tratando de trabajar lo mejor posible con Python para ver si en un futuro puedo hacer algo con esto

Un cordial saludo. Buenas noches.
'''
print(long_message)

#Para seleccionar solo un carácter o una palabra de una frase:
course3 = 'Primera letra, segunda letra'
#para seleccionar la primera letra
print(course3[0])
#para seleccionar la última letra
print(course3[-1])
#para seleccionar una palabra entera o más de un carácter a la vez:
#hay que tener en cuenta que el segundo valor es excluyente
print(course3[0:13])
#excluye el carácter de la posición asignada
print(course3[0:])
print(course3[1:])

#Al hacer por ejemplo
name = 'Jeniffer'
print(name[1:-1]) #nos mostraría todos los caractéres que se encuentran desde la posicion 1 hasta el final, excluyendo el último caracter por el -1
"""

# 7 Formatted Strings
"""
first = 'John'
last = 'Smith'
#Es una forma mucho más cómoda y profesional de concatenar cadenas de texto
#LA F DEL PRINCIPIO ES NECESARIA, OJO!!!!
message = f'{first} [{last}] is a coder'
print(message)
"""

# 8 String Methods
"""
#Cuenta el número de caractéres que hay en una cadena de texto
course = 'Python for Beginners'
print(len(course))

#Para transformar una cadena de texto en minúscula
print(course.upper())
#OJO!!!, ESTO NO MODIFICA LA CADENA DE TEXTO ORIGINAL
print(course)

#Para averiguar la posición de un caracter en una cadena de texto
print(course.find('o'))

#Para reemplazar una palabra o texto en una cadena de texto
print(course.replace('Beginners', 'Pros'))
#OJO!!!, ESTO NO MODIFICA LA CADENA DE TEXTO ORIGINAL
print(course)

#Para comprobar que una palabra se encuentra en un texto:
if 'Python' in course: #Devuelve un booleano
    print("Efectivamente, Python se encuentra en la frase")

#La función 'title' devuelve una cadena de texto transformando la inicial de cada palabra en mayúsucla
title_example = 'hola bUEnaS tARDES a todos'
print(title_example.title())
"""

# 9 Arithmetic Operations
"""
x = 10
y = 10
z = 10
j = 10

x += 3
print(x)

y-=3
print(y)

z*=3
print(z)

j//=2
print(j)
"""

# 10 Math Functions
"""
#Para saber más iformación sobre este módulo, acceder a https://docs.python.org/3/library/math.html
import math

x = 2.9

#Convierte cualquier número a positivo
print(abs(-2.9))

#Redondea hacia arriba
print(math.ceil(x))

#Redondea hacia abajo
print(math.floor(x))
"""

# 11 If statements
"""
is_hot = False
is_cold = True

if is_hot:
    print("It´s a hot day")
elif is_cold:
    print("It´s a cold day")
else:
    print("It´s a lovely day")
print("Enjoy your day")
"""

# 12 Ejercicio 1 If statements
"""
price = 1000000
good_credit = False

def comprobar_buen_precio(price, good_credit):
    if good_credit == True:
        porcentaje = price * 10 / 100
        return porcentaje
    elif good_credit == False:
        porcentaje = price * 20 / 100
        return porcentaje

price -= comprobar_buen_precio(price, good_credit)
print(f"The final price is ${round(price)}")
"""

# 13 Logical Operators
"""
#AND (&&) -> and
#OR (||) -> or
#NOT -> not

#Ejemplo de not
has_good_credit = True
has_criminal_record = False

if has_good_credit and not has_criminal_record:
    print("That´s a clean person")
"""

# 14 Comparaison Operators
"""
temperature = 30

if temperature > 30:
    print("It´s a hot day")
elif temperature < 30:
    print("It´s a cold day")
else:
    print("It´s a perfect day")
"""

# 15 Ejercicio 1 de Operadores de Comparación
"""
name = input("Introduce tu nombre: ")

if len(name)<3:
    print("Lo sentimos, el nombre tiene que contener al menos 3 caracteres")
elif len(name)>50:
    print("Lo sentimos, el nombre NO puede contener más de 50 caracteres")
else:
    print("Nombre introducido correctamente")
"""

# 16 Ejercicio 2 de Operadores de Comparación y funciones de cadenas de texto
"""
peso = float(input("Introduce tu peso: "))
opcion = input("(L)bs or (K)g: ")


def cambiar_peso(peso, opcion):
    if opcion.upper() == "K":
        peso /= 2.205
        print(f"Pesas {peso} kilos")

    elif opcion.upper() == "L":
        peso *= 2.205
        print(f"Pesas {peso} libras")


cambiar_peso(peso, opcion)
"""

# 17 While Loops
