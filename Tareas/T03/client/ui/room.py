from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from os import path

class RoomWindow(QWidget):
    nickname_signal = pyqtSignal()

    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
        self.initUI()


    def initUI(self):
        logo_label = QLabel(self)
        logo_pixmap = QPixmap(path.join('assets', 'logo.png'))
        # self.logo_label.setGeometry()
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setPixmap(logo_pixmap.scaled(
            logo_label.width(), logo_label.height()))

        connected_players_label = QLabel(
            'JUGADORES CONECTADOS', self)


        self.players_vbox = QVBoxLayout()
        self.players_labels = dict() # initialized empty

        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addWidget(logo_label)
        vbox.addStretch(2)
        vbox.addWidget(connected_players_label)
        vbox.addStretch(2)
        vbox.addLayout(self.players_vbox)


        self.setLayout(vbox)

        self.setWindowTitle('Bienvenido a DCCuatro!')
        self.setGeometry(*self.parameters['login_window_geometry'])

    def show(self, player, opponents):
        """
        overrided method to accept player and
        opponent arguments
        """
        self.players_labels['self'] = QLabel(f'{player} (YOU)', self)
        self.players_vbox.addWidget(self.players_labels['self'])

        for opponent in opponents:
            self.players_labels[opponent] = QLabel(opponent, self)
            self.players_vbox.addStretch(0.1)
            self.players_vbox.addWidget(self.players_labels[opponent])

        super().show()

    def new_player(self, name, bool):
        if bool:
            self.players_labels[name] = QLabel(name, self)
            self.players_vbox.addWidget(self.players_labels[name])
        else:
            self.players_vbox.removeWidget(self.players_labels[name])

    def room_full(self):
        """
        Method to make the mechanic of displaying 'about to start..'
        for 3 seconds when all players joined (postponed)
        """
        print('room full')
        pass
