import uuid
import random

class Sistema_Entrega_Mensajes:

    def mostrar_mensajes(self, mensajes):
        for i in range(len(mensajes)):
            print(f'({i}) {mensajes[i].cuerpo}\n')

    def registro_usuarios(self, usuarios):
        for usuario in usuarios:
            usuarios[usuario].set_id(uuid.uuid1())
            
    def anyadir_mensajes(self, usuario, mensaje):
        mensaje.set_id(uuid.uuid1())
        mensajes = {}
        mensajes['mensaje'] = mensaje

        #Para que un mensaje tenga la posibilidad de no recibirse
        if random.randint(1, 10) > 8:
            mensajes['recibido'] = False
        else:
            mensajes['recibido'] = True

        mensajes['leido'] = False
        usuario.bandeja.append(mensajes)