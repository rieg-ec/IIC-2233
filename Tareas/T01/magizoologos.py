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
        self.__alimentos = [random.choice([_ for _ in pm.ALIMENTOS.keys()])]
        self.licencia = pm.ESTADO_LICENCIA_INICIAL
        self.nivel_magico = random.randint(*pm.PARAMETROS_MAGIZOOLOGOS[self.index][0])
        self.destreza = random.randint(*pm.PARAMETROS_MAGIZOOLOGOS[self.index][1])
        self.energia_total = random.randint(*pm.PARAMETROS_MAGIZOOLOGOS[self.index][2])
        self.__energia_actual = self.energia_total
        self.responsabilidad = random.randint(*pm.PARAMETROS_MAGIZOOLOGOS[self.index][3])
        self.hab_especial_disp = pm.ESTADO_HABILIDAD_INICIAL

        self.dccriaturas = []

        # las dccriaturas se agregaran aca cuando se llame a la funcion pasar_al_dia_siguiente()
        # donde por cada dccriatura del magizoologo se chequeara si sucede algun evento, y si sucede
        # se agregan aca
        self.dccriaturas_escapadas_hoy = []
        self.dccriaturas_enfermas_hoy = []
        self.dccriaturas_salud_minima_hoy = []


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

    @property
    def alimentos(self):
        if self.__alimentos == [] or self.__alimentos == [""]:
            return False
        else:
            return [i for i in self.__alimentos if i != ""]

    @alimentos.setter
    def alimentos(self, alimento):
        if alimento != "":
            self.__alimento = alimento



    @abstractmethod
    def habilidad_especial(self):
        pass

    def modificar_parametros(self, sickles, dccriaturas_nombres, alimentos, licencia, nivel_magico, \
                             destreza, energia_total, responsabilidad, hab_especial_disp):
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
                    self.dccriaturas.append(dccriatura)

        self.sickles = int(sickles)
        self.alimentos = alimentos.split(";")
        self.licencia = licencia
        self.nivel_magico = int(nivel_magico)
        self.destreza = int(destreza)
        self.energia_total = int(energia_total)
        self.energia_actual = self.energia_total
        self.responsabilidad = int(responsabilidad)
        self.hab_especial_disp = hab_especial_disp

    def actualizar_archivo(self):
        """
        Esta funcion modifica el archivo magizoologos.csv
        con los atributos e informacion del magizoologo actualizados

        TO-DO:

        - en caso de ser Tareo actualizar nivel_clepto
        """


        # guardar atributos actuales para actualizar magizoologos.csv
        atributos_magizoologo = f"{self.nombre},{self.tipo},{self.sickles}," \
                                +f"{';'.join(i.nombre for i in self.dccriaturas)}," \
                                +f"{';'.join(i for i in self.alimentos if self.alimentos is not False)}," \
                                +f"{self.licencia},{self.nivel_magico},{self.destreza}," \
                                +f"{self.energia_total},{self.responsabilidad}," \
                                +f"{self.hab_especial_disp}"

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

    def alimentar_dccriatura(self, alimento, dccriatura):

        self.alimentos.remove(alimento)
        self.energia_actual -= pm.COSTO_ENERGETICO_ALIMENTAR
        dccriatura.alimentarse(alimento)
        dccriatura.actualizar_archivo()
        self.actualizar_archivo()

    def recuperar_dccriatura(self, dccriatura):

            self.energia_actual -= pm.COSTO_ENERGETICO_RECUPERAR
            prob_recuperar = (self.destreza + self.nivel_magico -
                              dccriatura.nivel_magico) / (self.destreza +
                                self.nivel_magico + dccriatura.nivel_magico)

            if random.random() < prob_recuperar:
                dccriatura.estado_escape = "False"
                print("\nRecuperacion exitosa")
                dccriatura.actualizar_archivo()
                return True
            else:
                print("\nRecuperacion ha fallado")
                return False


    def sanar_dccriatura(self, dccriatura):
        self.energia_actual -= pm.COSTO_ENERGETICO_SANAR
        prob_sanar = (self.nivel_magico - dccriatura.salud_actual) / \
                            (self.nivel_magico + dccriatura.salud_actual)

        if random.random() < prob_sanar:
            dccriatura.estado_salud = "False"
            print("\nSanacion exitosa")
            dccriatura.actualizar_archivo()
        else:
            print("\nSanacion ha fallado")




