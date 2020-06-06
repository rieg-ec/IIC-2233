from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal, QMimeData, QTimer, QRect
from PyQt5 import QtCore
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap, QDropEvent
from frontend.utils_front import Chef, Mesa, MiuEnzo, DragLabel, Cliente

from PARAMETROS import *
from random import choice
import os


class VentanaMapa(QWidget):

    # senal que envia la informacion al backend sobre el drag:
    senal_drag = pyqtSignal(QDropEvent, list, QLabel, QRect)
    # senal que envia informacion al backend sobre teclas presionadas,
    # la informacion enviada es un dict con el estado de las teclas, un dict con
    # referencia a la clase y la geometria de los labels (sin contar a miuenzo)
    # y un QRect con la geometria de miuenzo
    senal_estado_teclas = pyqtSignal(dict, list, QLabel, QRect)
    senal_salida_cliente = pyqtSignal(QLabel)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()
        self.pre_ronda = False
        self.pausa = False
        self.teclas = {
            87: False,
            65: False,
            68: False,
            83: False,
        }
        # timer que revisa estado de las teclas:
        self.timer_teclas = QTimer()
        self.timer_teclas.setInterval(TIMER_INTERVAL)
        self.timer_teclas.timeout.connect(self.estado_teclas)
        self.timer_teclas.start()

    def initUI(self):
        self.setAcceptDrops(True)
        # aqui guardaremos las entidades distintas a MiuEnzo:
        self.labels_entidades = []
        self.clientes = []

        pixmap_mapa = QPixmap(os.path.join('sprites', 'mapa',
                                'mapa_sin_borde_2.png'))
        self.label_mapa = QLabel(self)
        self.label_mapa.setAlignment(QtCore.Qt.AlignCenter)
        self.label_mapa.setPixmap(pixmap_mapa.scaled(
            self.width(), self.height()))


        ### Asignamos un label a los arboles del mapa:
        tamano_arboles = (0.05, 0.15) # parametro experimental
        label_arbol_1 = QLabel('', self)
        label_arbol_1.resize(self.width() * tamano_arboles[0],
                            self.height() * tamano_arboles[1])
        label_arbol_1.move(0, self.height() * 0.14)

        label_arbol_2 = QLabel('', self)
        label_arbol_2.resize(self.width() * tamano_arboles[0],
                            self.height() * tamano_arboles[1])
        label_arbol_2.move(self.width() - label_arbol_2.width(),
                                self.height() * 0.14)

        self.labels_entidades.extend([label_arbol_1, label_arbol_2])

        self.label_miuenzo = MiuEnzo('', self)

        self.setFixedSize(self.size())

    def sprites_nuevo_juego(self, miuenzo, mesas, chefs):
        self.label_miuenzo.move(miuenzo[0], miuenzo[1])

        for mesa in mesas:
            label = Mesa(self, mesa[0], mesa[1])
            self.labels_entidades.append(label)

        for chef in chefs:
            platos = chef # key es platos preparados
            x, y = chefs[chef]
            label = Chef(self, x, y, platos_preparados=platos)
            self.labels_entidades.append(label)


    def activar_pre_ronda(self, bool):
        ''' funcion para entrar y salir de la pre-ronda, bool
        nos indica que hacer '''
        self.pre_ronda = bool
        if bool:
            self.timer_teclas.stop()
            # reseteamos las teclas para que no se quede guardada ninguna
            # como presionada, causando bugs:
            self.teclas = {
                87: False,
                65: False,
                68: False,
                83: False,
            }
            self.label_miuenzo.resetear()
            for label in self.labels_entidades:
                if label.__class__.__name__ != 'QLabel':
                    # objetos obstaculo no tienen metodo resetear
                    label.resetear()
        else:
            self.timer_teclas.start()


    def pausar(self, bool):
        # debemos detener las animaciones y dejar de procesar inputs:
        self.pausa = bool
        for label in self.labels_entidades:
            if label.__class__.__name__ == 'Chef':
                label.pausar(bool)

    def dragEnterEvent(self, e):
        e.accept()

    def dropEvent(self, e):
        # mandamos al backend informacion con el evento y los limites
        self.senal_drag.emit(e, *self.limites())

    def nuevo_sprite(self, data):
        ''' funcion asociada a senal en el backend '''
        # la senal es emitida cuando el drop es valido y manda las coordenadas
        x, y = data['pos'].x(), data['pos'].y()
        if data['tipo'] == 'chef':
            nuevo_label = Chef(self, x, y)
        elif data['tipo'] == 'mesa':
            nuevo_label = Mesa(self, x, y)

        self.labels_entidades.append(nuevo_label)

    def keyPressEvent(self, e):
        if not self.pausa and not self.pre_ronda:
            # solo procesamos keyEvents en etapa de ronda
            if e.key() in self.teclas:
                self.teclas[e.key()] = True

    def keyReleaseEvent(self, e):
        if e.key() in self.teclas:
            self.teclas[e.key()] = False

    def estado_teclas(self):
        ''' Funcion asociada al QTimer'''
        # mandamos el estado de las teclas al backend si hay alguna presionada
        # y ahi vemos si miuenzo se desplaza o no
        if any(self.teclas.values()):
            self.senal_estado_teclas.emit(self.teclas, *self.limites())
        # ademas mandamos una senal siempre que se encarga de revisar que pixmap
        # debe tener miuenzo
        else:
            # si ninguna tecla esta presionada, debemos hacer que miuenzo se
            # quede quieto:
            self.label_miuenzo.fase_mov = 2 # idle

    def limites(self):
        ''' funcion que retorna la geometria/posicion de todos los objetos del
        mapa que pueden generar una colision'''
        labels = [i for i in self.labels_entidades]
        # para la dimension del mapa no tomamos en cuenta el borde superior
        # con ventanas
        borde_superior = self.height() * BORDE_SUPERIOR_MAPA
        dimensiones_mapa = QRect(0, borde_superior, self.width(),
                                self.height() - borde_superior)
        return labels, self.label_miuenzo, dimensiones_mapa

    def mover_miuenzo(self, dx, dy, tecla):
        ''' Esta funcion esta asociada a una senal en el backend'''
        self.label_miuenzo.move(self.label_miuenzo.pos().x() + dx,
                                self.label_miuenzo.pos().y() + dy)
        # independiente del valor de dx y dy, miuenzo se mueve segun
        # la tecla presionada, por lo que actualizamos su direccion:
        self.label_miuenzo.direccion = tecla
        self.label_miuenzo.fase_mov += 1 # siguiente animacion

    def colision_mesa(self, mesa):
        cliente = mesa.cliente
        bocadillo = self.label_miuenzo.soltar_bocadillo() # retorna el bocadillo
        cliente.recibir_bocadillo(bocadillo)

    def colision_chef(self, chef, accion):
        if accion == 1:
            self.empezar_bocadillo(chef)

        elif accion == 0:
            self.entregar_bocadillo(chef)

    def entregar_bocadillo(self, chef):
        bocadillo = chef.entregar_bocadillo()
        self.label_miuenzo.agarrar_bocadillo(bocadillo)

    def empezar_bocadillo(self, chef):
        chef.empezar_bocadillo()
        # mandamos una senal al reloj para que inicie un timer
        # senal_timer.emit(chef)

    def terminar_bocadillo(self, chef):
        ''' funcion asociada a senal en el backend'''
        chef.terminar_bocadillo()

    def llegada_cliente(self, tmp_enojarse, tmp_irse):
        # escogemos una mesa vacia:
        mesa = choice([label for label in self.labels_entidades if
                    label.__class__.__name__ == 'Mesa' and not label.ocupado])
        cliente = Cliente(self)
        cliente.move(mesa.pos().x(), mesa.pos().y())
        self.clientes.append(cliente)

        mesa.cliente = cliente

        tmp_enojarse.timeout.connect(cliente.enojarse)
        tmp_enojarse.setInterval(cliente.tiempo_espera)

        irse = lambda: self.salida_cliente(cliente)
        tmp_irse.timeout.connect(irse)
        tmp_irse.setInterval(cliente.tiempo_espera * 2)

        tmp_enojarse.start(), tmp_irse.start()

    def salida_cliente(self, cliente):
        self.senal_salida_cliente.emit(cliente)
        for mesa in [label for label in self.labels_entidades if
                    label.__class__.__name__ == 'Mesa']:

            if mesa.cliente == cliente:
                mesa.cliente = None


