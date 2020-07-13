from os import path
import json

def traducir_modulos(modulos_string):
    tipos_modulo = modulos_string.split(';')
    modulos_y_horarios = [
        i.split('#') for i in tipos_modulo]

    default_dict = {tipo[0]: [] for tipo in modulos_y_horarios}

    for tipo in modulos_y_horarios:
        try:
            dias, modulos = tipo[1].split(':')
            dias = dias.split(',')
            modulos = modulos.split(',')
            for dia in dias:
                for modulo in modulos:
                    default_dict[tipo[0]].append((dia, int(modulo)))

        except IndexError:
            pass

    return default_dict

def cargar_cursos(semestre):
    archivo = path.join('datos', f'{semestre}.json')
    try:
        with open(archivo, 'r') as archivo_json:
            data = archivo_json.read()
            dict_data = json.loads(data)
            cursos = dict_data.keys()
            for curso in cursos:
                pr_orig = dict_data[curso]['Prerrequisitos']
                ramos = pr_orig.split(';')
                ramos = [i for i in ramos if i.startswith('IIC')]
                dict_data[curso]['Prerrequisitos'] = ramos
                secciones_orig = dict_data[curso]['Secciones']
                for seccion in secciones_orig:
                    datos = dict_data[curso]['Secciones'][seccion]['Modulos']
                    modulos_traducidos = traducir_modulos(datos)
                    dict_data[curso]['Secciones'][seccion]['Modulos'] = modulos_traducidos

            return dict_data

    except FileNotFoundError:
        print('semestre no existe')



if __name__ == "__main__":

    semestre = "2020-1" # Cambiar para probar

    cursos = cargar_cursos(semestre)

    with open("resultado_cargado.json", "wt", encoding="utf-8") as archivo:
        json.dump(cursos, archivo, indent=4)
