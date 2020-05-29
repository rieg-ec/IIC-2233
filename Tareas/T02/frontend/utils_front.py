
from PyQt5.QtWidgets import QLabel

from PyQt5.QtCore import Qt, QMimeData, QThread, pyqtSignal
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication
from PARAMETROS import VEL_MOVIMIENTO

# implementacion simple de un QLabel que se puede dragear
class DragLabel(QLabel):
    def __init__(self, tipo, parent):
        super().__init__(parent)
        self.tipo = tipo

    def mouseMoveEvent(self, e):
        mimeData = QMimeData()
        mimeData.setText(f'{self.tipo},{self.pixmap().width()},'
                        +f'{self.pixmap().height()}')
        drag = QDrag(self)
        if self.pixmap():
            drag.setPixmap(self.pixmap())
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos())

        dropAction = drag.exec_(Qt.MoveAction)


class MiuEnzo(QLabel):

    senal_colision = pyqtSignal(int, int)

    def __init__(self, tipo, parent, *args, **kwargs):
        super().__init__(tipo, parent)
        self.initUI()

    def initUI(self):
        pixmap = QPixmap('sprites/mesero/otros/mesere_down_01.png')
        self.setPixmap(pixmap)

class Chef(QLabel):
    senal_colision_miuenzo = pyqtSignal()
    senal_iniciar_timer = pyqtSignal()

    def __init__(self, parent, posicion_x, posicion_y, nivel = 1,
                    platos_preparados = 0):
        super().__init__(parent)
        self.nivel = nivel
        self.platos_preparados = platos_preparados
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.estado = 'esperando'
        self.initUI()

    def initUI(self):
        pixmap = QPixmap('sprites/chef/meson_01.png')
        self.setPixmap(pixmap)
        self.move(self.posicion_x, self.posicion_y)
        self.resize(pixmap.width(), pixmap.height())
        self.show()

    def colision(self):
        ''' funcion asociada a senal del backend '''
        if self.estado == 'esperando':
            self.estado = 'cocinando'

        elif self.estado == 'listo':
            # senal que gatilla que miuenzo recoja el plato:
            self.senal_colision_miuenzo.emit()

    def timer_cocina(self):
        senal_iniciar_timer.emit()


class Mesa(QLabel):

    def __init__(self, parent, posicion_x, posicion_y):
        super().__init__(parent)
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.initUI()

    def initUI(self):
        pixmap = QPixmap('sprites/mapa/accesorios/silla_mesa_roja.png')
        self.setPixmap(pixmap)
        # los valores en move() los saque experimentalmente, son los que mejor
        # aproximan el lugar correcto donde el usuario hace drop:
        self.move(self.posicion_x, self.posicion_y)
        self.resize(pixmap.width(), pixmap.height())
        self.show()
