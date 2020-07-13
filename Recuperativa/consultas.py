import json
from collections import defaultdict
from cargar_cursos import cargar_cursos

### Espacio para funciones auxiliares ###


### --------------------------------- ###


def filtrar_por_prerrequisitos(curso, dicc_de_cursos):
    nombre = curso['Sigla']
    cursos_requisitos = dicc_de_cursos[nombre]['Prerrequisitos']
    dict_pre = {key:value for key, value in dicc_de_cursos.items()
        if key in cursos_requisitos}
    return dict_pre

def filtrar_por_cupos(cupos, dicc_de_cursos):
    cursos = []
    for curso, info in dicc_de_cursos.items():
        for seccion, seccion_info in info['Secciones'].items():
            if int(seccion_info['Vacantes disponibles']) >= cupos:
                cursos.append(curso)
    dict_cupos = {key:value for key, value in dicc_de_cursos.items()
        if key in cursos}
    return dict_cupos

def filtrar_por(llave, string, dicc_de_cursos):
    cursos = dict()
    string = string.capitalize()
    for curso, info in dicc_de_cursos.items():
        if llave in ['Profesor', 'NRC']:
            secciones = {}
            for seccion, seccion_info in info['Secciones'].items():
                if string in seccion_info['Profesor']\
                        or string in seccion_info['NRC']:
                    secciones[seccion] = seccion_info
            if secciones:
                cursos[curso] = info
                cursos[curso]['Secciones'] = secciones


        elif llave in ['Sigla', 'Nombre']:
            if string.upper() in info['Sigla'] or string in info['Nombre']:
                cursos[curso] = info

    return cursos

def filtrar_por_modulos(modulos_deseados, dicc_de_cursos):
    cursos = dict()
    for curso, info in dicc_de_cursos.items():
        for seccion, seccion_info in info['Secciones'].items():
            for tipo, modulos in seccion_info['Modulos'].items():
                for modulo in modulos_deseados:
                    if (modulo[0], str(modulo[1])) in modulos:
                        cursos[curso] = info
    return cursos

def filtrar_por_cursos_compatibles(lista_nrc, dicc_de_cursos):

    cursos = dict()
    horarios = []
    for curso in lista_nrc:
        (sigla, info), = filtrar_por('NRC', curso, dicc_de_cursos).items()
        for seccion in info['Secciones'].values():
            for modulo in seccion['Modulos'].values():
                horarios.extend(modulo)

    for sigla, info in dicc_de_cursos.items():
        secciones = {}
        for seccion, seccion_info in info['Secciones'].items():
            topa = False
            for modulo in seccion_info['Modulos'].values():
                for md in modulo:
                    if md in horarios:
                        topa = True
            if not topa:
                secciones[seccion] = seccion_info
        if secciones:
            cursos[sigla] = info
            cursos[sigla]['Secciones'] = secciones
    return cursos

if __name__ == "__main__":

    semestre = "2020-1"
    cursos = cargar_cursos(semestre)

    # avanzada = cursos['IIC2233']
    # for sigla, info_curso in filtrar_por_prerrequisitos(avanzada, cursos).items():
    #     print(sigla, info_curso)
    #
    # for sigla, info_curso in filtrar_por_cupos(25, cursos).items():
    #     for nr_seccion, info_seccion in info_curso['Secciones'].items():
    #         print(sigla, nr_seccion, info_seccion['Vacantes disponibles'])

    # Filtrar por Profesor
    # resultado = filtrar_por('Profesor', 'cris', cursos)
    # for sigla, info_curso in resultado.items():
    #     for info_seccion in info_curso['Secciones'].values():
    #         print(info_seccion['Profesor'], sigla)

    # Filtrar por Sigla
    # resultado = filtrar_por('Sigla', 'iic2', cursos)
    # for sigla, info_curso in resultado.items():
    #     print(sigla)

    # Filtrar por NRC
    # resultado = filtrar_por('NRC', '211', cursos)
    # for sigla, info_curso in resultado.items():
    #     for info_seccion in info_curso['Secciones'].values():
    #         print(info_seccion['NRC'])

    # Filtrar por Nombre
    # resultado = filtrar_por('Nombre', 'cri', cursos)
    # for sigla, info_curso in resultado.items():
    #     print(info_curso['Nombre'])

    # Filtar por Modulo
    # for sigla, info_curso in filtrar_por_modulos([('V',1)], cursos).items():
    #     for nr_seccion, info_seccion in info_curso['Secciones'].items():
    #         print(sigla, nr_seccion, info_seccion['Modulos'])

    # Filtar por horarios
    # for sigla, info_curso in filtrar_por_cursos_compatibles(['10732', '10791', '21116', '15169', '10923', '18871', '23685', '10892', '10660', '10881'], cursos).items():
    #     for nr_seccion, info_seccion in info_curso['Secciones'].items():
    #         print(sigla, info_seccion['NRC'], info_seccion['Modulos'])
