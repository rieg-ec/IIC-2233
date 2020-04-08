from abc import ABC, abstractmethod
from collections import defaultdict
import parametros

class Magizoologo(ABC):

    def __init__(self, nombre, sickles, dccriaturas, alimentos, licencia, nivel_magico, destreza, \
                 energia_total, responsabilidad, habilidad_especial):

        self.nombre = nombre
        self.sickles = int(sickles)
        self.dccriaturas_nombres = dccriaturas
        self.alimentos = alimentos.split(";")
        self.licencia = licencia
        self.nivel_magico = int(nivel_magico)
        self.destreza = int(destreza)
        self.energia_total = int(energia_total)
        self.responsabilidad = int(responsabilidad)
        self.habilidad_especial = habilidad_especial





    @abstractmethod
    def habilidad_especial(self):
        pass

    def alimentar_dccriatura(self):
        print("\nQue DCCriatura deseas alimentar :")
        for index, dccriatura in enumerate(self.dccriaturas_nombres):
            print(f"\n[{index}] {dccriatura})

        opcion_dccriatura = input("\nIndique su opcion : ")

        print("\nQue alimento deseas darle :")
        for index, alimento in enumerate(self.alimentos):
            print(f"\n[{index}] {alimento})
        opcion_alimento = input("\nIndique su opcion : ")


    def recuperar_dccriatura(self):
        pass

    def sanar_dccriatura(self):
        pass



class Docencio(Magizoologo):

    def __init__(self, nombre, sickles, dccriaturas, alimentos, licencia, nivel_magico, destreza, \
                 energia_total, responsabilidad, habilidad_especial):

        super().__init__(nombre, sickles, dccriaturas, alimentos, licencia, nivel_magico, destreza, \
                     energia_total, responsabilidad, habilidad_especial)

    def habilidad_especial(self):
        self.habilidad_especial = False


class Tareo(Magizoologo):

    def __init__(self, nombre, sickles, dccriaturas, alimentos, licencia, nivel_magico, destreza, \
                 energia_total, responsabilidad, habilidad_especial):

        super().__init__(nombre, sickles, dccriaturas, alimentos, licencia, nivel_magico, destreza, \
                     energia_total, responsabilidad, habilidad_especial)

    def habilidad_especial(self):
        self.habilidad_especial = False

class Hibrido(Magizoologo):

    def __init__(self, nombre, sickles, dccriaturas, alimentos, licencia, nivel_magico, destreza, \
                 energia_total, responsabilidad, habilidad_especial):

        super().__init__(nombre, sickles, dccriaturas, alimentos, licencia, nivel_magico, destreza, \
                     energia_total, responsabilidad, habilidad_especial)

    def habilidad_especial(self):
        self.habilidad_especial = False