class VentanaEstadisticas(QWidget):

    senal_salir = pyqtSignal()
    senal_pausar = pyqtSignal(bool)
    senal_comenzar = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pausa = False
        self.initUI()

    def initUI(self):

        self.labels = {}
        vboxs = {}

        pixmap_dccafe = QPixmap(os.path.join('sprites', 'otros', 'logo_negro.png'))
        self.labels['dccafe_icon'] = QLabel(self)
        self.labels['dccafe_icon'].setAlignment(QtCore.Qt.AlignCenter)
        self.labels['dccafe_icon'].setPixmap(pixmap_dccafe.scaled(
                                            self.labels['dccafe_icon'].width(),
                                            self.labels['dccafe_icon'].height(),
                                            ))
        # Layout principal
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self.labels['dccafe_icon'])

        # Estara compuesto de vertical layouts
        vboxs['ronda'] = QVBoxLayout() # Layout con el numero de ronda y opcion de comenzar
        self.labels['ronda-text'] = QLabel(self) #
        self.labels['ronda-text'].setText('ronda 4')

        vboxs['ronda'].addStretch(2)
        vboxs['ronda'].addWidget(self.labels['ronda-text'])

        self.labels['ronda-comenzar'] = QPushButton('Comenzar', self)
        self.labels['ronda-comenzar'].clicked.connect(self.comenzar)
        self.labels['ronda-comenzar'].setEnabled(False)

        vboxs['ronda'].addWidget(self.labels['ronda-comenzar'])

        hbox.addStretch(1)
        hbox.addLayout(vboxs['ronda'])

        # El vertical layout con reputacion y dinero estara compuesto de
        # horizontal layouts
        vboxs['reputacion-dinero'] = QVBoxLayout()

        # Horizontal layout con informacion sobre reputacion
        reputacion_hbox = QHBoxLayout()

        self.labels['reputacion-text'] = QLabel('Reputacion', self)
        reputacion_hbox.addWidget(self.labels['reputacion-text'], 1)

        # self.labels['reputacion-bar'] = QProgressBar(self)
        self.labels['reputacion-bar'] = QLabel('5/5', self)
        reputacion_hbox.addWidget(self.labels['reputacion-bar'])

        vboxs['reputacion-dinero'].addLayout(reputacion_hbox)

        # Horizontal layout con informacion sobre dinero
        dinero_hbox = QHBoxLayout()

        self.labels['dinero-text'] = QLabel('Dinero', self)
        dinero_hbox.addWidget(self.labels['dinero-text'], 1)

        self.labels['dinero-display'] = QLabel('0', self)
        dinero_hbox.addWidget(self.labels['dinero-display'])

        vboxs['reputacion-dinero'].addLayout(dinero_hbox)

        hbox.addStretch(1)
        hbox.addLayout(vboxs['reputacion-dinero'])

        # Vertical layout con boton de pausa y salir
        vboxs['pausar-salir'] = QVBoxLayout()

        self.labels['pausar'] = QPushButton('Pausar', self)
        self.labels['pausar'].clicked.connect(self.pausar)
        vboxs['pausar-salir'].addWidget(self.labels['pausar'])

        self.labels['salir'] = QPushButton('Salir', self)
        self.labels['salir'].clicked.connect(self.salir)
        vboxs['pausar-salir'].addWidget(self.labels['salir'])

        hbox.addStretch(1)
        hbox.addLayout(vboxs['pausar-salir'])

        self.setLayout(hbox)

    def actualizar_dinero(self, dinero):
        self.labels['dinero-display'].setText(f'{dinero}')

    def actualizar_reputacion(self, rep):
        self.labels['reputacion-bar'].setText(f'{rep}/5')

    def activar_pre_ronda(self):
        self.labels['ronda-comenzar'].setEnabled(True)

    def comenzar(self):
        self.senal_comenzar.emit()
        self.labels['ronda-comenzar'].setEnabled(False)

    def pausar(self):
        if self.pausa:
            self.pausa = False
            self.senal_pausar.emit(False)
            self.labels['pausar'].setText('Pausar')
        else:
            self.pausa = True
            self.senal_pausar.emit(True)
            self.labels['pausar'].setText('Reanudar')

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
        pixmap_chef = QPixmap(os.path.join('sprites', 'chef', 'meson_01.png'))
        # Override de QLabel para hacerlo drageable
        self.label_chef = DragLabel('chef', self)
        self.label_chef.setPixmap(pixmap_chef)
        self.label_chef.resize(pixmap_chef.width(), pixmap_chef.height())
        self.label_chef.setAlignment(QtCore.Qt.AlignCenter)

        label_precio_mesa = QLabel(f'{PRECIO_MESA} $')
        label_precio_mesa.setAlignment(QtCore.Qt.AlignCenter)
        pixmap_mesa = QPixmap(os.path.join('sprites', 'mapa', 'accesorios', 'silla_mesa_roja.png'))
        # Override de QLabel para hacerlo drageable
        self.label_mesa = DragLabel('mesa', self)
        self.label_mesa.setPixmap(pixmap_mesa)
        self.label_mesa.setAlignment(QtCore.Qt.AlignCenter)

        vbox = QVBoxLayout()
        vbox.addWidget(label_tienda)
        vbox.addStretch(2)
        vbox.addWidget(self.label_chef)
        vbox.addWidget(label_precio_chef)
        vbox.addStretch(2)
        vbox.addWidget(self.label_mesa)
        vbox.addWidget(label_precio_mesa)
        vbox.addStretch(2)
        self.setLayout(vbox)
        self.setEnabled(False) # comienza deshabilitada


