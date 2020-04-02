from abc import ABC, abstractmethod
import random


class Jugador(ABC):

    def __init__(self, nombre, equipo, especialidad, energia):
        self.nombre = nombre
        self.equipo = equipo
        self.especialidad = especialidad
        self.energia = int(energia)
        self.inteligencia = 0
        self.audacia = 0
        self.trampa = 0
        self.nerviosismo = 0

    def __str__(self):
        if self.equipo == 'ayudante':
            return f'Ayudante {self.nombre} ({self.especialidad})'
        return f'Alumno(a) {self.nombre} ({self.especialidad})'

    def __repr__(self):
        return (f'({type(self).__name__}) {self.nombre}: '
                f'equipo={self.equipo}|'
                f'energia={self.energia}|'
                f'inteligencia={self.inteligencia}|'
                f'audacia={self.audacia}|'
                f'trampa={self.trampa}|'
                f'nerviosismo={self.nerviosismo}')

    @abstractmethod
    def enfrentar(self, tipo_de_juego, enemigo):
        return 0


class JugadorMesa(Jugador):

    def __init__(self, nombre, equipo, especialidad, energia):
        super().__init__(nombre, equipo, especialidad, energia)
        self.nerviosismo = min(self.energia, random.randint(0, 3))

    def jugar_mesa(self, enemigo):
        return enemigo.nerviosismo > self.nerviosismo

    def enfrentar(self, tipo_de_juego, enemigo):
        print(f"{self.equipo} {self.nombre} ({self.especialidad}): ¡Desafio a {enemigo.equipo}(a) "
             +f"{enemigo.nombre} ({enemigo.especialidad}) a un juego de {tipo_de_juego}!")
        self.jugar_mesa(enemigo)


class JugadorCartas(Jugador):

    def __init__(self, nombre, equipo, especialidad, energia):
        super().__init__(nombre, equipo, especialidad, energia)
        self.inteligencia = self.energia * 2.5

    def jugar_cartas(self, enemigo):
        return enemigo.inteligencia < self.inteligencia

    def enfrentar(self, tipo_de_juego, enemigo):
        print(f"{self.equipo} {self.nombre} ({self.especialidad}): ¡Desafio a {enemigo.equipo}(a) "
             +f"{enemigo.nombre} ({enemigo.especialidad}) a un {tipo_de_juego}")
        return self.jugar_cartas(enemigo)


class JugadorCombate(Jugador):

    def __init__(self, nombre, equipo, especialidad, energia):
        super().__init__(nombre, equipo, especialidad, energia)
        self.audacia = max(self.energia, random.randint(3, 5))

    def jugar_combate(self, enemigo):
        return enemigo.audacia < self.audacia

    def enfrentar(self, tipo_de_juego, enemigo):
        print(f"{self.equipo} {self.nombre} ({self.especialidad}): ¡Desafio a {enemigo.equipo}(a) "
             +f"{enemigo.nombre} ({enemigo.especialidad}) a un {tipo_de_juego}")
        return self.jugar_combate(enemigo)

class JugadorCarreras(Jugador):

    def __init__(self, nombre, equipo, especialidad, energia):
        super().__init__(nombre, equipo, especialidad, energia)
        self.trampa = self.energia * 3

    def jugar_carrera(self, enemigo):
        return enemigo.trampa < self.trampa

    def enfrentar(self, tipo_de_juego, enemigo):
        print(f"{self.equipo} {self.nombre} ({self.especialidad}): ¡Desafio a {enemigo.equipo}(a) "
             +f"{enemigo.nombre} ({enemigo.especialidad}) a un {tipo_de_juego}")
        return self.jugar_carrera(enemigo)


class JugadorInteligente(JugadorMesa, JugadorCartas):

    def __init__(self, nombre, equipo, especialidad, energia):
        super().__init__(nombre, equipo, especialidad, energia)
        self.audacia = 3
        self.trampa = 3


class JugadorIntrepido(JugadorCarreras, JugadorCombate):
    def __init__(self, nombre, equipo, especialidad, energia):
        super().__init__(nombre, equipo, especialidad, energia)
        self.nerviosismo = 3
        self.inteligenca = 3
