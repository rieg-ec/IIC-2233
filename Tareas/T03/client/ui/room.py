from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap

from os import path
import sys, json

sys.path.append('..')
from client.utils import json_hook


class RoomWindow(QWidget):

    with open('parameters.json', 'r') as file:
        parameters = json.loads(file.read(), object_hook=json_hook)


    nickname_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.widgets = []
        self.initUI()


    def initUI(self):
        logo_label = QLabel(self)
        logo_pixmap = QPixmap(path.join('ui', 'assets', 'logo.png'))
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setPixmap(logo_pixmap.scaled(
            self.width() / 2, self.height() / 2))

        connected_players_label = QLabel(
            'JUGADORES CONECTADOS', self)
        connected_players_label.setAlignment(Qt.AlignCenter)


        self.players_vbox = QVBoxLayout()
        self.players_labels = dict() # initialized empty


        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(logo_label, 5)
        vbox.addWidget(connected_players_label, 1)
        vbox.addStretch(1)
        vbox.addLayout(self.players_vbox, 5)
        vbox.addStretch(1)
        vbox.setAlignment(Qt.AlignCenter)

        self.setLayout(vbox)


        self.setStyleSheet('background-color: black;')
        self.setWindowTitle('Bienvenido a DCCuatro!')
        self.setGeometry(*self.parameters['login_window_geometry'])

    def show(self, player, opponents):
        """
        overrided method to accept player and
        opponent arguments
        """

        for widget in self.widgets.copy():
            self.widgets.remove(widget)
            widget.deleteLater()

        self.players_labels['self'] = QLabel(f'{player} (YOU)', self)
        self.players_vbox.addWidget(self.players_labels['self'])
        self.players_vbox.setAlignment(
            Qt.AlignCenter | Qt.AlignTop)
        self.widgets.append(self.players_labels['self'])

        for opponent in opponents:
            self.players_labels[opponent] = QLabel(opponent, self)
            self.widgets.append(self.players_labels[opponent])
            self.players_vbox.addStretch(0.1)
            self.players_vbox.addWidget(self.players_labels[opponent])

        super().show()

    def new_player(self, name, bool):
        if bool:
            self.players_labels[name] = QLabel(name, self)
            self.players_vbox.addWidget(self.players_labels[name])
            self.players_labels[name].setAlignment(
                Qt.AlignCenter | Qt.AlignTop)
        else:
            self.players_labels[name].deleteLater()
