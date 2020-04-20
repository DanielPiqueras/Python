from Mensaje import Mensaje
from Usuario import Usuario
from Sistema_Entrega_Mensajes import Sistema_Entrega_Mensajes


listado_usuarios = []
usuarios_creados = {}
mensajes_creados = []

def menu_principal():
    print("Introduce una opción:\n(0.Salir ---- 1.Usuarios ---- 2.Mensajes)")
    opcion = input()
    return opcion

def menu_usuarios():
    print("Introduce una opción:\n(0.Salir ---- 1.Crear Usuario ---- 2.Mostrar Bandeja de Entrada ---- 3.Marcar Leído)")
    opcion = input()
    return opcion




def inicio():
    print("Introduce una opción:\n(0.Salir ---- 1.Usuarios ---- 2.Mensajes)")
    opcion1 = input()
    while opcion1 != '0':
        if opcion1 == '1':
            usuario()
        elif opcion1 == '2':
            mensaje()
        else:
            print("Incorrecto, vuelve a introducir una opción:\n(0.Salir ---- 1.Usuarios ---- 2.Mensajes)")
            opcion1 = input()
        break

def usuario():
    print("¡¡Bienvenido a los usuarios!!, ¿Qué desea hacer?...\n(0.Atrás ---- 1.Crear Usuario ---- 2.Mostrar Bandeja de Entrada ---- 3.Marcar Leído)")
    opcion_usuario = input()
    while opcion_usuario != '0':

        #Crear Usuario
        if opcion_usuario == '1':
            print("Introduce el nombre de usuario: ")
            nombre_usuario = input("Nombre: ")
            print("Creando usuarios, esto puede tardar un tiempo...")
            usuarios_creados[nombre_usuario] = Usuario(nombre_usuario)
            print(f'Bienvenido {usuarios_creados[nombre_usuario].nombre}!!')
            print("Usuario creado correctamente\n(0.Atrás ---- 1.Crear Usuario ---- 2.Mostrar Bandeja de Entrada ---- 3.Marcar Leído).")
            opcion_usuario = input()

        #Mostrar Bandeja de Entrada
        elif opcion_usuario == '2':
            print("Introduce el nombre de usuario del que quieres ver la bandeja de entrada: ")
            nombre_usuario = input("Nombre: ")
            print("Mostrando la bandeja de entrada...")
            try:
                usuarios_creados[nombre_usuario].mostrar_mensaje()
            except KeyError:
                print("No se ha encontrado el usuario.")
            print("\n(0.Atrás ---- 1.Crear Usuario ---- 2.Mostrar Bandeja de Entrada ---- 3.Marcar Leído).")
            opcion_usuario = input()

        #Marcar leído
        elif opcion_usuario == '3':
            print("Introduce un nombre de usuario")
            nombre_usuario = input("Nombre: ")

            try:
                usuarios_creados[nombre_usuario].mostrar_mensaje()

                try:
                    print("Introduce un mensaje que quieras marcar como leído: ")          
                    mensaje_elegido = input("Tiene que ser un número entero:")

                    usuarios_creados[nombre_usuario].marcar_leido(int(mensaje_elegido))
                    print("Mensaje marcado como leído correctamente\n(0.Atrás ---- 1.Crear Usuario ---- 2.Mostrar Bandeja de Entrada ---- 3.Marcar Leído).")
                except IndexError:
                    print("No se ha encontrado el mensaje")
            except KeyError:
                print("No se ha encontrado el usuario.")
                print("Ha ocurrido un error\n(0.Atrás ---- 1.Crear Usuario ---- 2.Mostrar Bandeja de Entrada ---- 3.Marcar Leído).")
            opcion_usuario = input()
            
        else:
            print("Incorrecto, vuelve a introducir una opción:\n(0.Atrás ---- 1.Crear Usuario ---- 2.Mostrar Bandeja de Entrada ---- 3.Marcar Leído)")
            opcion_usuario = input()
    inicio()

