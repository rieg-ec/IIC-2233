from PyQt5.QtCore import pyqtSignal, QObject, QRect
from PyQt5.QtWidgets import QLabel
from PARAMETROS import VEL_MOVIMIENTO

class Logica(QObject):

    senal_compra_verificada = pyqtSignal(dict)
    senal_mover_miuenzo = pyqtSignal(int, int)

    senal_colision_chef = pyqtSignal(QLabel)
    senal_colision_mesa = pyqtSignal(QLabel)

    def __init__(self):
        super().__init__()

    def verificar_compra(self, e, labels, geometria_miuenzo, dimensiones_mapa):
        tipo, width, height = e.mimeData().text().split(',')
        qrect_drop = QRect(e.pos().x(), e.pos().y(), int(width), int(height))
        valido = True

        if not dimensiones_mapa.contains(qrect_drop):
            valido = False

        elif qrect_drop.intersects(geometria_miuenzo):
            valido = False

        else:
            for label in labels:
                if label.geometry().intersects(qrect_drop):
                    valido = False

        if valido:
            data = {'tipo': tipo,
                    'pos': e.pos()}
            self.senal_compra_verificada.emit(data)


    def movimiento_miuenzo(self, teclas, labels,
                            geometria_miuenzo, dimensiones_mapa):
        ''' En caso de que el movimiento de miuenzo sea valido, mandamos senal
        a VentanaMapa'''
        # guardamos la posicion de miuenzo antes del movimiento
        # tecla W:
        if teclas[87]:
            dx = 0
            dy = - VEL_MOVIMIENTO
        # tecka A:
        elif teclas[65]:
            dx = - VEL_MOVIMIENTO
            dy = 0
        # tecla D:
        elif teclas[68]:
            dx = VEL_MOVIMIENTO
            dy = 0
        # tecla S:
        elif teclas[83]:
            dx = 0
            dy = VEL_MOVIMIENTO

        nueva_posicion = QRect(geometria_miuenzo.x() + dx, geometria_miuenzo.y() + dy,
                                geometria_miuenzo.width(), geometria_miuenzo.height())
        interseccion = False
        for label in labels:
            if nueva_posicion.intersects(label.geometry()):
                interseccion = True
                if label.__class__.__name__ == 'Chef':
                    self.senal_colision_chef.emit(label)
                elif label.__class__.__name__ == 'Mesa':
                    self.senal_colision_mesa.emit(label)

            if not dimensiones_mapa.contains(nueva_posicion):
                interseccion = True

        if not interseccion:
            self.senal_mover_miuenzo.emit(dx, dy)
