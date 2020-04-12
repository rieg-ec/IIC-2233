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
        self.__energia_actual = self.energia_total
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
    setter/getters:
        - self.energia_actual

    - habilidad_especial()
    - recuperar_dccriatura()
    - sanar_dccriatura()

    """

    @property
    def energia_actual(self):
        return self.__energia_actual
    @energia_actual.setter
    def energia_actual(self, energia):
        if energia > self.energia_total:
            self.__energia_actual = self.energia_total
        elif energia < 0:
            self.__energia_actual = 0
        else:
            self.__energia_actual = energia

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
        file = open('criaturas.csv', 'r')
        lineas = file.readlines()
        file.close()

        for dccriatura_nombre in dccriaturas_nombres:
            for i in lineas:
                i = i.strip().split(',')

                if i[0] == dccriatura_nombre:
                    if i[1] == "Niffler":
                        dccriatura = dccriaturas.Niffler(dccriatura_nombre, self)
                    elif i[1] == "Augurey":
                        dccriatura = dccriaturas.Augurey(dccriatura_nombre, self)
                    elif i[1] == "Erkling":
                        dccriatura = dccriaturas.Erkling(dccriatura_nombre, self)

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
        if self.energia_actual >= pm.COSTO_ENERGETICO_ALIMENTAR:
            if len(self.alimentos) > 0:
                print("\nQue DCCriatura deseas alimentar?: ")
                print("")
                for index, dccriatura in enumerate(self.dccriaturas_actuales):
                    print(f"[{index}] {dccriatura.nombre} ({dccriatura.tipo})")
                opcion_dccriatura = input(f"\nIndique su opcion: "
                                          +f"({', '.join(str(i) for i in range(len(self.dccriaturas_actuales)))}): ")

                if opcion_dccriatura in [str(i) for i in range(len(self.dccriaturas_actuales))]:

                    print("\nQue alimento desea darle?")
                    print("")
                    for index, alimento in enumerate(self.alimentos):
                        print(f"[{index}] {alimento} (+{pm.ALIMENTOS[alimento]} de vida)")

                    opcion_alimento = input(f"Indique su opcion ({', '.join(str(i) for i in range(len(self.alimentos)))}): ")

                    if opcion_alimento in [str(i) for i in range(len(self.alimentos))]:
                        alimento_seleccionado = self.alimentos[int(opcion_alimento)]
                        dccriatura_seleccionada = self.dccriaturas_actuales[int(opcion_dccriatura)]

                        self.alimentos.remove(alimento_seleccionado)
                        dccriatura_seleccionada.alimentarse(alimento_seleccionado, self)
                        dccriatura_seleccionada.actualizar_archivo()
                        self.actualizar_archivo()


                    else:
                        print("\nOpcion invalida")
                else:
                    print("\nOpcion invalida")




            else:
                print("\nNo tienes alimentos")
        else:
            print("\nNo tienes energia suficiente")

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
