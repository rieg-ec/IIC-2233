from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QLabel, QProgressBar, QLCDNumber
)
from PyQt5.QtCore import (
    pyqtSignal, QEvent, QMimeData, QTimer,
    QRect
)
from PyQt5 import QtCore
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QDropEvent
from frontend.utils_front import Chef, Mesa, MiuEnzo, DragLabel

from PARAMETROS import *


class VentanaMapa(QWidget):

    # senal que envia la informacion al backend sobre el drag:
    senal_drag = pyqtSignal(QDropEvent, list, QRect, QRect)
    # senal que envia informacion al backend sobre teclas presionadas,
    # la informacion enviada es un dict con el estado de las teclas, un dict con
    # referencia a la clase y la geometria de los labels (sin contar a miuenzo)
    # y un QRect con la geometria de miuenzo
    senal_estado_teclas = pyqtSignal(dict, list, QRect, QRect)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.teclas = {
            87: False,
            65: False,
            68: False,
            83: False,
        }
        # timer asociado a eventos de teclas:
        self.timer = QTimer()
        self.timer.setInterval(TIMER_INTERVAL)
        self.timer.timeout.connect(self.estado_teclas)
        self.timer.start()

        self.setAcceptDrops(True)
        # aqui guardaremos las entidades distintas a MiuEnzo:
        self.labels_entidades = []
        # aqui guardamos la geometria de los labels para no enviar tantos datos
        # al backend:
        self.geometry_labels = []

        pixmap_mapa = QPixmap('sprites/mapa/mapa_sin_borde_2.png')
        self.label_mapa = QLabel(self)
        self.label_mapa.setAlignment(QtCore.Qt.AlignCenter)
        self.label_mapa.setPixmap(pixmap_mapa.scaled(
            self.width(), self.height()))

        self.label_miuenzo = MiuEnzo('', self)
        '''sacar'''
        self.label_miuenzo.move(100, 100)

        ### Asignamos un label a los arboles del mapa:
        tamano_arboles = (0.05, 0.15) # parametro experimental
        self.label_arbol_1 = QLabel('', self)
        self.label_arbol_1.resize(self.width() * tamano_arboles[0],
                            self.height() * tamano_arboles[1])
        self.label_arbol_1.move(0, self.height() * 0.14)

        self.label_arbol_2 = QLabel('', self)
        self.label_arbol_2.resize(self.width() * tamano_arboles[0],
                            self.height() * tamano_arboles[1])
        self.label_arbol_2.move(self.width() - self.label_arbol_2.width(),
                                self.height() * 0.14)

        self.labels_entidades.extend([self.label_arbol_1, self.label_arbol_2])

        self.setFixedSize(self.size())

        ''' sacar '''
        self.setStyleSheet('background-color: red;')

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        # mandamos al backend informacion con el evento y los limites
        self.senal_drag.emit(e, *self.limites())

    # es llamada desde el backend cuando un drop es valido
    def nuevo_sprite(self, data):
        x, y = data['pos'].x(), data['pos'].y()
        if data['tipo'] == 'chef':
            self.nuevo_label = Chef(self, x, y)
        elif data['tipo'] == 'mesa':
            self.nuevo_label = Mesa(self, x, y)
        self.labels_entidades.append(self.nuevo_label)

    def keyPressEvent(self, e):
        if e.key() in self.teclas:
            self.teclas[e.key()] = True

    def keyReleaseEvent(self, e):
        if e.key() in self.teclas:
            self.teclas[e.key()] = False

    def estado_teclas(self):
        ''' Funcion asociada al QTimer'''
        # mandamos el estado de las teclas al backend si hay alguna presionada
        if any(self.teclas.values()):
            self.senal_estado_teclas.emit(self.teclas, *self.limites())

    def limites(self):
        ''' funcion que retorna la geometria/posicion de todos los objetos del
        mapa que pueden generar una colision'''
        labels = [i for i in self.labels_entidades]
        geometria_miuenzo = self.label_miuenzo.geometry()
        # para la dimension del mapa no tomamos en cuenta el borde superior
        # con ventanas
        borde_superior = self.height() * BORDE_SUPERIOR_MAPA
        dimensiones_mapa = QRect(0, borde_superior, self.width(),
                                self.height() - borde_superior)
        return labels, geometria_miuenzo, dimensiones_mapa

    def mover_miuenzo(self, dx, dy):
        ''' Esta funcion esta asociada a una senal en el backend'''
        self.label_miuenzo.move(self.label_miuenzo.pos().x() + dx,
                                self.label_miuenzo.pos().y() + dy)

    def actualizar_mesa(self, mesa):
        pass
        # mesa.actualizar_pixmap()
    def actualizar_chef(self, chef):
        pass
        # chef.actualizar_pixmap()

