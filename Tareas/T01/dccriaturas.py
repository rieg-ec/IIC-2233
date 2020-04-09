from abc import ABC
import random
import parametros as pm


class DCCriatura(ABC):

    def __init__(self, nombre):
        """
        el atributo 'self.index' es 0, 1 o 2, dependiendo de la ddcriatura,
        y es usado como index al llamar a las estructuras de datos de parametros.py,
        donde estaran los parametros para cada ddcriatura
        """

        self.index = 0
        self.nombre = nombre
        self.nivel_magico = random.randint(*pm.PARAMETROS_DCCRIATURAS[self.index][0])
        self.salud_total = random.randint(*pm.PARAMETROS_DCCRIATURAS[self.index][1]) # rango de salud
        self.salud_actual = self.salud_total # salud inicial es la maxima
        self.prob_esc = pm.PARAMETROS_DCCRIATURAS[self.index][2]
        self.prob_enf = pm.PARAMETROS_DCCRIATURAS[self.index][3]
        self.max_dias_sin_comer = pm.PARAMETROS_DCCRIATURAS[self.index][4]
        self.nivel_agresividad = pm.PARAMETROS_DCCRIATURAS[self.index][5] # nivel de agresividad
        self.estado_salud = "False" # inicia sana
        self.estado_escape = "False" # inicia sin escaparse
        self.nivel_hambre = 0
        self.dias_sin_comer = 0
        self.tipo = ""
        self.nivel_clepto = 0


    def actualizar_archivo(self):
        """
        Esta funcion actualiza los parametros de la dccriatura en
        el archivo criaturas.csv, reescribiendo el archivo con la dccriatura al
        final
        """

        atributos_dccriatura = f"{self.nombre},{self.tipo},{self.nivel_magico}," \
                                +f"{self.prob_esc},{self.prob_enf},{self.estado_salud}," \
                                +f"{self.estado_escape},{self.salud_total}," \
                                +f"{self.salud_actual}," \
                                +f"{self.nivel_hambre},{self.nivel_agresividad}," \
                                +f"{self.dias_sin_comer},{self.nivel_clepto}"

        with open('criaturas.csv', 'r') as f:
            nombres_existentes = []
            lineas_existentes = []
            for i in f.readlines():
                i = i.strip().split(',')
                lineas_existentes.append(i)
                nombres_existentes.append(i[0])
            f.close()

        with open('criaturas.csv', 'w') as f:
            for i in lineas_existentes:
                if i[0] != self.nombre:
                    f.write(",".join(_ for _ in i))
                    f.write("\n")
            f.write(atributos_dccriatura)
            f.write("\n")
            f.close()



    def escaparse(self):
        pass

    def enfermarse(self):
        pass


class Augurey(DCCriatura):
    def __init__(self, nombre):

        super().__init__(nombre)

        self.index = 0
        self.tipo = "Augurey"


class Niffler(DCCriatura):
    def __init__(self, nombre):

        super().__init__(nombre)

        self.index = 1
        self.tipo = "Niffler"
        self.nivel_clepto = random.randint(*pm.NIVEL_CLEPTO_NIFFLER)

class Erkling(DCCriatura):
    def __init__(self, nombre):

        super().__init__(nombre)

        self.index = 2
        self.tipo = "Erkling"
