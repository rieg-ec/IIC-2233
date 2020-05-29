from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget
from frontend.inicio import VentanaInicio
from frontend.ventanajuego import VentanaJuego, VentanaMapa
from frontend.resumen import VentanaResumen
from backend.backend import Logica

class Controller:

    def __init__(self):
        self.logica = Logica()

        self.inicio = VentanaInicio()
        self.ventana_juego = VentanaJuego()
        # botones de la ventana inicial
        self.inicio.senal_nuevo_juego.connect(self.nuevo_juego)
        self.inicio.senal_resumir_juego.connect(self.resumir_juego)
        # botones de la ventana de juego
        # boton para cerrar juego y volver a ventana de inicio:
        self.ventana_juego.senal_salir.connect(self.salir_juego)
        self.inicio.show()
        # self.resumen()
        # senales de la VentanaMapa para verificar compras en la tienda:
        self.ventana_juego.mapa.senal_drag.connect(self.logica.verificar_compra)
        self.logica.senal_compra_verificada.connect(self.ventana_juego.mapa.nuevo_sprite)
        # Senales asociadas al movimiento de miuenzo:
        self.ventana_juego.mapa.senal_estado_teclas.connect(self.logica.movimiento_miuenzo)
        self.logica.senal_mover_miuenzo.connect(self.ventana_juego.mapa.mover_miuenzo)

    def nuevo_juego(self):
        self.inicio.hide()
        self.ventana_juego.show()

    def resumir_juego(self):
        print('resumiendo juego')

    def resumen(self):
        ronda = 4
        clientes_perdidos = 10
        clientes_atendidos = 10
        dinero = 100
        reputacion = [4, 5]
        self.ventana_resumen = VentanaResumen(ronda, clientes_perdidos,
            clientes_atendidos, dinero, reputacion)
        self.ventana_resumen.show()

    def salir_juego(self):
        self.ventana_juego.hide()
        self.inicio.show()
