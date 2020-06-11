import pickle


# ETAPA DE CARGA #
class EquipoDocencia:
    def __init__(self):
        self.ayudantes_normales = []
        self.ayudante_jefe = None

    # Aquí se filtra la lista del objeto al deserializarlo
    def __setstate__(self, estado):
        self.ayudantes_normales = []
        self.ayudante_jefe = None
        for ayudante in estado['ayudantes_normales']:
            if ayudante.cargo == 'Jefe':
                self.ayudante_jefe = ayudante
            else:
                self.ayudantes_normales.append(ayudante)

# Aquí se carga la instancia de EquipoDocencia
def cargar_instancia(ruta):
    # Completar
    with open(ruta, 'rb') as file:
        equipo_docencia = pickle.load(file)
    return equipo_docencia

# ETAPA DE GUARDADO #
class Ayudante:
    def __init__(self, cargo, usuario_github, pokemon_favorito, pizza_favorita):
        self.cargo = cargo
        self.usuario_github = usuario_github
        self.pokemon_favorito = pokemon_favorito
        self.pizza_favorita = pizza_favorita

    def __repr__(self):
        mensaje = f"¡Hola! soy {self.usuario_github} y tengo el cargo de {self.cargo}"
        return mensaje


class AyudanteJefe(Ayudante):
    def __init__(self, cargo, usuario_github, pokemon_favorito, pizza_favorita, trabajo_restante, experto, carrera):
        super().__init__(cargo, usuario_github, pokemon_favorito, pizza_favorita)
        self.trabajo_restante = trabajo_restante
        self.experto = experto
        self.carrera = carrera

    # Aquí se definen cambios que sólo se afectan a AyudanteJefe
    def __getstate__(self):
        # Completar

        pass

# Aquí se guarda instancia de EquipoDocencia
def guardar_instancia(ruta, instancia_equipo_docencia):
    # Completar
    with open(ruta, 'wb') as file:
        serializado = pickle.dumps(instancia_equipo_docencia)
        file.write(bytes(serializado))
    return True
