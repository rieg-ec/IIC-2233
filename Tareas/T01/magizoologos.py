from abc import ABC

class Magizoologo(ABC):

    def __init__(self, nombre, sickles, criaturas, alimentos, licencia, nivel_magia, destreza, \
        responsabilidad, hab_especial):

        self.nombre = nombre
        self.sickles = sickles
        self.criaturas = criaturas
        self.alimentos = alimentos
        self.licencia = licencia
        self.nivel_magia = nivel_magia
        self.destreza = destreza
        self.responsabilidad = responsabilidad
        self.habilidad_especial = hab_especial


    def adoptar_criatura(self):
        pass

    def comprar_alimento(self):
        pass


    def alimentar_criatura(self):
        pass

    def recuperar_criatura(self):
        pass

    def sanar_criatura(self):
        pass

    def mostrar_estado(self):
        pass

    @abstractmethod
    def habilidad_especial(self):
        pass

class Docencio(Magizoologo):

    def __init__(self, nombre, sickles, criaturas, alimentos, licencia, nivel_magia, destreza, \
        responsabilidad, hab_especial):

        super().__init__(nombre, sickles, criaturas, alimentos, licencia, nivel_magia, destreza, \
            responsabilidad, hab_especial)

        def habilidad_especial(self):
            pass


class Tareo(Magizoologo):

    def __init__(self, nombre, sickles, criaturas, alimentos, licencia, nivel_magia, destreza, \
        responsabilidad, hab_especial):

        super().__init__(nombre, sickles, criaturas, alimentos, licencia, nivel_magia, destreza, \
            responsabilidad, hab_especial)

        def habilidad_especial(self):
            pass

class Hibrido(Magizoologo):

    def __init__(self, nombre, sickles, criaturas, alimentos, licencia, nivel_magia, destreza, \
        responsabilidad, hab_especial):

        super().__init__(nombre, sickles, criaturas, alimentos, licencia, nivel_magia, destreza, \
            responsabilidad, hab_especial)

        def habilidad_especial(self):
            pass
