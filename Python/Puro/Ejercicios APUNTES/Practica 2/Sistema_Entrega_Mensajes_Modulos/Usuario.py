class Usuario:    
    def __init__(self, nombre):
        self.nombre = nombre
        self.__id = ""
        self.bandeja = []

    def set_id(self, id):
        self.__id = id

    def get_id(self):
        return self.__id

    def set_bandeja(self, mensajes):
        self.bandeja.append(mensajes)

    def get_bandeja(self):
        return self.bandeja

    def mostrar_mensaje(self):
        if len(self.bandeja) == 0:
            print("No se han encontrado mensajes en este usuario aún.")
        for b in range(len(self.bandeja)):
            if self.bandeja[b]['recibido']:
                if self.bandeja[b]['leido']:
                    print(f"({b}) {self.bandeja[b]['mensaje'].cuerpo} ya ha sido leído.")
                else:
                    print(f"({b}) {self.bandeja[b]['mensaje'].cuerpo}.")

    def marcar_leido(self, numero):
        if self.bandeja[numero]['recibido']:
            self.bandeja[numero]['leido'] = True

