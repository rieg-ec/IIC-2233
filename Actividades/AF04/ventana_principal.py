import os
import sys
from random import choice
from logica import Logica
from ventana_final import VentanaFinal

from PyQt5.QtWidgets import QLabel, QWidget, QLineEdit, \
    QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication


class VentanaPrincipal(QWidget):

    # Aquí debes crear una señal que usaras para enviar la jugada al back-end
    senal_enviar_jugada = pyqtSignal(dict)

    def __init__(self, *args):
        super().__init__(*args)
        self.crear_pantalla()

    def crear_pantalla(self):
        # Aquí deben crear la ventana vacia.
        self.setWindowTitle("DCCuent")
        self.setGeometry(100, 100, 600, 600)
        # Es decir, agregar y crear labels respectivos a datos del juego, pero sin contenido
        # Si usas layout recuerda agregar los labels al layout y finalmente setear el layout
        self.labels = {}

        self.labels['nombre_usuario'] = QLabel(self)
        self.labels['victorias'] = QLabel(self)
        self.labels['derrotas'] = QLabel(self)

        for tecla in ['Q', 'W', 'E']:
            self.labels[tecla] = QLabel(self)

        for carta in ['infanteria', 'rango', 'artilleria']:
            self.labels[carta] = QLabel(self)
            self.labels[carta].resize(238, 452)
            self.labels[carta].setScaledContents(True)

        self.hboxs = {}

        self.hboxs['info'] = QHBoxLayout()
        for label in ['nombre_usuario', 'victorias', 'derrotas']:
            self.hboxs['info'].addStretch(1)
            self.hboxs['info'].addWidget(self.labels[label])
            self.hboxs['info'].addStretch(1)


        self.hboxs['teclas'] = QHBoxLayout()
        for tecla in ['Q', 'W', 'E']:
            self.hboxs['teclas'].addStretch(1)
            self.hboxs['teclas'].addWidget(self.labels[tecla])
            self.hboxs['teclas'].addStretch(1)


        self.hboxs['cartas'] = QHBoxLayout()
        for carta in ['infanteria', 'rango', 'artilleria']:
            self.hboxs['cartas'].addStretch(1)
            self.hboxs['cartas'].addWidget(self.labels[carta])
            self.hboxs['cartas'].addStretch(1)

        self.vbox = QVBoxLayout()
        for hbox in ['info', 'teclas', 'cartas']:
            self.vbox.addStretch(1)
            self.vbox.addLayout(self.hboxs[hbox])
            self.vbox.addStretch(1)

        self.setLayout(self.vbox)

    def actualizar(self, datos):
        # Esta es la funcion que se encarga de actualizar el contenido de la ventana y abrirla
        # Recibe las nuevas cartas y la puntuación actual en un diccionario

        # Al final, se muestra la ventana.
        cartas = ['infanteria', 'artilleria', 'rango']
        teclas = ['Q', 'W', 'E']


        for carta in cartas:
            pixmap = QPixmap(datos[carta]['ruta'])
            self.labels[carta].setPixmap(pixmap)

        self.labels['nombre_usuario'].setText(f'nombre de usuario: {datos["usuario"]}')
        self.labels['victorias'].setText(f'victorias: {datos["victorias"]}')
        self.labels['derrotas'].setText(f'derrotas: {datos["derrotas"]}')


        for tecla in teclas:
            self.labels[tecla].setText(tecla)

        self.show()

    def keyPressEvent(self, evento):
        cartas = {
            'Q': 'infanteria',
            'W': 'rango',
            'E': 'artilleria'
        }
        if evento.text() in ['q', 'w', 'e']:
            print('si')
            carta_usuario = {
                'tipo': cartas[evento.text().capitalize()],
                'valor': None
            }
            self.senal_enviar_jugada.emit(carta_usuario)
            self.hide()


class VentanaCombate(QWidget):

    # Esta señal es para volver a la VentanaPrincipal con los datos actualizados
    senal_regresar = pyqtSignal(dict)
    # Esta señal envia a la ventana final con el resultado del juego
    senal_abrir_ventana_final = pyqtSignal(str)

    def __init__(self, *args):
        super().__init__(*args)
        self.crear_pantalla()

    def crear_pantalla(self):
        self.setWindowTitle("DCCuent")
        self.vbox = QVBoxLayout()
        self.layout_principal = QHBoxLayout()
        self.label_carta_usuario = QLabel()
        self.label_victoria = QLabel()
        self.label_carta_enemiga = QLabel()
        self.boton_regresar = QPushButton("Regresar")

        self.layout_principal.addWidget(self.label_carta_usuario)
        self.layout_principal.addWidget(self.label_victoria)
        self.layout_principal.addWidget(self.label_carta_enemiga)

        self.boton_regresar.clicked.connect(self.regresar)
        self.vbox.addLayout(self.layout_principal)
        self.vbox.addWidget(self.boton_regresar)

        self.setLayout(self.vbox)

    def mostrar_resultado_ronda(self, datos):
        self.datos = datos
        mensaje = datos["mensaje"]
        carta_enemiga = datos["enemigo"]
        carta_jugador = datos["jugador"]
        self.label_carta_usuario.setPixmap(QPixmap(carta_jugador["ruta"]).scaled(238,452))
        self.label_carta_enemiga.setPixmap(QPixmap(carta_enemiga["ruta"]).scaled(238,452))
        self.label_victoria.setText(mensaje)
        self.show()

    def regresar(self):
        resultado = self.datos["resultado"]
        if resultado == "victoria" or resultado == "derrota":
            self.senal_abrir_ventana_final.emit(resultado)
        else:
            self.senal_regresar.emit(self.datos)
        self.hide()


if __name__ == "__main__":
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    a = QApplication(sys.argv)
    ventana_principal = VentanaPrincipal()

    ventana_principal.show()
    sys.exit(a.exec())
