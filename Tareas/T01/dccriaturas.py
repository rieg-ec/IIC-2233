from abc import ABC, abstractmethod
import random
import parametros as pm


class DCCriatura(ABC):

    def __init__(self, nombre, dueño):
        """
        el atributo 'self.index' es 0, 1 o 2, dependiendo de la ddcriatura,
        y es usado como index al llamar a las estructuras de datos de parametros.py,
        donde estaran los parametros para cada ddcriatura
        """

        self.index = 0
        self.nombre = nombre
        self.nivel_magico = random.randint(*pm.PARAMETROS_DCCRIATURAS[self.index][0])
        self.salud_total = random.randint(*pm.PARAMETROS_DCCRIATURAS[self.index][1]) # rango de salud
        self.__salud_actual = self.salud_total # salud inicial es la maxima
        self.prob_esc = pm.PARAMETROS_DCCRIATURAS[self.index][2]
        self.prob_enf = pm.PARAMETROS_DCCRIATURAS[self.index][3]
        self.max_dias_sin_comer = pm.PARAMETROS_DCCRIATURAS[self.index][4]
        self.nivel_agresividad = pm.PARAMETROS_DCCRIATURAS[self.index][5] # nivel de agresividad
        self.estado_salud = pm.ESTADO_SALUD_INICIAL_DCCRIATURAS
        self.estado_escape = pm.ESTADO_ESCAPE_INICIAL_DCCRIATURAS
        self.nivel_hambre = pm.HAMBRE_INICIAL_DCCRIATURAS
        self.__dias_sin_comer = pm.DIAS_SIN_COMER_INICIAL_DCCRIATURAS
        self.tipo = None
        self.nivel_clepto = 0

        self.alimentada_hoy = False
        self.dueño = dueño

    @property
    def dias_sin_comer(self):
        return self.__dias_sin_comer
    @dias_sin_comer.setter
    def dias_sin_comer(self, dias):
        if dias > self.max_dias_sin_comer:
            self.nivel_hambre = "hambrienta"
        self.__dias_sin_comer = dias

    @property
    def salud_actual(self):
        return self.__salud_actual
    @salud_actual.setter
    def salud_actual(self, salud):
        if salud > self.salud_total:
            self.__salud_actual = self.salud_total
        elif salud < pm.SALUD_MINIMA_DCCRIATURAS:
            self.__salud_actual = pm.SALUD_MINIMA_DCCRIATURAS
        else:
            self.__salud_actual = salud

    @abstractmethod
    def habilidad_especial(self):
        pass

    def modificar_parametros(self):
        with open('criaturas.csv', 'r') as f:
            for linea in f.readlines():
                linea = linea.split(',')
                if linea[0] == self.nombre:
                    atributos = linea
            f.close()

        self.nivel_magico = int(atributos[2])
        self.prob_esc = float(atributos[3])
        self.prob_enf = float(atributos[4])
        self.estado_salud = atributos[5]
        self.estado_escape = atributos[6]
        self.salud_total = int(atributos[7])
        self.salud_actual = int(atributos[8])
        self.nivel_hambre = atributos[9]
        self.nivel_agresividad = atributos[10]
        self.dias_sin_comer = int(atributos[11])
        self.nivel_clepto = int(atributos[12])

    def actualizar_archivo(self):
        """
        Esta funcion actualiza los parametros de la dccriatura en
        el archivo criaturas.csv, reescribiendo el archivo con la dccriatura al
        final

        TO-DO: documentar mejor, explicar funcionamiento
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

    def alimentarse(self, alimento):

        alimentada = True
        # si el alimento es higado de dragon la criatura se sana
        if alimento == "Hígado de Dragón":
            self.estado_salud = "False"
            print(f"{self.nombre} se ha alimentado con Higado de Dragón")

        # si el alimento es buñuelo de gusarajo la criatura podria atacar
        elif alimento == "Buñuelo de Gusarajo":
            if random.random() < pm.PROBABILIDAD_ATACAR_BUÑUELO:
                print(f"\n{self.nombre} ha rechazado el alimento")
                alimentada = False
            else:
                print(f"{self.nombre} se ha alimentado con Buñuelo de Gusarajo")


        elif alimento == "Tarta de Melaza":
            if self.tipo == "Niffler":
                if random.random() < pm.PROBABILIDAD_DISMINUIR_AGRESIVIDAD_MELAZA:
                    self.agresividad = "inofensiva"
            print(f"{self.nombre} se ha alimentado con Tarta de Melaza")


        if alimentada:
            self.nivel_hambre = "satisfecha"
            self.dias_sin_comer = 0
            self.alimentada_hoy = True
            self.salud_actual += pm.ALIMENTOS[alimento]


        efecto_hambre = pm.EFECTO_HAMBRE[self.nivel_hambre]
        efecto_agresividad = pm.EFECTO_AGRESIVIDAD[self.nivel_agresividad]

        probabilidad_ataque = (efecto_hambre + efecto_agresividad) / 100

        if random.random() < probabilidad_ataque:
            ataque = self.dueño.nivel_magico - self.nivel_magico
            self.dueño.energia_actual -= ataque

    def escaparse(self):
        resp_magizoologo = self.dueño.responsabilidad
        if self.nivel_hambre == "hambrienta":
            efecto_hambre = 20
        else:
            efecto_hambre = 0
        prob_total_escaparse = self.prob_esc + (efecto_hambre - resp_magizoologo) / 100

        if self.estado_escape == "False" and random.random() < prob_total_escaparse:
            self.estado_escape = "True"
            return True
        else:
            return False

    def enfermarse(self):
        resp_magizoologo = self.dueño.responsabilidad
        prob_total_enfermarse = self.prob_enf + \
                                (self.salud_total - self.salud_actual) / self.salud_total - \
                                resp_magizoologo / 100

        if self.estado_salud == "False" and random.random() < prob_total_enfermarse:
            self.estado_salud = "True"
            return True
        else:
            return False


class Augurey(DCCriatura):
    def __init__(self, nombre, dueño):

        super().__init__(nombre, dueño)

        self.index = 0
        self.tipo = "Augurey"

    def habilidad_especial(self):
        if self.nivel_hambre == "satisfecha" and self.estado_salud == "False" and \
            self.salud_actual == self.salud_total:
            alimento = random.choice([_ for _ in pm.ALIMENTOS.keys()])
            self.dueño.alimentos.append(alimento)
            print(f"\nAugurey {self.nombre} te ha regalado un {alimento}")

class Niffler(DCCriatura):
    def __init__(self, nombre, dueño):

        super().__init__(nombre, dueño)

        self.index = 1
        self.tipo = "Niffler"
        self.nivel_clepto = random.randint(*pm.NIVEL_CLEPTO_NIFFLER)

    def habilidad_especial(self):
        sickles = self.nivel_clepto * 2
        if self.nivel_hambre == "satisfecha":
            self.dueño += sickles
            print(f"\nNiffler {self.nombre} te ha regañadp {sickles} sickles")
        else:
            self.dueño -= sickles

class Erkling(DCCriatura):
    def __init__(self, nombre, dueño):

        super().__init__(nombre, dueño)

        self.index = 2
        self.tipo = "Erkling"

    def habilidad_especial(self):
        if self.nivel_hambre == "hambrienta":
            alimento_robado = random.choice(self.dueño.alimentos)
            print(f"\nErkling {self.nombre} te ha robado {alimento_robado}")
            self.nivel_hambre = "satisfecha"
            self.salud_actual += pm.ALIMENTOS[alimento_robado]
            if alimento_robado == "Hígado de Dragón":
                self.estado_salud = "False"
