class Mensaje:
    def __init__(self, cuerpo):
        self.cuerpo = cuerpo
        self.__id = ""

    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def mostrar_usuarios_enviados(self, listado):
        for usuarios in listado:
            for mensaje in listado[usuarios].bandeja:
                if mensaje['mensaje'].cuerpo == self.cuerpo:
                    print(f"El mensaje {mensaje['mensaje'].cuerpo} ha sido enviado a {listado[usuarios].nombre}")
        pass

    #Comprobar usuarios leídos manera corta, cambiar nombre de función
    def mostrar_usuarios_leidos(self, listado):
        for usuarios in listado:
            for mensaje in listado[usuarios].bandeja:
                if mensaje['recibido']:
                    if mensaje['leido'] == True and mensaje['mensaje'].cuerpo == self.cuerpo:
                        print(f"El mensaje {mensaje['mensaje'].cuerpo} ha sido leído por {listado[usuarios].nombre}")
        pass

    def mostrar_usuarios_recibidos(self, listado):
        for usuarios in listado:
            for mensaje in listado[usuarios].bandeja:
                if mensaje['recibido'] == True and mensaje['mensaje'].cuerpo == self.cuerpo:
                    print(f"El mensaje {mensaje['mensaje'].cuerpo} ha sido recibido por el usuario {listado[usuarios].nombre}")

    def estadisticas_apertura(self, listado):
        total = 0
        contador = 0
        for usuarios in listado:
            for mensaje in listado[usuarios].bandeja:
                if mensaje['mensaje'].cuerpo == self.cuerpo:
                    total += 1
                if mensaje['leido'] == True and mensaje['mensaje'].cuerpo == self.cuerpo:
                    contador +=1
        print(f'({total}/{contador}) El porcentaje de apertura del mensaje {self.cuerpo} es {str(round((100 * contador)/total,2))}%')    

    def estadisticas_recepcion(self, listado):
        total = 0
        contador = 0
        for usuarios in listado:
            for mensaje in listado[usuarios].bandeja:
                if mensaje['mensaje'].cuerpo == self.cuerpo:
                    total += 1
                if mensaje['recibido'] == True and mensaje['mensaje'].cuerpo == self.cuerpo:
                    contador +=1
        print(f'({total}/{contador}) El porcentaje de recepcion del mensaje {self.cuerpo} es {str(round((100 * contador)/total,2))}%')

