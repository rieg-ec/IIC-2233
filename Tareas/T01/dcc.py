import parametros as pm
import dccriaturas
import random

class DCC:


    def dccriaturas_existentes():
        with open('criaturas.csv', 'r') as f:
            nombres = []
            for i in f.readlines():
                i = i.strip().split(',')
                nombres.append(i[0])

            return nombres

    def calcular_aprobacion(magizoologo):
        pass

    def pagar(magizoologo):
        pass

    def fiscalizar(magizoologo):
        pass

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
                if magizoologo.sickles >= opciones[opcion][1]:
                    nombre_dccriatura = input("\nComo deseas llamar a "
                                            +f"tu nueva DCCriatura {opciones[opcion][0]}?: ")


                    if nombre_dccriatura not in DCC.dccriaturas_existentes():
                        magizoologo.sickles -= opciones[opcion][1]
                        dccriatura = dccriaturas_clases[int(opcion)](nombre_dccriatura) # crea objeto dccriatura
                        magizoologo.dccriaturas_actuales.append(dccriatura) # agregar a dccriaturas de magizoologo
                        print(f"\nDCCriatura {dccriatura.tipo} {dccriatura.nombre} adoptada")
                        dccriatura.actualizar_archivo() # registrar en criaturas.csv
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


            if magizoologo.sickles >= opciones[opcion][1]:
                magizologo.sickles -= opciones[opcion][1]
                magizoologo.alimentos.append(opciones[opcion][0])
                magizoologo.actualizar_archivo()
                print(f"\n{opcioneS[opcion[0]]} comprada")

            else:
                print("\nNo tienes sickles suficiente")



    def mostrar_estado(magizoologo):
        pass
