from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QWidget, QLabel
)
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QPixmap

## ventana de inicio

class VentanaInicio(QWidget):

    senal_main_window = pyqtSignal()

    def __init__(self, ):
        super().__init__()
        self.init_gui()

    def init_gui(self):

        self.labels = {}
        pixmap_dccafe = QPixmap('sprites/otros/logo_blanco.png')
        self.labels['dccafe_icon'] = QLabel(self)
        self.labels['dccafe_icon'].setGeometry(0, 0, 400, 200)
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
        self.setGeometry(300, 300, 600, 800)
        self.setStyleSheet(
            'background-color: grey'
        )
        self.show()

    def resumir_juego(self):
        print('resumir')

    def empezar_nuevo_juego(self):
        print('nuevo')

if __name__ == '__main__':
    import sys
    app = QApplication([])
    window = VentanaInicio()
    sys.exit(app.exec_())
