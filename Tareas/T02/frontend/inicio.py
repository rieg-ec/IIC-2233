from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QLabel, QMainWindow, QProgressBar, QLCDNumber
)
from PyQt5.QtCore import pyqtSignal, QEvent
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QPixmap, QPaintEvent

from PARAMETROS import (
    GM_VENTANA_INICIO, GM_VENTANA_JUEGO, GM_LOGO_DCCAFE_INICIO
)

## ventana de inicio

class VentanaInicio(QWidget):

    senal_nuevo_juego = pyqtSignal()
    senal_resumir_juego = pyqtSignal()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):

        self.labels = {}
        pixmap_dccafe = QPixmap('sprites/otros/logo_blanco.png')
        self.labels['dccafe_icon'] = QLabel(self)
        self.labels['dccafe_icon'].setGeometry(*GM_LOGO_DCCAFE_INICIO)
        self.labels['dccafe_icon'].setAlignment(QtCore.Qt.AlignCenter)
        self.labels['dccafe_icon'].setPixmap(pixmap_dccafe.scaled(
                                            self.labels['dccafe_icon'].width(),
                                            self.labels['dccafe_icon'].height(),
                                            ))

        self.labels['subtitulo'] = QLabel(self)
        self.labels['subtitulo'].setText('Bienvenido al mejor cafe virtual del DCC!')
        self.labels['subtitulo'].setAlignment(QtCore.Qt.AlignCenter)
        self.labels['subtitulo'].setStyleSheet(
            'color: green; font-size: 30px;')

        opciones = QHBoxLayout()
        self.botones = {}
        self.botones['resumir'] = QPushButton('Seguir jugando', self)
        self.botones['resumir'].setStyleSheet(
                    'background-color: blue; color: black')
        self.botones['resumir'].clicked.connect(self.resumir_juego)

        self.botones['nuevo'] = QPushButton('Comenzar de nuevo', self)
        self.botones['nuevo'].setStyleSheet(
                    'background-color: red; color: black')
        self.botones['nuevo'].clicked.connect(self.empezar_nuevo_juego)

        for boton in self.botones:
            opciones.addStretch(2)
            opciones.addWidget(self.botones[boton])
            opciones.addStretch(2)


        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addWidget(self.labels['dccafe_icon'])
        vbox.addStretch(2)
        vbox.addWidget(self.labels['subtitulo'])
        vbox.addStretch(2)
        vbox.addLayout(opciones)
        vbox.addStretch(2)

        self.setLayout(vbox)

        self.setWindowTitle('Bienvenido a DCCafe!')
        self.setGeometry(*GM_VENTANA_INICIO)
        self.show()

    def resumir_juego(self):
        self.senal_resumir_juego.emit()

    def empezar_nuevo_juego(self):
        self.senal_nuevo_juego.emit()