def mensaje():
    print("¡¡Bienvenido a los mensajes!!, ¿Qué desea hacer?...\n(0.Atrás ---- 1.Crear Mensaje ---- 2.Enviar mensaje ---- 3.Lista de mensajes enviados ---- 4.Lista de mensajes recibidos ---- 5. Lista de mensajes abiertos ---- 6.Obtener estadísticas)")
    opcion_mensaje = input()
    while opcion_mensaje != '0':
        #Crear mensaje
        if opcion_mensaje == '1':
            print("Introduce el mensaje que desea escribir: ")
            nombre_mensaje = input("Mensaje: ")
            mensajes_creados.append(Mensaje(nombre_mensaje))

            print("Mensaje escrito correctamente\n(0.Atrás ---- 1.Crear Mensaje ---- 2.Enviar mensaje ---- 3.Lista de mensajes enviados ---- 4.Lista de mensajes recibidos ---- 5. Lista de mensajes abiertos ---- 6.Obtener estadísticas).")
            opcion_mensaje = input()
        
        #Enviar mensaje
        elif opcion_mensaje == '2':
            print("Seleccione el mensaje que desea enviar: ")
            SE = Sistema_Entrega_Mensajes()
            SE.mostrar_mensajes(mensajes_creados)
            mensaje_elegido = input("Tiene que ser un número entero:")

            print("Seleccione el receptor")
            nombre_receptor = input()

            print("Registrando Usuario en la terminal...")
            SE.registro_usuarios(usuarios_creados)

            print("Enviando mensaje...")
            try:
                SE.anyadir_mensajes(usuarios_creados[nombre_receptor], mensajes_creados[int(mensaje_elegido)])
                print("¡¡Mensaje enviado correctamente!!\n(0.Atrás ---- 1.Crear Mensaje ---- 2.Enviar mensaje ---- 3.Lista de mensajes enviados ---- 4.Lista de mensajes recibidos ---- 5. Lista de mensajes abiertos ---- 6.Obtener estadísticas).")
            except (IndexError, KeyError):
                print("Ha ocurrido un error")
                print("\n(0.Atrás ---- 1.Crear Mensaje ---- 2.Enviar mensaje ---- 3.Lista de mensajes enviados ---- 4.Lista de mensajes recibidos ---- 5. Lista de mensajes abiertos ---- 6.Obtener estadísticas).")
            opcion_mensaje = input()
        
        
        #Listado de mensajes enviados
        elif opcion_mensaje == '3':
            print("Seleccione el mensaje del que desea ver la lista de usuarios a los que se les ha enviado: ")
          
            SE = Sistema_Entrega_Mensajes()
            SE.mostrar_mensajes(mensajes_creados)
            mensaje_elegido = input("Tiene que ser un número entero:")

            try:
                mensajes_creados[int(mensaje_elegido)].mostrar_usuarios_enviados(usuarios_creados)
                print("\n(0.Atrás ---- 1.Crear Mensaje ---- 2.Enviar mensaje ---- 3.Lista de mensajes enviados ---- 4.Lista de mensajes recibidos ---- 5. Lista de mensajes abiertos ---- 6.Obtener estadísticas).")
            except (IndexError, KeyError):
                print("Ha ocurrido un error")
                print("\n(0.Atrás ---- 1.Crear Mensaje ---- 2.Enviar mensaje ---- 3.Lista de mensajes enviados ---- 4.Lista de mensajes recibidos ---- 5. Lista de mensajes abiertos ---- 6.Obtener estadísticas).")
            opcion_mensaje = input()
        
        #Listado de mensajes recibidos
        elif opcion_mensaje == '4':
            print("Seleccione el mensaje del que desea ver la lista de usuarios que han recibido el mensaje: ")
          
            SE = Sistema_Entrega_Mensajes()
            SE.mostrar_mensajes(mensajes_creados)
            mensaje_elegido = input("Tiene que ser un número entero:")

            try:
                mensajes_creados[int(mensaje_elegido)].mostrar_usuarios_recibidos(usuarios_creados)
                print("\n(0.Atrás ---- 1.Crear Mensaje ---- 2.Enviar mensaje ---- 3.Lista de mensajes enviados ---- 4.Lista de mensajes recibidos ---- 5. Lista de mensajes abiertos ---- 6.Obtener estadísticas).")
            except (IndexError, KeyError):
                print("Ha ocurrido un error")
                print("\n(0.Atrás ---- 1.Crear Mensaje ---- 2.Enviar mensaje ---- 3.Lista de mensajes enviados ---- 4.Lista de mensajes recibidos ---- 5. Lista de mensajes abiertos ---- 6.Obtener estadísticas).")
            opcion_mensaje = input()
            
        
        #Listado de mensajes abiertos/leidos
        elif opcion_mensaje == '5':
            print("Seleccione el mensaje del que desea ver la lista de usuarios que han abierto el mensaje: ")
        
            SE = Sistema_Entrega_Mensajes()
            SE.mostrar_mensajes(mensajes_creados)
            mensaje_elegido = input("Tiene que ser un número entero:")

            try:
                mensajes_creados[int(mensaje_elegido)].mostrar_usuarios_leidos(usuarios_creados)
                print("\n(0.Atrás ---- 1.Crear Mensaje ---- 2.Enviar mensaje ---- 3.Lista de mensajes enviados ---- 4.Lista de mensajes recibidos ---- 5. Lista de mensajes abiertos ---- 6.Obtener estadísticas).")
            except (IndexError, KeyError):
                print("Ha ocurrido un error")
                print("\n(0.Atrás ---- 1.Crear Mensaje ---- 2.Enviar mensaje ---- 3.Lista de mensajes enviados ---- 4.Lista de mensajes recibidos ---- 5. Lista de mensajes abiertos ---- 6.Obtener estadísticas).")
            opcion_mensaje = input()
            
        
        #Estadísticas de recibidos y apertura
        elif opcion_mensaje == '6':
            print("Seleccione el mensaje del que desea ver las estadísticas: ")
          
            SE = Sistema_Entrega_Mensajes()
            SE.mostrar_mensajes(mensajes_creados)
            mensaje_elegido = input("Tiene que ser un número entero:")

            try:
                mensajes_creados[int(mensaje_elegido)].estadisticas_apertura(usuarios_creados)
                mensajes_creados[int(mensaje_elegido)].estadisticas_recepcion(usuarios_creados)
                print("\n(0.Atrás ---- 1.Crear Mensaje ---- 2.Enviar mensaje ---- 3.Lista de mensajes enviados ---- 4.Lista de mensajes recibidos ---- 5. Lista de mensajes abiertos ---- 6.Obtener estadísticas).")
            except (IndexError, KeyError):
                print("Ha ocurrido un error")
                print("\n(0.Atrás ---- 1.Crear Mensaje ---- 2.Enviar mensaje ---- 3.Lista de mensajes enviados ---- 4.Lista de mensajes recibidos ---- 5. Lista de mensajes abiertos ---- 6.Obtener estadísticas).")
            opcion_mensaje = input()
            

        else:
            print("Incorrecto, vuelve a introducir una opción:\n(0.Atrás ---- 1.Crear Mensaje ---- 2.Enviar mensaje ---- 3.Lista de mensajes enviados ---- 4.Lista de mensajes recibidos ---- 5. Lista de mensajes abiertos ---- 6.Obtener estadísticas).")
            opcion_mensaje = input()
    inicio()

#Pruebas
"""mensajes_creados.append(Mensaje("Mensaje Pepe2"))
mensajes_creados.append(Mensaje("Mensaje Pepe"))
usuarios_creados['Pepe'] = Usuario('Pepe')
usuarios_creados['Rodolfo'] = Usuario('Rodolfo')
SE = Sistema_Entrega_Mensajes()

SE.anyadir_mensajes(usuarios_creados['Pepe'], mensajes_creados[0])
SE.anyadir_mensajes(usuarios_creados['Rodolfo'], mensajes_creados[0])
SE.anyadir_mensajes(usuarios_creados['Pepe'], mensajes_creados[1])

usuarios_creados['Pepe'].marcar_leido(0)

mensajes_creados[0].mostrar_usuarios_enviados(usuarios_creados)
mensajes_creados[0].mostrar_usuarios_leidos(usuarios_creados)
mensajes_creados[0].mostrar_usuarios_recibidos(usuarios_creados)

mensajes_creados[1].mostrar_usuarios_enviados(usuarios_creados)
mensajes_creados[1].mostrar_usuarios_leidos(usuarios_creados)
mensajes_creados[1].mostrar_usuarios_recibidos(usuarios_creados)
"""
inicio()
