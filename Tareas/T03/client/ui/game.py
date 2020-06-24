from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from os import path

class GameWindow(QWidget):

    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
        self.initUI()

    def initUI(self):
        pass
