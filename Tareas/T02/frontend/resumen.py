from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QLabel, QProgressBar, QLCDNumber
)
from PyQt5.QtCore import pyqtSignal, QEvent
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QLabel, QProgressBar, QLCDNumber
)
from PyQt5.QtCore import pyqtSignal, QEvent
from PyQt5 import QtCore
from PyQt5.QtWidgets import (QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QPixmap
from PARAMETROS import GM_VENTANA_RESUMEN



class VentanaResumen(QWidget):
    def __init__(self, ronda, clientes_perdidos, clientes_atendidos,
                    dinero, reputacion, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ronda = ronda
        self.clientes_perdidos = clientes_perdidos
        self.clientes_atendidos = clientes_atendidos
        self.dinero = dinero
        self.reputacion = reputacion
        self.initUI()


    def initUI(self):
        self.setGeometry(*GM_VENTANA_RESUMEN)

        hboxs = {}

        label_resumen_ronda = QLabel(f'RESUMEN RONDA {self.ronda}')
        label_resumen_ronda.setAlignment(QtCore.Qt.AlignCenter)

        hboxs['clientes-perdidos'] = QHBoxLayout()
        hboxs['clientes-perdidos'].addStretch(2)
        label_clientes_perdidos = QLabel('CLIENTES PERDIDOS')
        label_nro_clientes_perdidos = QLCDNumber(self)
        hboxs['clientes-perdidos'].addWidget(label_clientes_perdidos, 2)
        hboxs['clientes-perdidos'].addStretch(0.1)
        hboxs['clientes-perdidos'].addWidget(label_nro_clientes_perdidos, 1)
        hboxs['clientes-perdidos'].addStretch(2)

        hboxs['clientes-atendidos'] = QHBoxLayout()
        hboxs['clientes-atendidos'].addStretch(2)
        label_clientes_atendidos = QLabel('CLIENTES ATENDIDOS')
        label_nro_clientes_atendidos = QLCDNumber(self)
        hboxs['clientes-atendidos'].addWidget(label_clientes_atendidos, 2)
        hboxs['clientes-atendidos'].addStretch(0.1)
        hboxs['clientes-atendidos'].addWidget(label_nro_clientes_atendidos, 1)
        hboxs['clientes-atendidos'].addStretch(2)

        hboxs['dinero-acumulado'] = QHBoxLayout()
        hboxs['dinero-acumulado'].addStretch(2)
        label_dinero_acumulado = QLabel('DINERO ACUMULADO')
        label_nro_dinero_acumulado = QLCDNumber(self)
        hboxs['dinero-acumulado'].addWidget(label_dinero_acumulado, 2)
        hboxs['dinero-acumulado'].addStretch(0.1)
        hboxs['dinero-acumulado'].addWidget(label_nro_dinero_acumulado, 1)
        hboxs['dinero-acumulado'].addStretch(2)

        hboxs['reputacion'] = QHBoxLayout()
        hboxs['reputacion'].addStretch(2)
        label_reputacion = QLabel('REPUTACION')
        label_nro_reputacion = QLCDNumber(self)
        hboxs['reputacion'].addWidget(label_reputacion, 2)
        hboxs['reputacion'].addStretch(0.1)
        hboxs['reputacion'].addWidget(label_nro_reputacion, 1)
        hboxs['reputacion'].addStretch(2)

        hbox_botones = QHBoxLayout()
        hbox_botones.addStretch(2)
        botones = {
            'salir': QPushButton('Salir', self),
            'guardar': QPushButton('Guardar', self),
            'continuar': QPushButton('Continuar', self)
        }
        hbox_botones.addStretch(0.5)
        for boton in botones:
            hbox_botones.addWidget(botones[boton])
            hbox_botones.addStretch(0.5)
        hbox_botones.addStretch(2)

        vbox = QVBoxLayout()
        vbox.addWidget(label_resumen_ronda)
        vbox.addStretch(1)

        for hbox in hboxs:
            vbox.addLayout(hboxs[hbox])
            vbox.addStretch(0.2)

        vbox.addStretch(2)
        vbox.addLayout(hbox_botones)

        self.setLayout(vbox)
