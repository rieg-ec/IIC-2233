from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QObject, QTimer
from PyQt5.QtGui import QPixmap

from math import floor

from PARAMETROS import (
    PRECIO_BOCADILLO, DINERO_INICIAL, REPUTACION_INICIAL, REPUTACION_TOTAL,
    CHEFS_INICIALES, MESAS_INICIALES, CLIENTES_INICIALES
)

class DCCafe(QObject):
    def __init__(self):
        super().__init__()
        self.mesero = []
        self.mesas = []
        self.chefs = {} # platos_preparados: [x, y]
        # self.mesas = MESAS_INICIALES
        # self.chefs = CHEFS_INICIALES
        self.abierto = True
        self.__mesas_ocupadas = 0
        self.__reputacion = REPUTACION_INICIAL
        self.dinero = DINERO_INICIAL
        self.rondas_terminadas = 0

    @property
    def mesas_ocupadas(self):
        return self.__mesas_ocupadas

    @mesas_ocupadas.setter
    def mesas_ocupadas(self, valor):
        self.__mesas_ocupadas = valor
        if self.__mesas_ocupadas < 0:
            self.__mesas_ocupadas = 0

    @property
    def reputacion(self):
        return self.__reputacion

    @reputacion.setter
    def reputacion(self, valor):
        self.__reputacion = valor
        if self.__reputacion < 0:
            self.__reputacion = 0

    def calcular_reputacion(self):
        diferencia = floor(4*(self.pedidos_exitosos/self.pedidos_totales) - 2)
        self.reputacion += diferencia
        return self.reputacion

    def empezar_ronda(self):
        self.abierto = True
        self.ronda += 1
        self.pedidos_totales = 0
        self.pedidos_exitosos = 0

    def clientes_ronda(self):
        # calcular clientes que llegaran en la ronda
        return 5 * (1 + self.ronda)

    def guardar_datos(self):
        with open('datos.csv', 'w') as file:
            file.write(f'{self.dinero},{self.reputacion},{self.rondas_terminadas}')
            file.write(f'\n{",".join(key for key in self.chefs)}') # key: platos preparados
            file.close()

        with open('mapa.csv', 'w') as file:
            file.write(f'mesero,{self.mesero[0]},{self.mesero[1]}')
            for mesa in self.mesas:
                file.write(f'\nmesa,{mesa[0]},{mesa[1]}')
            for chef in self.chefs:
                # self.chefs es un diccionario
                file.write(f'\nchef,{self.chefs[chef][0]},{self.chefs[chef][1]}')
            file.close()

    def cargar_datos(self):
        # sacar datos de .csv y overridear atributos de constructor
        with open('datos.csv', 'r') as file:
            din, rep, rondas = file.readline().split(',')
            platos_preparados = file.readline().split(',')
            file.close()

        self.rondas_terminadas = self.ronda = int(rondas)
        self.dinero = int(din)
        self.reputacion = int(rep)

        with open('mapa.csv', 'r') as file:
            for line in file.readlines():
                tipo, x, y = line.split(',')
                tipo, x, y = tipo.replace('\n', ''),  int(x), int(y.replace('\n', ''))
                if tipo == 'chef':
                    self.chefs[platos_preparados.pop().replace('\n', '')] = [x, y]
                elif tipo == 'mesa':
                    self.mesas.append([x, y])
                elif tipo == 'mesero':
                    self.mesero = [x, y]
            file.close()