class VentanaJuego(QWidget):

    senal_salir = pyqtSignal()
    senal_pausar = pyqtSignal(bool)
    senal_comenzar = pyqtSignal()
    senal_nuevo_juego = pyqtSignal()

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

    def activar_pre_ronda(self):
        ''' Etapa de pre-ronda '''
        self.mapa.activar_pre_ronda(True)
        self.estadisticas.activar_pre_ronda()
        self.tienda.setEnabled(True)

    def nuevo_juego(self):
        ''' Esta funcion se diferencia de comenzar en que
        (1) NO esta asociada al boton comenzar dentro del juego
        (2) SI esta encargada de la transicion entre la ventana de inicio y el
        comienzo del juego en la etapa ronda '''
        # senal que llama a la funcion nuevo_juego() en Logica
        self.setEnabled(True)
        self.senal_nuevo_juego.emit()

    def pausar(self, bool):
        ''' funcion asociada a senal en ventana de estadisticas '''
        self.mapa.pausar(bool)
        self.senal_pausar.emit(bool)

    def comenzar(self):
        ''' Esta funcion esta asociada al boton comenzar en la ventana de estadisticas
        y es llamada cuando el jugador decide comenzar luego de la pre-ronda '''
        self.tienda.setEnabled(False) # deshabilitamos la tienda
        self.mapa.activar_pre_ronda(False)
        # mandamos senal al backend para comenzar al ronda:
        self.senal_comenzar.emit()

    def salir(self):
        self.senal_salir.emit()

    # Key events no son capturados por otras ventanas hijas, por lo que
    # lo implemento en la ventana madre, y esta llama al metodo de la clase
    # miuenzo
    def keyPressEvent(self, e):
        self.mapa.keyPressEvent(e)

    def keyReleaseEvent(self, e):
        self.mapa.keyReleaseEvent(e)
