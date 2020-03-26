class Estudiante:
    # Debes completar el constructor de la clase estudiante
    def __init__(self, username, hobbies, deberes):

        self.username = username
        self.hobbies = hobbies
        self.deberes = deberes
        self.__felicidad = 0
        self.__estres = 0
        self.rango_felicidad = (0, 0)
        self.rango_estres = (0, 0)

    def realizar_actividad(self, actividad):
        print(f"Realizando {actividad.nombre}")
        print(f"El nivel de estres del estudiante es {self.estres}\
             y el de felicidad {self.felicidad}")

    # Debes rellenar las property felicidad
    @property
    def felicidad(self):
        return self.__felicidad

    @felicidad.setter
    def felicidad(self, nueva_felicidad):
        if nueva_felicidad > self.rango_felicidad[1]:
            self.__felicidad = self.rango_felicidad[1]
        elif nueva_felicidad < self.rango_felicidad[0]:
            self.__felicidad = self.rango_felicidad[0]
        else:
            self.__felicidad += nueva_felicidad

    # Debes rellenar las property estres
    @property
    def estres(self):
        return self.__estres

    @estres.setter
    def estres(self, nuevo_estres):
        if nuevo_estres > self.rango_estres[1]:
            self.__estres = self.rango_estres[1]
        elif nuevo_estres < self.rango_estres[0]:
            self.__estres = self.rango_estres[0]
        else:
            self.__estres += nuevo_estres


######## REVISAR LOS PARAMETROS
class Alumno(Estudiante):
    def __init__(self, username, hobbies, deberes):
        super().__init__(username, hobbies, deberes)
        self.__felicidad = 75
        self.__estres = 25
        self.rango_felicidad = (0, 200)
        self.rango_estres = (0, 100)

    def realizar_actividad(self, actividad):
        print(f"Realizando {actividad.nombre}")
        self.felicidad = actividad.felicidad * 1.5
        self.estres = actividad.estres
        print(f"El nivel de estres del estudiante es {self.estres}\
             y el de felicidad {self.felicidad}")


######## REVISAR LOS PARAMETROS
class Ayudante(Estudiante):
    def __init__(self, username, hobbies, deberes):
        super().__init__(username, hobbies, deberes)
        self.__felicidad = 25
        self.__estres = 75
        self.rango_felicidad = (0, 100)
        self.rango_estres = (0, 200)

    def realizar_actividad(self, actividad):
        print(f"Realizando {actividad.nombre}")
        self.felicidad = actividad.felicidad
        self.estres = 2*actividad.estres
        print(f"El nivel de estres del ayudante es {self.estres}\
             y el de felicidad {self.felicidad}")
