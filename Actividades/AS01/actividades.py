class Actividad:
    def __init__(self, nombre, felicidad, estres):
        self.nombre = nombre
        self.felicidad = felicidad
        self.estres = estres


class Hobby(Actividad):
    def __init__(self, nombre, felicidad, estres):
        super().__init__(nombre, felicidad, estres)


class Deber(Actividad):
    def __init__(self, nombre, felicidad, estres):
        super().__init__(nombre, felicidad, estres)
