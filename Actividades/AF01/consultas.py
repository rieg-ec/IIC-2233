from collections import defaultdict
from cargar import cargar_animes, cargar_consultas


def cantidad_animes_genero(animes):
    animes_per_genre = {}

    genre_types = []
    genre_count = []

    for i in animes:
        for x in i[2]:
            if x not in genre_types:
                genre_types.append(x)
            genre_count.append(x)

    for i in genre_types:
        animes_per_genre[i] = genre_count.count(i)


    return animes_per_genre

def generos_distintos(anime, animes):
    return animes


def promedio_rating_genero(animes):
    ratings_per_genre = {}
    genres = {}

    for i in animes:
        for x in i:
            genres[x] = 0

    for i in animes:
        for x in i[2]:
