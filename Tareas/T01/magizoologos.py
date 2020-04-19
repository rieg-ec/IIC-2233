from abc import ABC, abstractmethod
import parametros as pm
import random
import dccriaturas

class Magizoologo(ABC):

    def __init__(self, nombre, index):

        # el parametro index se usa al llamar a la clase madre en las subclases, para
        # llamar a las listas con los parametros de  cada magizoologo en parametros.py
        # al llamar a modificar_parametros()
        self.__index = index
        self.tipo = None
        self.nombre = nombre
        self.sickles = pm.SICKLES_INICIALES
        self.alimentos = [random.choice([_ for _ in pm.ALIMENTOS.keys()])]
        self.licencia = pm.ESTADO_LICENCIA_INICIAL
        self.nivel_magico = random.randint(*pm.PARAMETROS_MAGIZOOLOGOS[self.__index][0])
        self.destreza = random.randint(*pm.PARAMETROS_MAGIZOOLOGOS[self.__index][1])
        self.energia_total = random.randint(*pm.PARAMETROS_MAGIZOOLOGOS[self.__index][2])
        self.__energia_actual = self.energia_total
        self.responsabilidad = random.randint(*pm.PARAMETROS_MAGIZOOLOGOS[self.__index][3])
        self.hab_especial_disp = pm.ESTADO_HABILIDAD_INICIAL

        self.dccriaturas = []

        # las dccriaturas se agregaran en estas listas cuando se llame a la
        # funcion pasar_al_dia_siguiente()  donde por cada dccriatura del magizoologo
        # se chequeara si sucede alguno de los eventos, y si sucede se agregan aca
        # y se fiscaliza correspondientemente
        self.dccriaturas_escapadas_hoy = []
        self.dccriaturas_enfermas_hoy = []
        self.dccriaturas_salud_minima_hoy = []

    @property
    def energia_actual(self):
        return self.__energia_actual

    @energia_actual.setter
    def energia_actual(self, energia):
        # energia no puede ser mayor a energia_total
        if energia > self.energia_total:
            self.__energia_actual = self.energia_total
        elif energia < 0:
            self.__energia_actual = 0
        else:
            self.__energia_actual = energia


    @abstractmethod
    def habilidad_especial(self):
        pass

    def modificar_parametros(self, sickles, dccriaturas_nombres, \
                             alimentos, licencia, nivel_magico, destreza, \
                             energia_total, responsabilidad, hab_especial_disp):
        """
        Esta funcion modifica los parametros del magizoologo en caso de que se cree
        una instancia y se quieran ocupar argumentos distintos de los que se crean
        por defecto, que sucede en el  caso de iniciar sesion
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
        self.alimentos = [i for i in alimentos.split(";") if i != ""]
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
        """


        # guardar atributos actuales para actualizar magizoologos.csv
        atributos_magizoologo = f"{self.nombre},{self.tipo},{self.sickles}," \
                                +f"{';'.join(i.nombre for i in self.dccriaturas)}," \
                                +f"{';'.join(i for i in self.alimentos)}," \
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
        # si la alimentacion fue exitosa o no, retornar True o False
        # para en caso de ser exitosa agregarle funcionalidad en las subclases
        if dccriatura.alimentarse(alimento):
            return True
        else:
            return False
        dccriatura.actualizar_archivo()
        self.actualizar_archivo()

    def recuperar_dccriatura(self, dccriatura):
        """
        Este metodo retorna True o False si la recuperacion fue exitosa, para que cada
        magizoologo pueda agregarle funcionalidad en caso de ser exitosa
        """
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

        self.__index = 0
        super().__init__(nombre, self.__index)
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
                    print(f"{dccriatura.nombre} se encuentra ahora satisfecha")
                    dccriatura.actualizar_archivo()

            else:
                print("\nNo tienes energia suficiente para ocupar tu habilidad especial")
        else:
            print("\nYa ocupaste tu habilidad especial")

    def alimentar_dccriatura(self, alimento, dccriatura):
        """
        Ademas de la funcionalidad del metodo de la clase madre,
        Docencio aumenta la salud de la dccriatura alimentada
        """
        if super().alimentar_dccriatura(alimento, dccriatura):
            dccriatura.salud_total += pm.AUMENTO_SALUD_TOTAL_ALIMENTAR_DOCENCIO
            dccriatura.actualizar_archivo()

    def recuperar_dccriatura(self, dccriatura):
        """
        Ademas de la funcionalidad del metodo de la clase madre,
        Docencio quita salud de la dccriatura recuperada si logro recuperarla
        """
        if super().recuperar_dccriatura(dccriatura):
            dccriatura.salud_actual -= pm.RESTAR_SALUD_TOT_CAPTURA_DOCENCIO
            dccriatura.actualizar_archivo()

class Tareo(Magizoologo):

    def __init__(self, nombre):
        self.__index = 1

        super().__init__(nombre, self.__index)
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
                        print(f"Has recuperado a {dccriatura.nombre}")
                        dccriatura.actualizar_archivo()

            else:
                print("\nNo tienes energia suficiente para ocupar tu habilidad especial")
        else:
            print("\nYa ocupaste tu habilidad especial")

    def alimentar_dccriatura(self, alimento, dccriatura):
        """
        Ademas de la funcionalidad del metodo de la clase madre,
        Tareo tiene una probabilidad de recuperar el
        maximo de salud de la dccriatura alimentada
        """
        if super().alimentar_dccriatura(alimento, dccriatura):
            if random.random() < pm.PROB_RECUPERAR_AL_ALIMENTAR_TAREO:
                dccriatura.salud_actual = dccriatura.salud_total

class Hibrido(Magizoologo):

    def __init__(self, nombre):
        self.__index = 2

        super().__init__(nombre, self.__index)
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
                        print(f"{dccriatura.nombre} se ha sanado")

            else:
                print("\nNo tienes energia suficiente para ocupar tu habilidad especial")
        else:
            print("\nYa ocupaste tu habilidad especial")

    def alimentar_dccriatura(self, alimento, dccriatura):
        """
        Ademas de la funcionalidad del metodo de la clase madre,
        Hibrido recupera salud a la dccriatura alimentada
        """
        if super().alimentar_dccriatura(alimento, dccriatura):
            dccriatura.salud_actual += pm.SALUD_RECUPERADA_ALIMENTAR_HIBRIDO
