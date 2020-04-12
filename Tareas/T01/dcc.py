import parametros as pm
import dccriaturas
import random

class DCC:
    """
    to-do: maybe improve documentation, fix bugs if any
    """

    def dccriaturas_existentes():
        # nombres de dccriaturas existentes
        with open('criaturas.csv', 'r') as f:
            nombres = []
            for i in f.readlines():
                i = i.strip().split(',')
                nombres.append(i[0])

            return nombres

    def calcular_aprobacion(magizoologo):
        n_dccriaturas_sanas = 0
        n_dccriaturas_retenidas = 0
        n_dccriaturas_totales = len(magizoologo.dccriaturas_actuales)
        for dccriatura in magizoologo.dccriaturas_actuales:
            if dccriatura.estado_salud == "False":
                n_dccriaturas_sanas += 1
            if dccriatura.estado_escape == "False":
                n_dccriaturas_retenidas += 1

        aprobacion = (n_dccriaturas_retenidas + \
                      n_dccriaturas_sanas) * 100 / (2 * n_dccriaturas_totales)

        return aprobacion

    def pagar_a_magizoologo(magizoologo):
        aprobacion = DCC.calcular_aprobacion(magizoologo)
        cantidad_alimento = len(magizoologo.alimentos)
        nivel_magico = magizoologo.nivel_magico

        cantidad_a_pagar = int(4*aprobacion + 15*cantidad_alimento + 3*nivel_magico)
        magizoologo.sickles += cantidad_a_pagar
        return cantidad_a_pagar


    def fiscalizar(magizoologo):

        # guardar eventos de fiscalizacion:
        fiscalizaciones = {
            "multas por enfermedad": [],
            "multas por escape": [],
            "multas por salud minima": [],
            "total multas": 0,
            # si el magizoologo perdio o recupero la licencia en esta fiscalizacion,
            # "estado licencia" tomara como valor un bool que indica si la recupero o perdio,
            # y el motivo, el cual sera ocupado para indicarle al magizoologo la razon
            "estado licencia": [False]
        }

        if DCC.calcular_aprobacion(magizoologo) < pm.MINIMO_APROBACION_MAGIZOOLOGO and \
            magizoologo.licencia == "True":
            # pierde la licencia, el motivo es baja aprobacion
            magizoologo.licencia = "False"
            fiscalizaciones["estado licencia"] = ["perdio", "baja aprobacion"]

        elif DCC.calcular_aprobacion(magizoologo) >= pm.MINIMO_APROBACION_MAGIZOOLOGO and \
            magizoologo.licencia == "False":
            # recupera la licencia, el motivo es alta aprobacion
            magizoologo.licencia = "True"
            fiscalizaciones["estado licencia"] = ["recupero", "alta aprobacion"]


        # fiscalizar por escapes
        for dccriatura in magizoologo.dccriaturas_escapadas_hoy:
            n = random.random()
            if n <= pm.PROBABILIDAD_MULTA_ESCAPE:
                if magizoologo.sickles >= pm.MULTA_ESCAPE:
                    magizoologo.sickles -= pm.MULTA_ESCAPE
                    fiscalizaciones["multas por enfermedad"].append(dccriatura)

                # si no hay dinero y el magizoologo tiene licencia se le quita
                elif magizoologo.licencia == "True":
                    magizoologo.licencia = "False"
                    fiscalizaciones["estado licencia"] = ["perdio", "sin dinero para multa"]

        # fiscalizar por criaturas enfermas
        for dccriatura in magizoologo.dccriaturas_enfermas_hoy:
            n = random.random()
            if n <= pm.PROBABILIDAD_MULTA_ENFERMEDAD:
                if magizoologo.sickles >= pm.MULTA_ENFERMEDAD:
                    magizoologo.sickles -= pm.MULTA_ENFERMEDAD
                    fiscalizaciones["multas por escape"].append(dccriatura)
                # si no hay dinero y el magizoologo tiene licencia se le quita
                elif magizoologo.licencia == "True":
                    magizoologo.licencia = "False"
                    fiscalizaciones["estado licencia"] = ["perdio", "sin dinero para multa"]


        # fiscalisar por criaturas que alcanzaron salud minima
        for dccriatura in magizoologo.dccriaturas_salud_minima_hoy:
            n = random.random()
            if n <= pm.PROBABILIDAD_MULTA_SALUD:
                if magizoologo.sickles >= pm.MULTA_SALUD:
                    magizoologo.sickles -= pm.MULTA_SALUD
                    fiscalizaciones["multas por salud minima"].append(dccriatura)
                # si no hay dinero y el magizoologo tiene licencia se le quita
                elif magizoologo.licencia == "True":
                    magizoologo.licencia = "False"
                    fiscalizaciones["estado licencia"] = ["perdio", "sin dinero para multa"]


        return fiscalizaciones

    def vender_dccriatura(magizoologo):
        """
        Esta funcion hace:
        (1) revisa que el magizoologo tenga sickles suficientes para comprar al menos la
        mascota mas barata
        (2) revisa que el magizoologo tenga sickles para comprar la mascota que desea
        (3) una vez elegida la mascota, el usuario escoge el nombre
        (4) descuenta los sickles y crea el objeto dccriatura correspondiente y lo guarda en el
        parametro dccriaturas_actuales del magizoologo correspondiente como un objeto
        (5) registra la nueva dccriatura en el archivo dccriaturas.csv y en magizoologos.csv con sus
        correspondientes parametros llamando a DCC.registrar_dccriatura()
        """
        if magizoologo.licencia == "True" \
            and magizoologo.sickles >= min([pm.PRECIO_AUGUREY, pm.PRECIO_NIFFLER, pm.PRECIO_ERKLING]):
            opcion = input("\nQue DCCriatura desea adoptar?"
                           +f"\n[0] Augurey: ${pm.PRECIO_AUGUREY} Sickles"
                           +f"\n[1] Niffler: ${pm.PRECIO_NIFFLER} Sickles"
                           +f"\n[2] Erkling: ${pm.PRECIO_ERKLING} Sickles"
                           +f"\n"
                           +f"\nIndique su opcion (0, 1 o 2): ")
            opciones = {
                "0": ["Augurey", pm.PRECIO_AUGUREY],
                "1": ["Niffler", pm.PRECIO_NIFFLER],
                "2": ["Erkling", pm.PRECIO_ERKLING]
            }

            dccriaturas_clases = (dccriaturas.Augurey, dccriaturas.Niffler, dccriaturas.Erkling)

            if opcion in opciones.keys():
                # chequear que tenga sickles suficientes para la dccriatura escogida
                if magizoologo.sickles >= opciones[opcion][1]:
                    nombre_dccriatura = input("\nComo deseas llamar a "
                                            +f"tu nueva DCCriatura {opciones[opcion][0]}?: ")


                    if nombre_dccriatura not in DCC.dccriaturas_existentes():
                        # descontar valor de dccriatura
                        magizoologo.sickles -= opciones[opcion][1]
                        # instanciar dccriatura comprada
                        dccriatura = dccriaturas_clases[int(opcion)](nombre_dccriatura, magizoologo)
                        # agregar dccriatura a dccriaturas del magizoologo
                        magizoologo.dccriaturas_actuales.append(dccriatura)
                        print(f"\nDCCriatura {dccriatura.tipo} {dccriatura.nombre} adoptada")
                        # registrar en criaturas.csv
                        dccriatura.actualizar_archivo()
                        # actualizar informacion del magizoologo en magizoologos.csv
                        magizoologo.actualizar_archivo()
                    else:
                        print("\nNombre ya existente")

                else:
                    print("\nNo te alcanza para esta mascota")
            else:
                print("\nOpcion invalida")
        else:
            print("\nNo puedes adoptar mascotas")

    def vender_alimento(magizoologo):
        # chequear que magizoologo tenga sickles suficientes para el alimento mas barato
        if magizoologo.sickles >= min([pm.PRECIO_TARTA_DE_MELAZA, pm.PRECIO_HIGADO_DE_DRAGON, \
                                       pm.PRECIO_BUÑUELO_DE_GUSARAJO]):

            opcion = input("\nQue alimento deseas comprar? :"
                           +"\n[0] Tarta de melaza"
                           +"\n[1] Higado de dragon"
                           +"\n[2] Buñuelo de gusarajo"
                           +"\n"
                           +"\nIndique su opcion (0, 1 o 2): ")

            opciones = {
                "0": ["Tarta de Melaza", pm.PRECIO_TARTA_DE_MELAZA],
                "1": ["Hígado de Dragón", pm.PRECIO_HIGADO_DE_DRAGON],
                "2": ["Buñuelo de Gusarajo", pm.PRECIO_BUÑUELO_DE_GUSARAJO]
            }

            # chequear que tenga sickles suficientes para el alimento comprado
            if magizoologo.sickles >= opciones[opcion][1]:
                magizoologo.sickles -= opciones[opcion][1]
                magizoologo.alimentos.append(opciones[opcion][0])
                # actualizar informacion en magizoologos.csv
                magizoologo.actualizar_archivo()
                print(f"\n{opciones[opcion][0]} comprado")

            else:
                print(f"\nNo tienes sickles suficientes para {opciones[opcion][0]}")
        else:
            print("\nNo tienes sickles suficientes para ningun alimento")

    def mostrar_estado(magizoologo):
        """
        DONE, maybe improve documentation
        """
        print("\nEstado actual:"
              +"\n"
              +"\nValores de atributos relevantes:"
              +f"\nClase de magizoologo: {magizoologo.tipo}"
              +f"\nNombre: {magizoologo.nombre}"
              +f"\nCantidad de sickles: {magizoologo.sickles}"
              +f"\nEnergia actual: {magizoologo.energia_actual}"
              +f"\nEstado de licencia: {magizoologo.licencia}"
              +f"\nNivel de aprobacion: {DCC.calcular_aprobacion(magizoologo)}"
              +f"\nNivel magico: {magizoologo.nivel_magico}"
              +f"\nDestreza: {magizoologo.destreza}"
              +f"\nResponsabilidad: {magizoologo.responsabilidad}"
              +"\n")

        print("\nAlimentos comprados restantes y puntos de salud que otorgan: ")
        for alimento in magizoologo.alimentos:
            print(f"{alimento}: {pm.ALIMENTOS[alimento]}")

        print("\nDCCriaturas: ")
        for dccriatura in magizoologo.dccriaturas_actuales:
            print(f"\nTipo: {dccriatura.tipo}"
                +f"\nNombre: {dccriatura.nombre}"
                +f"\nNivel magico: {dccriatura.nivel_magico}"
                +f"\nPuntos de salud actuales: {dccriatura.salud_actual}"
                +f"\nEstado de salud (enferma o no): {dccriatura.estado_salud}"
                +f"\nNivel de hambre: {dccriatura.nivel_hambre}"
                +f"\nNivel de agresividad: {dccriatura.nivel_agresividad}")
