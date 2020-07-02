from PyQt5.QtWidgets import QDialog, QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

class ColorDialog(QDialog):

    color_signal = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setModal(True)

        text_1 = QLabel('HAZ JUGADO UN CAMBIO DE COLOR', self)
        text_2 = QLabel('SELECCIONA UN COLOR PARA SEGUIR JUGANDO', self)

        red_button = QPushButton('ROJO', self)
        red_button.setStyleSheet('background-color: red;')
        send_red = lambda: self.send_color('rojo')
        red_button.clicked.connect(send_red)

        green_button = QPushButton('VERDE', self)
        green_button.setStyleSheet('background-color: green;')
        send_green = lambda: self.send_color('verde')
        green_button.clicked.connect(send_green)

        yellow_button = QPushButton('AMARILLO', self)
        yellow_button.setStyleSheet('background-color: yellow;')
        send_yellow = lambda: self.send_color('amarillo')
        yellow_button.clicked.connect(send_yellow)

        blue_button = QPushButton('AZUL', self)
        blue_button.setStyleSheet('background-color: blue;')
        send_blue = lambda: self.send_color('azul')
        blue_button.clicked.connect(send_blue)

        box_1 = QHBoxLayout()
        box_2= QHBoxLayout()

        box_1.addWidget(red_button)
        box_1.addWidget(green_button)

        box_2.addWidget(yellow_button)
        box_2.addWidget(blue_button)

        vbox = QVBoxLayout()
        vbox.addWidget(text_1)
        vbox.addWidget(text_2)
        vbox.addStretch(1)
        vbox.addLayout(box_1)
        vbox.addLayout(box_2)

        self.setLayout(vbox)
        self.setStyleSheet('background-color: black;')
        self.show()

    def send_color(self, color):
        self.color_signal.emit(color)
        self.close()

class EndGameDialog(QDialog):

    back_to_login_signal = pyqtSignal()

    def __init__(self, parent, winner):
        super().__init__(parent)
        self.initUI(winner)

    def initUI(self, winner):

        self.setModal(True)

        text_1 = QLabel('EL JUEGO HA ACABADO', self)
        text_2 = QLabel(f'GANADOR: {winner.upper()}', self)

        restart_button = QPushButton('VOLVER A LA SALA DE INICIO', self)
        restart_button.clicked.connect(self.back_to_login_signal.emit)
        restart_button.clicked.connect(self.close)
        restart_button.setStyleSheet('background-color: grey;')

        vbox = QVBoxLayout()
        vbox.addWidget(text_1)
        vbox.addWidget(text_2)
        vbox.addStretch(1)
        vbox.addWidget(restart_button)

        self.setLayout(vbox)
        self.setStyleSheet('background-color: black;')
        self.show()
