import sys

from PyQt5.QtWidgets import QLabel, QWidget, QLineEdit, \
    QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication

from parametros import ruta_logo


class VentanaInicial(QWidget):

    # Esta señal es para enviar un intento de nombre de usuario
    senal_revisar_nombre = pyqtSignal(str)

    def __init__(self, *args):
        super().__init__(*args)
        self.crear_pantalla()


    def crear_pantalla(self):
        # Aqui deben crear la pantalla.
        self.setGeometry(50, 50, 400, 500)
        self.setWindowTitle("Ventana Inicial DCCuent")

        self.labels = {}

        self.labels['logo'] = QLabel(self)
        pixeles = QPixmap(ruta_logo)
        self.labels['logo'].setPixmap(pixeles)
        self.labels['logo'].setGeometry(0, 0, 400, 400)

        self.labels['input_usuario'] = QLabel('Ingrese su nombre de usuario: ', self)
        self.input_usuario = QLineEdit('', self)

        self.labels['boton'] = QPushButton('Ingresar', self)
        self.labels['boton'].clicked.connect(self.revisar_input)

        self.hboxs = {}

        self.hboxs['input'] = QHBoxLayout()

        self.hboxs['logo'] = QHBoxLayout()
        self.hboxs['logo'].addWidget(self.labels['logo'])

        self.hboxs['input'].addStretch(1)
        self.hboxs['input'].addWidget(self.labels['input_usuario'])
        self.hboxs['input'].addStretch(1)
        self.hboxs['input'].addWidget(self.input_usuario)
        self.hboxs['input'].addStretch(1)

        self.hboxs['boton'] = QHBoxLayout()
        self.hboxs['boton'].addWidget(self.labels['boton'])


        vbox = QVBoxLayout()
        vbox.addLayout(self.hboxs['logo'])
        vbox.addStretch(1)
        vbox.addLayout(self.hboxs['input'])
        vbox.addStretch(1)
        vbox.addLayout(self.hboxs['boton'])
        vbox.addStretch(1)

        self.setLayout(vbox)

        self.show()


        # El logo, la caja de texto y el botón.
        # IMPORTANTE la caja de texto debe llamarse input_usuario
        # Si usas layout recuerda agregar los labels al layout y finalmente setear el layout

    def revisar_input(self):
        input = self.input_usuario.text()
        self.senal_revisar_nombre.emit(input)


    def recibir_revision(self, error):
        # Resetea la ventana si es que ocurre algun error,en caso contrario comienza el juego
        # IMPORTANTE la caja de text debe llamarse input_usuario
        if error:
            self.input_usuario.clear()
            self.input_usuario.setPlaceholderText("¡Inválido! Debe ser alfa-numérico.")
        else:
            usuario = self.input_usuario.text()
            self.hide()


if __name__ == "__main__":
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    a = QApplication(sys.argv)
    ventana_inicial = VentanaInicial()

    ventana_inicial.show()
    sys.exit(a.exec())
