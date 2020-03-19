from collections import namedtuple, deque


def cargar_animes(path):

    anime_datos = {}
    Animes = namedtuple("Animes", ["nombre", "rating", "estudio", "generos"])
    # Abrimos el archivo de animes
    with open(path, 'r') as file:
        # Leemos las lineas
        for line in file.readlines():
            # Las separamos por coma
            anime = line.strip().split(",")
            # Separamos los generos por slash
            anime[3] = anime[3].split("/")

            anime = Animes(*anime)

            anime_datos[anime.nombre] = (anime.rating, anime.estudio, anime.generos)

    return anime_datos
    # return anime


def cargar_consultas(path):
    # Abrimos el archivo de animes
    consultas = deque()

    with open(path, 'r') as file:
        # Leemos las lineas
        for line in file.readlines():
            # Los separamos por coma
            consulta = line.strip().split(";")
            consultas.append((consulta[0], list(consulta[1:])))


    return consultas
