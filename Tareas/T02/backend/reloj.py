from PyQt5.QtCore import QObject, pyqtSignal, QTimer
from PARAMETROS import RAPIDEZ_RELOJ, LLEGADA_CLIENTES


class Reloj(QObject):
    ''' clase ocupada para manejar los temporizadores '''

    def __init__(self):
        super().__init__()
        self.rapidez_reloj = RAPIDEZ_RELOJ # ponderador
        self.temporizadores = []
        self.intervalo_clientes = LLEGADA_CLIENTES # no cambia durante el juego

    def reanudar_reloj(self):
        for temporizador in self.temporizadores:
            temporizador.start()

    def pausar_reloj(self):
        for temporizador in self.temporizadores:
            temporizador.stop()


    def temporizador_chef(self, tiempo, senal, chef):
        tmp_chef = ChefTimer(tiempo * self.rapidez_reloj, senal, chef)
        tmp_chef.start()
        self.temporizadores.append(tmp_chef)

    def temporizador_cliente(self):
        ''' temporizador asociado a un cliente en especifico '''
        tmp_enojarse = QTimer()
        tmp_enojarse.setSingleShot(True)
        tmp_irse = QTimer()
        tmp_irse.setSingleShot(True)
        self.temporizadores.extend([tmp_enojarse, tmp_irse])
        # guardamos el temporizador del ultimo cliente para saber cuando cerrar
        # el DCC:
        self.ultimo_cliente_timer = tmp_irse
        return tmp_enojarse, tmp_irse

    def temporizador_clientes(self, func):
        ''' temporizador asociado a la llegada periodica de clientes '''
        self.tmp_clientes = QTimer()
        self.tmp_clientes.setInterval(self.rapidez_reloj *
                                            self.intervalo_clientes)
        self.tmp_clientes.timeout.connect(func)
        self.tmp_clientes.start()
        self.temporizadores.append(self.tmp_clientes)

    def temporizador_acabar_ronda(self, func):
        self.temporizadores.remove(self.tmp_clientes)
        self.tmp_clientes.deleteLater() # nos aseguramos
        # que en caso de pausar y reanudar la ronda, no se vuelva a activar
        self.tmp_acabar_ronda = QTimer()
        self.tmp_acabar_ronda.setInterval(self.rapidez_reloj *
                                                self.intervalo_clientes)
        self.tmp_acabar_ronda.setSingleShot(True)
        self.tmp_acabar_ronda.timeout.connect(func)
        self.tmp_acabar_ronda.start()
        self.temporizadores.append(self.tmp_acabar_ronda)

class ChefTimer(QObject):
    ''' clase que simula un temporizador que al terminar activa una senal '''
    def __init__(self, tiempo, senal, chef):
        super().__init__()
        self.tiempo = tiempo
        self.senal = senal
        self.chef = chef
        self.elapsado = 0
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(self.tiempo)
        self.timer.timeout.connect(self.mandar_senal)

    def start(self):
        self.timer.start()

    def stop(self):
        self.timer.stop()

    def mandar_senal(self):
        self.senal.emit(self.chef)
        self.deleteLater()
