from collections import defaultdict
from cargar import cargar_animes, cargar_consultas


def cantidad_animes_genero(animes):
    genres = dict()

    for i in animes:
        for x in i[2]:
            genres[x] = 0 # instantiate dict with 0

    for i in animes:
        for x in genres.keys():
            if x in i[2]:
                genres[x] += 1

    return genres


def generos_distintos(anime, animes):
    animes_list = []

    for i in animes:
        for x in i[2]:
            if x not in animes_list:
                animes_list.append(x)

    for i in anime[2]:
        if i in animes_list:
            animes_list.remove(i)

    return set(animes_list)



def promedio_rating_genero(animes):
    genres_dict = dict() # values = (a, b) --> a = rating, b = times it is rated

    # instantiate genres
    for i in animes:
        for x in i[2]:
            genres_dict[x] = [0, 0]

    for i in animes:
        genres = set(i[2])
        for x in genres:
            genres_dict[x][0] += int(i[0])
            genres_dict[x][1] += 1

    for i in genres_dict.keys():
        genres_dict[i] = genres_dict[i][0] / genres_dict[i][1]

    return genres_dict
