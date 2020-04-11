

ESTADO_LICENCIA_INICIAL = "True"
ESTADO_HABILIDAD_INICIAL = "True"

MINIMO_APROBACION_MAGIZOOLOGO = 60

NIVEL_MAGICO_DOCENCIO = (40, 60)
DESTREZA_DOCENCIO = (30, 40)
ENERGIA_DOCENCIO = (40, 50)
RESPONSABILIDAD_DOCENCIO = (15, 20)


NIVEL_MAGICO_TAREO = (40, 55)
DESTREZA_TAREO = (40, 50)
ENERGIA_TAREO = (35, 45)
RESPONSABILIDAD_TAREO = (10, 25)

NIVEL_MAGICO_HIBRIDO = (35, 45)
DESTREZA_HIBRIDO = (30, 50)
ENERGIA_HIBRIDO = (50, 55)
RESPONSABILIDAD_HIBRIDO = (15, 25)

PARAMETROS_MAGIZOOLOGOS = [
    [NIVEL_MAGICO_DOCENCIO, DESTREZA_DOCENCIO, ENERGIA_DOCENCIO, RESPONSABILIDAD_DOCENCIO],
    [NIVEL_MAGICO_TAREO, DESTREZA_TAREO, ENERGIA_TAREO, RESPONSABILIDAD_TAREO],
    [NIVEL_MAGICO_HIBRIDO, DESTREZA_HIBRIDO, ENERGIA_HIBRIDO, RESPONSABILIDAD_HIBRIDO]
]

ALIMENTOS = {
    "Tarta de Melaza": 15,
    "Hígado de Dragón": 10,
    "Buñuelo de Gusarajo": 5
}

PRECIO_AUGUREY = 75
PRECIO_NIFFLER = 125
PRECIO_ERKLING = 125

ESTADO_SALUD_INICIAL_DCCRIATURAS = "False"
ESTADO_ESCAPE_INICIAL_DCCRIATURAS = "False"
HAMBRE_INICIAL_DCCRIATURAS = "satisfecha"
DIAS_SIN_COMER_INICIAL_DCCRIATURAS = 0

SALUD_MINIMA_DCCRIATURAS = 1

NIVEL_MAGICO_AUGUREY = (20, 25)
PUNTOS_SALUD_AUGUREY = (35, 45)
PROBABILIDAD_ESCAPE_AUGUREY = 0.2
PROBABILIDAD_ENFERMARSE_AUGUREY = 0.3
MAX_DIAS_SIN_COMER_AUGUREY = 3
NIVEL_AGRESIVIDAD_AUGUREY = "inofensiva"

NIVEL_MAGICO_NIFFLER = (10, 20)
PUNTOS_SALUD_NIFFLER = (20, 30)
PROBABILIDAD_ESCAPE_NIFFLER = 0.3
PROBABILIDAD_ENFERMARSE_NIFFLER = 0.2
MAX_DIAS_SIN_COMER_NIFFLER = 2
NIVEL_AGRESIVIDAD_NIFFLER = "arisca"
NIVEL_CLEPTO_NIFFLER = (5, 10)

NIVEL_MAGICO_ERKLING = (30, 45)
PUNTOS_SALUD_ERKLING = (50, 60)
PROBABILIDAD_ESCAPE_ERKLING = 0.5
PROBABILIDAD_ENFERMARSE_ERKLING = 0.3
MAX_DIAS_SIN_COMER_ERKLING = 2
NIVEL_AGRESIVIDAD_ERKLING = "peligrosa"

EFECTO_HAMBRE = {
    "satisfecha": 0,
    "hambrienta": 15
}
EFECTO_AGRESIVIDAD = {
    "inofensiva": 0,
    "arisca": 15,
    "peligrosa": 40
}


# usado en la funcion dcc.vender_dccriatura para crear dccriatura usando "opcion" como index
PARAMETROS_DCCRIATURAS = [
    [NIVEL_MAGICO_AUGUREY, PUNTOS_SALUD_AUGUREY, PROBABILIDAD_ESCAPE_AUGUREY, \
     PROBABILIDAD_ENFERMARSE_AUGUREY, MAX_DIAS_SIN_COMER_AUGUREY, NIVEL_AGRESIVIDAD_AUGUREY], \
    [NIVEL_MAGICO_NIFFLER, PUNTOS_SALUD_NIFFLER, PROBABILIDAD_ESCAPE_NIFFLER, \
     PROBABILIDAD_ENFERMARSE_NIFFLER, MAX_DIAS_SIN_COMER_NIFFLER, NIVEL_AGRESIVIDAD_NIFFLER, \
     NIVEL_CLEPTO_NIFFLER], \
    [NIVEL_MAGICO_ERKLING, PUNTOS_SALUD_ERKLING, PROBABILIDAD_ESCAPE_ERKLING, \
     PROBABILIDAD_ENFERMARSE_ERKLING, MAX_DIAS_SIN_COMER_ERKLING, NIVEL_AGRESIVIDAD_ERKLING]
]



PRECIO_TARTA_DE_MELAZA = 10
PRECIO_HIGADO_DE_DRAGON = 15
PRECIO_BUÑUELO_DE_GUSARAJO = 3

SICKLES_INICIALES = 500


MULTA_ESCAPE = 50
PROBABILIDAD_MULTA_ESCAPE = 0.5

MULTA_ENFERMEDAD = 70
PROBABILIDAD_MULTA_ENFERMEDAD = 0.7

MULTA_SALUD = 150
PROBABILIDAD_MULTA_SALUD = 1
