
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QMimeData, pyqtSignal, QTimer, QObject
from PyQt5.QtGui import QDrag, QPixmap
from PyQt5.QtWidgets import QPushButton, QWidget, QApplication
from PARAMETROS import (
    VEL_MOVIMIENTO, TIMER_INTERVAL, PLATOS_EXPERTO, PLATOS_INTERMEDIO,
    TIEMPO_ESPERA_APURADO, TIEMPO_ESPERA_RELAJADO
)
from random import randint
import os

# implementacion simple de un QLabel que se puede dragear
class DragLabel(QLabel):
    def __init__(self, tipo, parent):
        super().__init__(parent)
        self.tipo = tipo
        self.habil = True

    def mouseMoveEvent(self, e):
        if self.habil:
            mimeData = QMimeData()
            mimeData.setText(f'{self.tipo},{self.pixmap().width()},'
                            +f'{self.pixmap().height()}')
            drag = QDrag(self)
            if self.pixmap():
                drag.setPixmap(self.pixmap())
            drag.setMimeData(mimeData)
            drag.setHotSpot(e.pos())
            drag.exec_(Qt.MoveAction)

    def setEnabled(self, bool):
        self.habil = bool

class MiuEnzo(QLabel):

    def __init__(self, tipo, parent, *args, **kwargs):
        super().__init__(tipo, parent)
        self.ocupado = 0 # si tiene un plato o no
        self.__direccion = 0 # parte mirando hacia abajo
        self.__fase_mov = 2 # fase de la animacion de movimiento
        self.initUI()

    @property
    def fase_mov(self):
        return self.__fase_mov

    @fase_mov.setter
    def fase_mov(self, fase):
        if fase == 2:
            self.__fase_mov = 2
        elif self.__fase_mov == 2:
            self.__fase_mov = 0
        else:
            self.__fase_mov += 1

    @property
    def direccion(self):
        return self.__direccion

    @direccion.setter
    def direccion(self, tecla):
        if tecla == 83:
            self.__direccion = 0
        elif tecla == 87:
            self.__direccion = 1
        elif tecla == 68:
            self.__direccion = 2
        elif tecla == 65:
            self.__direccion = 3

    def cargar_pixmaps(self):
        self.qpixmaps = [
            [[QPixmap(os.path.join('sprites', 'mesero', 'down_01.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'down_03.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'down_02.png'))],
            [QPixmap(os.path.join('sprites', 'mesero', 'down_snack_01.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'down_snack_03.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'down_snack_02.png'))]],
            [[QPixmap(os.path.join('sprites', 'mesero', 'up_01.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'up_03.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'up_02.png'))],
            [QPixmap(os.path.join('sprites', 'mesero', 'up_snack_01.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'up_snack_03.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'up_snack_02.png'))]],
            [[QPixmap(os.path.join('sprites', 'mesero', 'right_01.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'right_03.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'right_02.png'))],
            [QPixmap(os.path.join('sprites', 'mesero', 'right_snack_01.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'right_snack_03.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'right_snack_02.png'))]],
            [[QPixmap(os.path.join('sprites', 'mesero', 'left_01.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'left_03.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'left_02.png'))],
            [QPixmap(os.path.join('sprites', 'mesero', 'left_snack_01.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'left_snack_03.png')),
            QPixmap(os.path.join('sprites', 'mesero', 'left_snack_02.png'))]]
                ]

    def actualizar_pixmaps(self):
        ''' funcion asociada al timer interno '''
        pixmap = self.qpixmaps[self.direccion][self.ocupado][self.fase_mov]
        self.setPixmap(pixmap)

    def initUI(self):
        # pixmap = QPixmap('sprites/mesero/otros/mesere_down_01.png')
        self.cargar_pixmaps()
        self.timer_pixmaps = QTimer() # timer que se encarga de cambiar los sprites
        self.timer_pixmaps.setInterval(100) # 10 animaciones por segundo
        self.timer_pixmaps.timeout.connect(self.actualizar_pixmaps)
        self.timer_pixmaps.start()

    def resetear(self):
        self.ocupado = 0
        self.__direccion = 0
        self.actualizar_pixmaps()

    def agarrar_bocadillo(self, bocadillo):
        self.ocupado = 1
        self.bocadillo = bocadillo

    def soltar_bocadillo(self):
        self.ocupado = 0
        return self.bocadillo

class Chef(QLabel):

    def __init__(self, parent, posicion_x, posicion_y, nivel = 1,
                    platos_preparados = 0):
        super().__init__(parent)
        self.nivel = nivel
        self.platos_preparados = int(platos_preparados)
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        # atributo cocinando puede ser 0, 1 o 2, que significa en espera,
        # cocinando y listo, respectivamente.
        self.cocinando = 0
        ''' temporal, modificar'''
        self.tiempo_cocina = 10000
        self.__fase_animacion = 0 # atributo usado para ciclar los sprites al cocinar
        self.initUI()

    @property
    def platos_preparados(self):
        return self.__platos_preparados

    @platos_preparados.setter
    def platos_preparados(self, sum):
        self.__platos_preparados = sum
        if self.__platos_preparados > PLATOS_INTERMEDIO:
            self.nivel = 2
        elif self.__platos_preparados > PLATOS_EXPERTO:
            self.nivel = 3


    @property
    def fase_animacion(self):
        return self.__fase_animacion

    @fase_animacion.setter
    def fase_animacion(self, n):
        self.__fase_animacion = n
        if self.__fase_animacion > 4:
            self.__fase_animacion = 0

    def cargar_pixmaps(self):
        self.qpixmaps = {
            'esperando': QPixmap(os.path.join('sprites', 'chef', 'meson_01.png')),
            'listo': QPixmap(os.path.join('sprites', 'chef', 'meson_16.png')),
            'cocinando': [QPixmap(os.path.join('sprites', 'chef', 'meson_13.png')),
                        QPixmap(os.path.join('sprites', 'chef', 'meson_15.png')),
                        QPixmap(os.path.join('sprites', 'chef', 'meson_14.png')),
                        QPixmap(os.path.join('sprites', 'chef', 'meson_15.png')),
                        QPixmap(os.path.join('sprites', 'chef', 'meson_13.png'))]
        }

    def initUI(self):
        self.cargar_pixmaps()
        pixmap = self.qpixmaps['esperando']
        self.setPixmap(pixmap)
        self.move(self.posicion_x, self.posicion_y)
        self.resize(pixmap.width(), pixmap.height())
        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.cocinar)
        self.show()

    def resetear(self):
        self.cocinando = 0
        self.setPixmap(self.qpixmaps['esperando'])

    def cocinar(self):
        self.fase_animacion += 1
        self.setPixmap(self.qpixmaps['cocinando'][self.fase_animacion])

    def pausar(self, bool):
        if not bool and self.cocinando == 1:
            # si esta cocinando reanudamos timer de animacioness
            self.timer.start()
        else:
            self.timer.stop()

    def empezar_bocadillo(self):
        self.cocinando = 1
        self.timer.start()

    def terminar_bocadillo(self):
        self.cocinando = 2 # bocadillo listo
        self.bocadillo = 'bocadillo :)' # no alcance a modelar el bocadillo :(
        self.timer.stop()
        self.setPixmap(self.qpixmaps['listo'])
        self.platos_preparados += 1

    def entregar_bocadillo(self):
        self.cocinando = 0 # listo para empezar otro bocadillo
        self.setPixmap(self.qpixmaps['esperando'])
        return self.bocadillo

class Mesa(QLabel):

    def __init__(self, parent, posicion_x, posicion_y):
        super().__init__(parent)
        self.posicion_x = posicion_x
        self.posicion_y = posicion_y
        self.ocupado = False # mesa parte sin clientes
        self.__cliente = None
        self.initUI()

    @property
    def cliente(self):
        return self.__cliente

    @cliente.setter
    def cliente(self, cliente):
        if cliente is not None:
            self.__cliente = cliente
            self.ocupado = True

        elif cliente is None:
            if self.__cliente is not None:
                self.__cliente.deleteLater()
            self.__cliente = None
            self.ocupado = False

    def initUI(self):
        self.pixmap = QPixmap(os.path.join('sprites', 'mapa', 'accesorios',
                                        'silla_mesa_roja.png'))
        self.setPixmap(self.pixmap)
        # los valores en move() los saque experimentalmente, son los que mejor
        # aproximan el lugar correcto donde el usuario hace drop:
        self.move(self.posicion_x, self.posicion_y)
        self.resize(self.pixmap.width(), self.pixmap.height())
        self.show()

    def resetear(self):
        self.ocupado = False
        self.cliente = None

    def recibir_bocadillo(self, bocadillo):
        pixmap = bocadillo.pixmap()
        self.bocadillo = bocadillo


class Cliente(QLabel):

    scale = [30, 30] # pixmap scale

    def __init__(self, parent):
        super().__init__(parent)
        # estados: normal (0), enojado (1), feliz (2)
        self.estado = 0 # normal
        self.tipo = 'apurado' '''sacar hardcode'''
        self.initUI()

    def cargar_pixmaps(self):
        self.qpixmaps = [
            [QPixmap(os.path.join('sprites', 'clientes', 'hamster', 'hamster_01.png')),
            QPixmap(os.path.join('sprites', 'clientes', 'hamster', 'hamster_19.png')),
            QPixmap(os.path.join('sprites', 'clientes', 'hamster', 'hamster_39.png'))],
            [QPixmap(os.path.join('sprites', 'clientes', 'hamster', 'hamster_02.png')),
            QPixmap(os.path.join('sprites', 'clientes', 'hamster', 'hamster_20.png')),
            QPixmap(os.path.join('sprites', 'clientes', 'hamster', 'hamster_35.png'))],
            [QPixmap(os.path.join('sprites', 'clientes', 'perro', 'perro_01.png')),
            QPixmap(os.path.join('sprites', 'clientes', 'perro', 'perro_14.png')),
            QPixmap(os.path.join('sprites', 'clientes', 'perro', 'perro_10.png'))],
            [QPixmap(os.path.join('sprites', 'clientes', 'perro', 'perro_02.png')),
            QPixmap(os.path.join('sprites', 'clientes', 'perro', 'perro_15.png')),
            QPixmap(os.path.join('sprites', 'clientes', 'perro', 'perro_12.png'))]
                ]

    def initUI(self):
        self.cargar_pixmaps()
        self.pixmap_index = randint(0, 3)
        pixmap = self.qpixmaps[self.pixmap_index][self.estado].scaled(*self.scale)
        self.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

        if self.tipo == 'apurado':
            self.tiempo_espera = TIEMPO_ESPERA_APURADO
        else:
            self.tiempo_espera = TIEMPO_ESPERA_RELAJADO
        self.show()

    def enojarse(self):
        if self.estado != 2:
            self.estado = 1
            pixmap = self.qpixmaps[self.pixmap_index][self.estado]
            self.setPixmap(pixmap.scaled(*self.scale))

    def recibir_bocadillo(self, bocadillo):
        self.estado = 2
        pixmap = self.qpixmaps[self.pixmap_index][self.estado]
        self.setPixmap(pixmap.scaled(*self.scale))



class Bocadillo(QObject):
    def __init__(self, calidad):
        self.precio = PRECIO_BOCADILLO
        self.calidad = calidad

    def initUI(self):
        pass
