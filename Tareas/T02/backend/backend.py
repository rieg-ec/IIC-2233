from PyQt5.QtCore import pyqtSignal, QObject, QRect, QTimer
from PyQt5.QtWidgets import QLabel
from PARAMETROS import VEL_MOVIMIENTO, PRECIO_CHEF, PRECIO_MESA
from backend.reloj import Reloj
from backend.utils_backend import DCCafe


class Logica(QObject):
    # miuenzo, mesas, chefs
    senal_crear_objetos = pyqtSignal(list, list, dict)

    senal_compra_verificada = pyqtSignal(dict)
    senal_mover_miuenzo = pyqtSignal(int, int, int)

    senal_colision_chef = pyqtSignal(QLabel, int)
    senal_colision_mesa = pyqtSignal(QLabel)

    senal_terminar_bocadillo = pyqtSignal(QLabel)

    senal_acabar_ronda = pyqtSignal(int, int, int, int, int)
    senal_llegada_cliente = pyqtSignal(QTimer, QTimer)

    # senal para actualizar el dinero y reputacion al ocurrir eventos
    senal_dinero = pyqtSignal(int)
    senal_reputacion = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.tiempo_actual = 0
        self.dccafe = DCCafe()
        self.dccafe.cargar_datos()

    def empezar_ronda(self):
        self.dccafe.empezar_ronda()
        self.senal_dinero.emit(self.dccafe.dinero)
        self.senal_reputacion.emit(self.dccafe.reputacion)
        self.clientes_totales = self.dccafe.clientes_ronda()
        self.clientes_actuales = 0
        self.reloj.temporizador_clientes(self.llegada_clientes)

    def timer_chef(self, chef):
        # creamos un QTimer singleShot para mandar senal al terminar de hacer
        # el bocadillo, desde el front end mandaremos una senal al terminar
        self.reloj.temporizador_chef(chef.tiempo_cocina,
                    self.senal_terminar_bocadillo, chef)

    def verificar_compra(self, e, labels, miuenzo, dimensiones_mapa):
        ''' to-do: verificar compra en backend '''
        tipo, width, height = e.mimeData().text().split(',')
        qrect_drop = QRect(e.pos().x(), e.pos().y(), int(width), int(height))
        valido = True

        if (tipo == 'chef' and self.dccafe.dinero < PRECIO_CHEF) or (tipo == 'mesa'
            and self.dccafe.dinero < PRECIO_MESA):
            valido = False

        if not dimensiones_mapa.contains(qrect_drop):
            valido = False

        elif qrect_drop.intersects(miuenzo.geometry()):
            valido = False

        else:
            for label in labels:
                if label.geometry().intersects(qrect_drop):
                    valido = False

        if valido:
            data = {'tipo': tipo,
                    'pos': e.pos()}
            if tipo == 'chef':
                self.dccafe.dinero -= PRECIO_CHEF
            else:
                self.dccafe.dinero -= PRECIO_MESA
            self.senal_compra_verificada.emit(data)
            self.senal_dinero.emit(self.dccafe.dinero)


    def movimiento_miuenzo(self, teclas, labels,
                            miuenzo, dimensiones_mapa):
        ''' En caso de que el movimiento de miuenzo sea valido, mandamos senal
        a VentanaMapa'''
        # guardamos la posicion de miuenzo antes del movimiento
        # tecla W:
        if teclas[87]:
            dx = 0
            dy = - VEL_MOVIMIENTO
            tecla = 87
        # tecka A:
        elif teclas[65]:
            dx = - VEL_MOVIMIENTO
            dy = 0
            tecla = 65
        # tecla D:
        elif teclas[68]:
            dx = VEL_MOVIMIENTO
            dy = 0
            tecla = 68
        # tecla S:
        elif teclas[83]:
            dx = 0
            dy = VEL_MOVIMIENTO
            tecla = 83

        nueva_posicion = QRect(miuenzo.pos().x() + dx, miuenzo.pos().y() + dy,
                                miuenzo.width(), miuenzo.height())
        interseccion = False
        for label in labels:
            if nueva_posicion.intersects(label.geometry()):
                interseccion = True
                if label.__class__.__name__ == 'Chef':
                    if not label.cocinando and not miuenzo.ocupado: # esperando
                        self.senal_colision_chef.emit(label, 1) # empezar a cocinar
                        self.timer_chef(label) # empezamos un timer
                    elif label.cocinando == 2 and not miuenzo.ocupado:
                        # el 2 significa que el chef termino el bocadillo
                        self.senal_colision_chef.emit(label, 0) # agarrar el bocadillo

                elif label.__class__.__name__ == 'Mesa':
                    if miuenzo.ocupado and label.ocupado:
                        # mesa con cliente y miuenzo con el bocadillo
                        self.senal_colision_mesa.emit(label)

        if not dimensiones_mapa.contains(nueva_posicion):
            interseccion = True

        if interseccion:
            dx = dy = 0 # su desplazamiento sera 0
        # siempre mandamos la senal, pues la animacion es independiente de
        # si se desplaza o no
        self.senal_mover_miuenzo.emit(dx, dy, tecla)

    def comenzar_juego(self):
        ''' Funcion asociada a empezar un juego luego de hacer los cambios
        en la pre-ronda, llamada al presionar el boton comenzar o al iniciar un juego
        desde la ronda 0 '''
        self.reloj = Reloj() # 2000 = intervalo con el que llegan los clientes
        self.empezar_ronda()



    def nuevo_juego(self):
        ''' Funcion llamada desde senal_nuevo_juego al empezar un juego nuevo '''
        # senal que llama a la funcion comenzar en ventana_mapa
        self.senal_crear_objetos.emit(self.dccafe.mesero, self.dccafe.mesas,
                                    self.dccafe.chefs)
        # actualizamos la informacion en ventana estadisticas:
        self.senal_dinero.emit(self.dccafe.dinero)
        self.senal_reputacion.emit(self.dccafe.dinero)
        self.comenzar_juego()

    def llegada_clientes(self):
        ''' sacar hard code'''
        if self.dccafe.abierto:
            if self.dccafe.mesas_ocupadas < len(self.dccafe.mesas) and\
                self.clientes_actuales <= self.clientes_totales:

                tmp_enojarse, tmp_irse = self.reloj.temporizador_cliente()
                # temporizadores que pertenecen a la instancia de reloj
                print('cliente llegando: ', self.dccafe.mesas_ocupadas, self.dccafe.mesas)
                self.senal_llegada_cliente.emit(tmp_enojarse, tmp_irse)
                self.dccafe.mesas_ocupadas += 1
            # actualizamos clientes que han llegado en esta ronda:
            self.clientes_actuales += 1
            # actualizamos clientes totales que han llegado:
            self.dccafe.pedidos_totales += 1
            if not self.clientes_actuales < self.clientes_totales:
                self.dccafe.abierto = False
                # creamos un nuevo timer con un poco de margen para que el cliente
                # alcanze a irse y ocurran todos los procesos necesarios:
                tiempo_ultimo_cliente = self.reloj.ultimo_cliente_timer.interval()
                self.timer_acabar_ronda = QTimer()
                self.timer_acabar_ronda.setSingleShot(True)
                self.timer_acabar_ronda.setInterval(tiempo_ultimo_cliente + 1000)
                self.timer_acabar_ronda.timeout.connect(self.acabar_ronda)
                self.timer_acabar_ronda.start()

    def salida_cliente(self, cliente):
        if cliente.estado != 1:
            self.dccafe.pedidos_exitosos += 1
        self.dccafe.mesas_ocupadas -= 1
        if cliente.estado == 1:
            print('cliente se fue enojado')
        else:
            print('cliente se fue contento')

    def acabar_ronda(self):
        ronda = self.dccafe.ronda
        c_perdidos = self.dccafe.pedidos_totales - self.dccafe.pedidos_exitosos
        c_atendidos = self.dccafe.pedidos_exitosos
        dinero = self.dccafe.dinero
        rep = self.dccafe.calcular_reputacion()
        self.dccafe.abierto = False
        self.senal_acabar_ronda.emit(ronda, c_perdidos, c_atendidos, dinero, rep)

    def pausar_juego(self, bool):
        print('pausar_juego')
        if not bool:
            # reanudamos el juego
            self.reloj.reanudar_reloj()
        else:
            # pausamos el juego
            self.reloj.pausar_reloj()