class VentanaEstadisticas(QWidget):

    senal_salir = pyqtSignal()
    senal_pausar = pyqtSignal()
    senal_comenzar = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):

        labels = {}
        vboxs = {}

        pixmap_dccafe = QPixmap('sprites/otros/logo_negro.png')
        labels['dccafe_icon'] = QLabel(self)
        labels['dccafe_icon'].setAlignment(QtCore.Qt.AlignCenter)
        labels['dccafe_icon'].setPixmap(pixmap_dccafe.scaled(
                                            labels['dccafe_icon'].width(),
                                            labels['dccafe_icon'].height(),
                                            ))
        # Layout principal
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(labels['dccafe_icon'])

        # Estara compuesto de vertical layouts
        vboxs['ronda'] = QVBoxLayout() # Layout con el numero de ronda y opcion de comenzar
        labels['ronda-text'] = QLabel(self) #
        labels['ronda-text'].setText('ronda 4')

        vboxs['ronda'].addStretch(2)
        vboxs['ronda'].addWidget(labels['ronda-text'])

        labels['ronda-comenzar'] = QPushButton('Comenzar', self)
        labels['ronda-comenzar'].clicked.connect(self.comenzar)

        vboxs['ronda'].addWidget(labels['ronda-comenzar'])

        hbox.addStretch(1)
        hbox.addLayout(vboxs['ronda'])

        # El vertical layout con reputacion y dinero estara compuesto de
        # horizontal layouts
        vboxs['reputacion-dinero'] = QVBoxLayout()

        # Horizontal layout con informacion sobre reputacion
        reputacion_hbox = QHBoxLayout()

        labels['reputacion-text'] = QLabel('Reputacion', self)
        reputacion_hbox.addWidget(labels['reputacion-text'], 1)

        labels['reputacion-bar'] = QProgressBar(self)
        reputacion_hbox.addWidget(labels['reputacion-bar'])

        vboxs['reputacion-dinero'].addLayout(reputacion_hbox)

        # Horizontal layout con informacion sobre dinero
        dinero_hbox = QHBoxLayout()

        labels['dinero-text'] = QLabel('Dinero', self)
        dinero_hbox.addWidget(labels['dinero-text'], 1)

        labels['dinero-display'] = QLCDNumber(self)
        dinero_hbox.addWidget(labels['dinero-display'])

        vboxs['reputacion-dinero'].addLayout(dinero_hbox)

        hbox.addStretch(1)
        hbox.addLayout(vboxs['reputacion-dinero'])

        # Vertical layout con boton de pausa y salir
        vboxs['pausar-salir'] = QVBoxLayout()

        labels['pausar'] = QPushButton('Pausar', self)
        labels['pausar'].clicked.connect(self.pausar)
        vboxs['pausar-salir'].addWidget(labels['pausar'])

        labels['salir'] = QPushButton('Salir', self)
        labels['salir'].clicked.connect(self.salir)
        vboxs['pausar-salir'].addWidget(labels['salir'])

        hbox.addStretch(1)
        hbox.addLayout(vboxs['pausar-salir'])

        self.setLayout(hbox)
        self.setStyleSheet('background-color: red;')

    def comenzar(self):
        self.senal_comenzar.emit()

    def pausar(self):
        self.senal_pausar.emit()

    def salir(self):
        self.senal_salir.emit()


class VentanaTienda(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        label_tienda = QLabel('TIENDA', self)
        label_tienda.setAlignment(QtCore.Qt.AlignCenter)

        label_precio_chef = QLabel(f'{PRECIO_CHEF} $', self)
        label_precio_chef.setAlignment(QtCore.Qt.AlignCenter)
        pixmap_chef = QPixmap('sprites/chef/meson_01.png')
        # Override de QLabel para hacerlo drageable
        label_chef = DragLabel('chef', self)
        label_chef.setPixmap(pixmap_chef)
        label_chef.resize(pixmap_chef.width(), pixmap_chef.height())
        label_chef.setAlignment(QtCore.Qt.AlignCenter)

        label_precio_mesa = QLabel(f'{PRECIO_MESA} $')
        label_precio_mesa.setAlignment(QtCore.Qt.AlignCenter)
        pixmap_mesa = QPixmap('sprites/mapa/accesorios/silla_mesa_roja.png')
        # Override de QLabel para hacerlo drageable
        label_mesa = DragLabel('mesa', self)
        label_mesa.setPixmap(pixmap_mesa)
        label_mesa.setAlignment(QtCore.Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(label_tienda)
        vbox.addStretch(2)
        vbox.addWidget(label_chef)
        vbox.addWidget(label_precio_chef)
        vbox.addStretch(2)
        vbox.addWidget(label_mesa)
        vbox.addWidget(label_precio_mesa)
        vbox.addStretch(2)
        self.setLayout(vbox)

        self.setStyleSheet('background-color: red;')

class VentanaJuego(QWidget):

    senal_salir = pyqtSignal()
    senal_pausar = pyqtSignal()
    senal_comenzar = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setGeometry(*GM_VENTANA_JUEGO)

        self.setAcceptDrops(True)

        self.estadisticas = VentanaEstadisticas()
        self.mapa = VentanaMapa()
        self.tienda = VentanaTienda()

        self.estadisticas.senal_pausar.connect(self.pausar)
        self.estadisticas.senal_comenzar.connect(self.comenzar)
        self.estadisticas.senal_salir.connect(self.salir)

        vbox = QVBoxLayout()

        vbox.addStretch(0.1)
        vbox.addWidget(self.estadisticas, 1)

        hbox = QHBoxLayout()
        hbox.addStretch(0.1)
        hbox.addWidget(self.mapa)
        hbox.addWidget(self.tienda)
        hbox.addStretch(0.1)

        vbox.addLayout(hbox, 5)

        self.setLayout(vbox)

        self.setFixedSize(self.size())
        self.setStyleSheet('background-color: green;')


    def pausar(self):
        self.senal_pausar.emit()

    def comenzar(self):
        self.senal_comenzar.emit()

    def salir(self):
        self.senal_salir.emit()

    # Key events no son capturados por otras ventanas hijas, por lo que
    # lo implemente en la ventana madre, y esta llama al metodo de la clase
    # miuenzo
    def keyPressEvent(self, e):
        self.mapa.keyPressEvent(e)

    def keyReleaseEvent(self, e):
        self.mapa.keyReleaseEvent(e)
    '''sacar'''
    def mousePressEvent(self, e):
        print('\n####')
        print(e.pos().x() - 22, e.pos().y() - 110)
        print((e.pos().x() - 22) / self.mapa.width(), (e.pos().y() - 110) / self.mapa.height())
