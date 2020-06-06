from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QWidget
from frontend.inicio import VentanaInicio
from frontend.ventanajuego import VentanaJuego, VentanaMapa
from frontend.resumen import VentanaResumen
from backend.backend import Logica
import sys

class Controller:

    def __init__(self):
        self.logica = Logica()
        self.ventana_inicio = VentanaInicio()
        self.ventana_juego = VentanaJuego()
        # botones de la ventana inicial
        self.ventana_inicio.senal_nuevo_juego.connect(self.nuevo_juego)
        self.ventana_inicio.senal_resumir_juego.connect(self.resumir_juego)
        # botones de la ventana de juego
        # boton para cerrar juego y volver a ventana de inicio:
        self.ventana_juego.senal_salir.connect(self.salir_juego)
        # conectamos la senal de pausa al backend para pausar procesos de logica:
        self.ventana_juego.senal_pausar.connect(self.logica.pausar_juego)
        self.ventana_juego.senal_comenzar.connect(self.logica.comenzar_juego)
        self.ventana_juego.senal_nuevo_juego.connect(self.logica.nuevo_juego)
        # senal para actualizar estadisticas:
        self.logica.senal_dinero.connect(self.ventana_juego.estadisticas.actualizar_dinero)
        self.logica.senal_reputacion.connect(self.ventana_juego.estadisticas.actualizar_reputacion)
        self.logica.senal_crear_objetos.connect(self.ventana_juego.mapa.sprites_nuevo_juego)
        # senales de la VentanaMapa para verificar compras en la tienda:
        self.ventana_juego.mapa.senal_drag.connect(self.logica.verificar_compra)
        self.logica.senal_compra_verificada.connect(self.ventana_juego.mapa.nuevo_sprite)
        # Senales asociadas al movimiento de miuenzo:
        self.ventana_juego.mapa.senal_estado_teclas.connect(self.logica.movimiento_miuenzo)
        self.logica.senal_mover_miuenzo.connect(self.ventana_juego.mapa.mover_miuenzo)
        # Senales asociadas a colisiones:
        self.logica.senal_colision_chef.connect(self.ventana_juego.mapa.colision_chef)
        self.logica.senal_colision_mesa.connect(self.ventana_juego.mapa.colision_mesa)
        # Senal asociada al chef:
        self.logica.senal_terminar_bocadillo.connect(self.ventana_juego.mapa.terminar_bocadillo)
        # senal llegada cliente:
        self.logica.senal_llegada_cliente.connect(self.ventana_juego.mapa.llegada_cliente)
        # senal salida de cliente:
        self.ventana_juego.mapa.senal_salida_cliente.connect(self.logica.salida_cliente)
        # senal fin de ronda:
        self.logica.senal_acabar_ronda.connect(self.resumen)


        self.ventana_inicio.show()

    def nuevo_juego(self):
        self.ventana_inicio.hide()
        self.ventana_juego.nuevo_juego()
        self.ventana_juego.show()

    def resumir_juego(self):
        ''' Funcion para partir desde un juego previamente guardado '''
        pass

    def resumen(self, ronda, c_perdidos, c_atendidos, dinero, rep):
        # al termino de ronda instanciamos una ventana de resumen
        # con las estadisticas:
        self.ventana_resumen = VentanaResumen(ronda, c_perdidos,
            c_atendidos, dinero, rep)
        self.ventana_resumen.senal_continuar.connect(self.continuar_ronda)
        self.ventana_resumen.senal_guardar.connect(self.guardar_ronda)
        self.ventana_resumen.senal_salir.connect(self.salir_juego)
        self.ventana_resumen.show()
        self.ventana_juego.setEnabled(False)
        # actualizamos la informacion en ventana estadisticas en caso de que
        # se continue jugando
        self.ventana_juego.estadisticas.actualizar_reputacion(rep)
        self.ventana_juego.estadisticas.actualizar_dinero(dinero)

    def salir_juego(self):
        sys.exit()
        # self.ventana_juego.deleteLater()
        # self.ventana_inicio.deleteLater()

    def continuar_ronda(self):
        self.ventana_juego.setEnabled(True)
        self.ventana_juego.activar_pre_ronda()
        self.ventana_resumen.deleteLater()

    def guardar_ronda(self):
        self.logica.dccafe.guardar_datos()
        self.ventana_resumen.deleteLater()
        self.ventana_juego.hide()
        self.ventana_inicio.show()
