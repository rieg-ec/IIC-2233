from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from parametros import RAPIDEZ_RELOJ


class Reloj(QObject):

    actualizar_hora_signal = pyqtSignal(int)
    actualizar_cronometro_signal = pyqtSignal(int, int, int, int)

    def __init__(self):
        super().__init__()
        self.tiempo_actual = 0
        self.tiempo_cronometro = 0
        self.reloj = QTimer()
        self.rapidez_reloj = RAPIDEZ_RELOJ
        self.reloj.setInterval(500)
        self.reloj.timeout.connect(self.paso_del_tiempo)
        self.cronometro = QTimer()
        self.cronometro.setInterval(500)
        self.cronometro.timeout.connect(self.tiempo_cronometro)

    def paso_del_tiempo(self):
        self.tiempo_actual += self.rapidez_reloj
        self.actualizar_hora_signal.emit(self.hora_actual)

    def comenzar_reloj(self):
        self.reloj.start()

    def tiempo_cronometro(self):
        self.tiempo_cronometro += self.rapidez_reloj
        self.actualizar_cronometro_signal.emit(self.tiempo_cronometro)

    def comenzar_cronometro(self):
        self.cronometro.start()

    def pausar_cronometro(self):
        self.cronometro.stop()

    def reiniciar_cronometro(self):
        self.tiempo_cronometro = 0
