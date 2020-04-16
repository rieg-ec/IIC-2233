

def verificar_rut(rut, datos_registrados):
    if "." in rut or "-" not in rut:
        raise ValueError('RUT viene con puntos o sin guión')

    if rut in datos_registrados.keys():
        return datos_registrados[rut]
    return

def permiso_clave_unica(rut, datos_registrados):
    if rut not in datos_registrados.keys():
        raise KeyError('No puedes solicitar clave única. Impostor!')


def permiso_asistencia_medica(hora):
    if not hora.isdigit():
        raise TypeError('El formato de la hora es incorrecto.')


def permiso_servicios_basicos(persona, solicitud, comunas_cuarentena):

    if ((solicitud.salida not in comunas_cuarentena) and
        (solicitud.llegada not in comunas_cuarentena)):
        raise ValueError('La comuna no está en cuarentena')

    elif solicitud.salida != persona.domicilio:
        raise ValueError('No está saliendo desde su domicilio.')
