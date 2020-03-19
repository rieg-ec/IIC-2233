from collections import defaultdict
from cargar import cargar_animes


def cantidad_animes_genero(animes):
    animes_per_genre = {}
    genre_types = []
    genre_count = []
    for i in range(len(animes)):
        genres = animes.values()[i][2]
        for i in genres:
            genre_count.append(i)
            if i not in genre_types:
                genre_types.append(i)

    for i in genre_types:
        animes_per_genre[i] = genre_count.count(i)

    return animes_per_genre

def generos_distintos(anime, animes):
    pass


def promedio_rating_genero(animes):
    pass


animes = cargar_animes('animes.csv')
