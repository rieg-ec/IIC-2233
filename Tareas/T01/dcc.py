import parametros as pm

class DCC:

    def registrar_dccriatura():
        pass

    def dccriaturas_existentes(solo_nombres=True):
        with open('criaturas.csv', 'r') as f:
            for i in f.readlines().strip().split(','):
                if solo_nombres:
                    return i[0]
                else:
                    return i

    def calcular_aprobacion(magizoologo):
        pass

    def pagar(magizoologo):
        pass

    def fiscalizar(magizoologo):
        pass

    def vender_dccriatura(magizoologo):
        if magizoologo.licencia == "True" \
            and magizoologo.sickles >= min([pm.PRECIO_AUGUREY, pm.PRECIO_NIFFLER, pm.PRECIO_ERKLING]):
            opcion = input("\nQue DCCriatura desea adoptar?"
                           +"\n[0] Augurey: $75 Sickles"
                           +"\n[1] Niffler: $100 Sickles"
                           +"\n[2] Erkling: $125 Sickles"
                           +"\n"
                           +"\nIndique su opcion (0, 1 o 2): ")

            if opcion == "0":
                if magizoologo.sickles >= pm.PRECIO_AUGUREY:
                    magizoologo.sickles -= pm.PRECIO_AUGUREY
                    nombre_dccriatura = input("\nComo deseas llamarla?: ")
                    DCC.registrar_dccriatura
                    magizoologo.dccriaturas.append(nombre_dccriatura)
                    print(f"\nAugurey '{nombre_dccriatura}' comprado")
                else:
                    print("\nNo te alcanza para esta mascota")

            elif opcion == "1":
                if magizoologo.sickles >= pm.PRECIO_NIFFLER:
                    magizoologo.sickles -= pm.PRECIO_NIFFLER
                    magizoologo.dccriaturas.append("Niffler")
                    print("\nNiffler comprado")
                else:
                    print("\nNo te alcanza para esta mascota")

            elif opcion == "2":
                if magizoologo.sickles >= pm.PRECIO_ERKLING:
                    magizoologo.sickles -= pm.PRECIO_ERKLING
                    magizoologo.dccriaturas.append("Erkling")
                    print("\nErkling comprado")
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

            if opcion == "0":
                if magizoologo.sickles >= pm.PRECIO_TARTA_DE_MELAZA:
                    magizoologo.sickles -= pm.PRECIO_TARTA_DE_MELAZA
                    magizoologo.alimentos.append("Tarta de Melaza")
                    print("\nTarta de Melaza comprada")
                else:
                    print("\nNo tienes sickles suficientes para este alimento")

            elif opcion == "1":
                if magizoologo.sickles >= pm.PRECIO_HIGADO_DE_DRAGON:
                    magizoologo.sickles -= pm.PRECIO_HIGADO_DE_DRAGON
                    magizoologo.alimentos.append("Hígado de Dragón")
                    print("\nHígado de Dragón comprado")
                else:
                    print("\nNo tienes sickles suficientes para este alimento")

            elif opcion == "2":
                if magizoologo.sickles >= pm.PRECIO_BUÑUELO_DE_GUSARAJO:
                    magizoologo.sickles -= pm.PRECIO_BUÑUELO_DE_GUSARAJO
                    magizoologo.alimentos.append("Buñuelo de Gusarajo")
                    print("\nBuñuelo de Gusarajo comprado")
                else:
                    print("\nNo tienes sickles suficientes para este alimento")
            else:
                print("\nOpcion invalida")
        else:
            print("\nNo tienes dinero para alimentos")


    def mostrar_estado(magizoologo):
        pass