class Docencio(Magizoologo):

    def __init__(self, nombre):

        self.index = 0
        super().__init__(nombre, self.index)
        self.tipo = "Docencio"

    def habilidad_especial(self):
        if self.hab_especial_disp == "True":
            if self.energia_actual >= pm.COSTO_ENERGETICO_HAB_ESPECIAL:

                self.energia_actual -= pm.COSTO_ENERGETICO_HAB_ESPECIAL
                self.hab_especial_disp = "False"
                print("\nHas ocupado tu habilidad especial")

                for dccriatura in self.dccriaturas:
                    dccriatura.nivel_hambre = "satisfecha"
                    dccriatura.dias_sin_comer = 0
                    dccriatura.actualizar_archivo()

            else:
                print("\nNo tienes energia suficiente para ocupar tu habilidad especial")
        else:
            print("\nYa ocupaste tu habilidad especial")

    def alimentar_dccriatura(self, alimento, dccriatura):
        super().alimentar_dccriatura(alimento, dccriatura)
        dccriatura.salud_total += pm.AUMENTO_SALUD_TOTAL_ALIMENTAR_DOCENCIO
        dccriatura.actualizar_archivo()

    def recuperar_dccriatura(self, dccriatura):
        if super().recuperar_dccriatura(dccriatura):
            dccriatura.salud_actual -= pm.RESTAR_SALUD_TOT_CAPTURA_DOCENCIO
            dccriatura.actualizar_archivo()

class Tareo(Magizoologo):

    def __init__(self, nombre):
        self.index = 1

        super().__init__(nombre, self.index)
        self.tipo = "Tareo"

    def habilidad_especial(self):
        if self.hab_especial_disp == "True":
            if self.energia_actual >= pm.COSTO_ENERGETICO_HAB_ESPECIAL:

                self.hab_especial_disp = "False"
                self.energia_actual -= pm.COSTO_ENERGETICO_HAB_ESPECIAL
                print("\nHas ocupado tu habilidad especial")

                for dccriatura in self.dccriaturas:
                    if dccriatura.estado_escape == "True":
                        dccriatura.estado_escape = "False"
                        dccriatura.actualizar_archivo()

            else:
                print("\nNo tienes energia suficiente para ocupar tu habilidad especial")
        else:
            print("\nYa ocupaste tu habilidad especial")

    def alimentar_dccriatura(self, alimento, dccriatura):
        super().alimentar_dccriatura(alimento, dccriatura)
        if random.random() < pm.PROB_RECUPERAR_AL_ALIMENTAR_TAREO:
            dccriatura.salud_actual = dccriatura.salud_total


class Hibrido(Magizoologo):

    def __init__(self, nombre):
        self.index = 2

        super().__init__(nombre, self.index)
        self.tipo = "Híbrido"

    def habilidad_especial(self):
        if self.hab_especial_disp == "True":
            if self.energia_actual >= pm.COSTO_ENERGETICO_HAB_ESPECIAL:

                self.energia_actual -= pm.COSTO_ENERGETICO_HAB_ESPECIAL
                self.hab_especial_disp = "False"
                print("\nHas ocupado tu habilidad especial")

                for dccriatura in self.dccriaturas:
                    if dccriatura.estado_salud == "True":
                        dccriatura.estado_salud = "False"

            else:
                print("\nNo tienes energia suficiente para ocupar tu habilidad especial")
        else:
            print("\nYa ocupaste tu habilidad especial")

    def alimentar_dccriatura(self, alimento, dccriatura):
        super().alimentar_dccriatura(alimento, dccriatura)
        dccriatura.salud_actual += pm.SALUD_RECUPERADA_ALIMENTAR_HIBRIDO
