from abc import ABC, abstractmethod
from collections import defaultdict
import parametros as pm
import random
import dccriaturas

class Magizoologo(ABC):

    def __init__(self, nombre, index):

        self.index = index # override en clases hijas
        self.tipo = "" # override en clases hijas
        self.nombre = nombre
        self.sickles = pm.SICKLES_INICIALES
        self.alimentos = [random.choice([_ for _ in pm.ALIMENTOS.keys()])]
        self.licencia = pm.ESTADO_LICENCIA_INICIAL
        self.nivel_magico = random.randint(*pm.PARAMETROS_MAGIZOOLOGOS[self.index][0])
        self.destreza = random.randint(*pm.PARAMETROS_MAGIZOOLOGOS[self.index][1])
        self.energia_total = random.randint(*pm.PARAMETROS_MAGIZOOLOGOS[self.index][2])
        self.energia_actual = self.energia_total
        self.responsabilidad = random.randint(*pm.PARAMETROS_MAGIZOOLOGOS[self.index][3])
        self.habilidad_especial = pm.ESTADO_HABILIDAD_INICIAL

        self.dccriaturas_actuales = []

        # las dccriaturas se agregaran aca cuando se llame a la funcion pasar_al_dia_siguiente()
        # donde por cada dccriatura del magizoologo se chequeara si sucede algun evento, y si sucede
        # se agregan aca
        self.dccriaturas_escapadas_hoy = []
        self.dccriaturas_enfermas_hoy = []
        self.dccriaturas_salud_minima_hoy = []


    """
    TO-DO:

    - habilidad_especial()

    - alimentar_dccriatura()

    - recuperar_dccriatura()

    - sanar_dccriatura()

    """
    @abstractmethod
    def habilidad_especial(self):
        pass

    def modificar_parametros(self, sickles, dccriaturas_nombres, alimentos, licencia, nivel_magico, \
                             destreza, energia_total, responsabilidad, habilidad_especial):
        """
        Esta funcion modifica los parametros del magizoologo en caso de que se cree una instancia
        y se quieran ocupar argumentos distintos de los que se crean por defecto, que sucede en el
        caso de iniciar sesion

        TO-DO: explicar mejor funcionamiento y documentar mejor

        automatizar --> no necesita argumentos, lee magizoologos.csv
        """

        dccriaturas_nombres = dccriaturas_nombres.split(";")
        with open('criaturas.csv', 'r') as f:
            for dccriatura_nombre in dccriaturas_nombres:
                for i in f.readlines():
                    i = i.strip().split(',')

                    if i[0] == dccriatura_nombre:
                        if i[1] == "Niffler":
                            dccriatura = dccriaturas.Niffler(dccriatura_nombre)
                        elif i[1] == "Augurey":
                            dccriatura = dccriaturas.Augurey(dccriatura_nombre)
                        elif i[1] == "Erkling":
                            dccriatura = dccriaturas.Erkling(dccriatura_nombre)

                        dccriatura.modificar_parametros()
                        self.dccriaturas_actuales.append(dccriatura)

        self.sickles = int(sickles)
        self.alimentos = alimentos.split(";")
        self.licencia = licencia
        self.nivel_magico = int(nivel_magico)
        self.destreza = int(destreza)
        self.energia_total = int(energia_total)
        self.energia_actual = self.energia_total
        self.responsabilidad = int(responsabilidad)
        self.habilidad_especial = habilidad_especial

    def actualizar_archivo(self):
        """
        Esta funcion modifica el archivo magizoologos.csv
        con los atributos e informacion del magizoologo actualizados

        TO-DO:

        - en caso de ser Tareo actualizar nivel_clepto
        """

        # guardar atributos actuales para actualizar magizoologos.csv
        atributos_magizoologo = f"{self.nombre},{self.tipo},{self.sickles}," \
                                +f"{';'.join(i.nombre for i in self.dccriaturas_actuales)}," \
                                +f"{';'.join(_ for _ in self.alimentos)}," \
                                +f"{self.licencia},{self.nivel_magico},{self.destreza}," \
                                +f"{self.energia_total},{self.responsabilidad}," \
                                +f"{self.habilidad_especial}"

        # guardar estado actual de magizoologos.csv
        # y nombres de magizoologos
        with open('magizoologos.csv', 'r') as f:
            nombres_existentes = []
            lineas_existentes = []

            for i in f.readlines():
                i = i.strip().split(',')
                nombres_existentes.append(i[0])
                lineas_existentes.append(i)

            f.close()

        with open('magizoologos.csv', 'w') as f:
            for i in lineas_existentes:
                # no alterar informacion de otros magizoologos
                if i[0] != self.nombre:
                    f.write(",".join(_ for _ in i))
                    f.write("\n")

            # escribir al final del archivo informacion de magizoologo actualizada
            f.write(atributos_magizoologo)
            f.write("\n")
            f.close()

    def alimentar_dccriatura(self):
        """
        TO-DO: alimentar a la dccriatura correspondiente, ocupando la instancia de la dccriatura creada
        y modificando sus atributos correspondientemente
        """
        print("\nQue DCCriatura deseas alimentar :")
        for index, dccriatura in enumerate(self.dccriaturas_nombres):
            print(f"\n[{index}] {dccriatura}")

        opcion_dccriatura = input("\nIndique su opcion : ")

        print("\nQue alimento deseas darle :")
        for index, alimento in enumerate(self.alimentos):
            print(f"\n[{index}] {alimento}")
        opcion_alimento = input("\nIndique su opcion : ")

    def recuperar_dccriatura(self):
        pass

    def sanar_dccriatura(self):
        pass



class Docencio(Magizoologo):

    def __init__(self, nombre):

        self.index = 0
        super().__init__(nombre, self.index)
        self.tipo = "Docencio"

    def habilidad_especial(self):
        self.habilidad_especial = False


class Tareo(Magizoologo):

    def __init__(self, nombre):
        self.index = 1

        super().__init__(nombre, self.index)
        self.tipo = "Tareo"

    def habilidad_especial(self):
        self.habilidad_especial = False

class Hibrido(Magizoologo):

    def __init__(self, nombre):
        self.index = 2

        super().__init__(nombre, self.index)
        self.tipo = "Híbrido"

    def habilidad_especial(self):
        self.habilidad_especial = False
