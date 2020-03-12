class Triangulo:
    def __init__(self, altura, base, lado1, lado2, lado3):
        self.altura = altura
        self.base = base
        self.lados = [lado1, lado2, lado3]

    def obtener_area(self):
        area = self.altura * self.base / 2
        return area

    def obtener_perimetro(self):
        perimetro = self.lados[0] + self.lados[1] + self.lados[2]
        return perimetro

    def es_equilatero(self):
        if (self.lados[0] == self.lados[1]) and (self.lados[1] == self.lados[2]):
            return True
        else:
            return False

    def __str__(self):
        return "Triangulo. lados: {}, {}, {}.".format(self.lados[0], self.lados[1], self.lados[2])



class Cuadrado:
    def __init__(self, lado):
        self.lado = lado

    def obtener_area(self):
        area = self.lado ** 2
        return area

    def obtener_perimetro(self):
        perimetro = self.lado * 4
        return perimetro

    def __str__(self):
        return "Cuadrado. Lados: {}".format(self.lado)
