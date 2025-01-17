from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from os import path
import sys, json

sys.path.append('..')
from client.utils import json_hook

class LoginWindow(QWidget):

    with open('parameters.json', 'r') as file:
        parameters = json.loads(file.read(), object_hook=json_hook)


    username_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        logo_label = QLabel(self)
        logo_pixmap = QPixmap(path.join('ui', 'assets', 'logo.png'))
        logo_label.setAlignment(Qt.AlignCenter)
        logo_label.setPixmap(logo_pixmap.scaled(
            self.width()/2, self.height()/2))


        hbox = QHBoxLayout()
        self.dialog_box = QLineEdit(self)
        self.dialog_box.setPlaceholderText('INGRESA TU NOMBRE')
        hbox.addStretch(0.1)
        hbox.addWidget(self.dialog_box)

        self.join_button = QPushButton('JOIN', self)
        self.join_button.setStyleSheet(
            'background-color: grey; border-radius: 2px; width: 50px;'
            +'height: 20px;')
        self.join_button.clicked.connect(self.join)

        hbox.addWidget(self.join_button)
        hbox.addStretch(0.1)

        vbox = QVBoxLayout()
        vbox.addStretch(2)
        vbox.addWidget(logo_label)
        vbox.addStretch(2)
        vbox.addLayout(hbox)
        vbox.addStretch(2)

        self.setLayout(vbox)
        self.setStyleSheet('background-color: black;')
        self.setWindowTitle('Bienvenido a DCCuatro!')
        self.setGeometry(*self.parameters['login_window_geometry'])

    def close(self, *args, **kwargs):
        """
        overrided method to accept extra arguments fromb backend signal
        associated also with room.show() (ignore them)
        """
        super().close()

    def join(self):
        """
        Called when user clicks on join button and sends signal
        to backend which sends the username to server to be validated
        """
        username = self.dialog_box.text()
        self.username_signal.emit(username)

    def invalid_username(self, cause):
        self.dialog_box.setText('')
        self.dialog_box.setPlaceholderText(cause)
