from abc import ABC


class DCCriatura(ABC):

    def __init__(self, nombre, nivel_magico, prob_esc, prob_enf, estado_salud \
                 estado_escape, salud_total, salud_actual, nivel_hambre, nivel_agresividad \
                 dias_sin_comer):


        self.nombre = nombre
        self.nivel_magico = nivel_magico
        self.prob_esc = prob_esc
        self.prob_enf = prob_enf
        self.estado_salud = estado_salud
        self.estado_escape = estado_escape
        self.salud_total = salud_total
        self.salud_actual = salud_actual
        self.nivel_hambre = nivel_hambre
        self.nivel_agresividad = nivel_agresividad
        self.dias_sin_comer = dias_sin_comer

    def alimentarse(self):
        pass

    def escaparse(self):
        pass

    def enfermarse(self):
        pass


class Augurey(DCCriatura):
    def __init__(self, nombre, nivel_magico, prob_esc, prob_enf, estado_salud \
                 estado_escape, salud_total, salud_actual, nivel_hambre, nivel_agresividad \
                 dias_sin_comer, nivel_clepto):

        super().__init__(nombre, nivel_magico, prob_esc, prob_enf, estado_salud \
                     estado_escape, salud_total, salud_actual, nivel_hambre, nivel_agresividad \
                     dias_sin_comer)

        self.nivel_clepto = nivel_clepto
