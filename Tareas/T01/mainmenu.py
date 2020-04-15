from abc import ABC, abstractmethod
import random

import parametros as pm
import magizoologos
import dccriaturas
import dcc


class MainMenu:
    def __init__(self, usuario, magizoologo):
        self.usuario = usuario
        self.magizoologo = magizoologo


    def interfaz(self):
        opcion = input("\n***** Menu de acciones *****"
                       + "\nSeleccione una opcion:"
                       +"\n[1] Menu cuidar DCCriaturas"
                       +"\n[2] Menu DCC"
                       +"\n[3] Pasar al dia siguiente"
                       +"\n[4] Volver atras (cerrar sesion)"
                       +"\n"
                       +"\nIndique su opcion (1, 2, 3, 4 o 5): ")

        if opcion == "1": # Cuidar criatura
            self.cuidar_dccriaturas()

        elif opcion == "2": # DCC
            self.dcc()

        elif opcion == "3": # Pasar al dia siguiente
            self.pasar_al_dia_siguiente()

        elif opcion == "4":
            print(f"\nHasta luego {self.usuario}")

        else:
            print("\nOpcion invalida")

        if opcion != "4":
            return self.interfaz()

    def cuidar_dccriaturas(self):
        opcion = input("\n***** Menu cuidar DCCriaturas *****"
                       +"\nSeleccione una opcion:"
                       +"\n[1] Alimentar DCCriatura"
                       +"\n[2] Recuperar DCCriatura"
                       +"\n[3] Sanar DCCriatura"
                       +"\n[4] Usar habilidad especial"
                       +"\n[5] Volver atras"
                       +"\n"
                       +"\nIndique su opcion (1, 2, 3, 4 o 5): ")

        if opcion == "1":
            if self.magizoologo.energia_actual >= pm.COSTO_ENERGETICO_ALIMENTAR:
                # alimentos.getter retorna False si no hay alimentos:
                if self.magizoologo.alimentos:

                    print("\nQue DCCriatura deseas alimentar?: ")
                    print("")

                    for index, dccriatura in enumerate(self.magizoologo.dccriaturas):
                        print(f"[{index}] {dccriatura.nombre}"
                              +f"({dccriatura.tipo}): {dccriatura.nivel_hambre}")


                    opciones = ', '.join(str(i) for i in range(len(self.magizoologo.dccriaturas)))
                    mensaje = f"\nIndique su opcion: ({opciones}): "
                    opcion_dccriatura = input(mensaje)

                    if opcion_dccriatura in [str(i) for i in \
                                             range(len(self.magizoologo.dccriaturas))]:

                        print("\nQue alimento desea darle?")
                        print("")
                        for index, alimento in enumerate(self.magizoologo.alimentos):
                            print(f"[{index}] {alimento} (+{pm.ALIMENTOS[alimento]} de vida)")


                        opciones = ', '.join(str(i) for i in range(len(self.magizoologo.alimentos)))
                        mensaje = f"\nIndique su opcion ({opciones}): "
                        opcion_alimento = input(mensaje)

                        # chequear input valido
                        if opcion_alimento in [str(i) for i in \
                                               range(len(self.magizoologo.alimentos))]:

                            alimento = self.magizoologo.alimentos[int(opcion_alimento)]
                            dccriatura = self.magizoologo.dccriaturas[int(opcion_dccriatura)]
                            self.magizoologo.alimentar_dccriatura(alimento, dccriatura)
                        else:
                            print("\nOpcion invalida")
                    else:
                        print("\nOpcion invalida")
                else:
                    print("\nNo tienes alimentos")
            else:
                print("\nNo tienes energia suficiente")

        elif opcion == "2":
            if self.magizoologo.energia_actual >= pm.COSTO_ENERGETICO_RECUPERAR:

                dccriaturas_escapadas = [i for i in self.magizoologo.dccriaturas if \
                                                                i.estado_escape == "True"]
                if dccriaturas_escapadas:
                    print("\nQue DCCriatura deseas recuperar?: ")
                    print("")
                    for index, dccriatura in enumerate(dccriaturas_escapadas):
                        if dccriatura != "":
                            print(f"[{index}] {dccriatura.nombre} ({dccriatura.tipo})")

                    opciones = ', '.join(str(i) for i in range(len(self.magizoologo.dccriaturas)))
                    mensaje = f"\nIndique su opcion ({opciones}): "
                    opcion_dccriatura = input(mensaje)

                    if opcion_dccriatura in [str(i) for i in \
                                             range(len(self.magizoologo.dccriaturas))]:

                        dccriatura = self.magizoologo.dccriaturas[int(opcion_dccriatura)]
                        if dccriatura.estado_escape == "True":
                            self.magizoologo.recuperar_dccriatura(dccriatura)
                        else:
                            print("\nEsta DCCriatura esta en cautiverio")
                    else:
                        print("\nOpcion invalida")
                else:
                    print("\nTodas las DCCcriaturas estan en cautiverio")
            else:
                print("\nNo tienes energia suficiente")

        elif opcion == "3":
            if self.magizoologo.energia_actual >= pm.COSTO_ENERGETICO_SANAR:

                dccriaturas_enfermas = [i for i in self.magizoologo.dccriaturas if i.estado_salud == "True"]
                if dccriaturas_enfermas:
                    print("\nQue DCCriatura deseas sanar?: ")
                    print("")
                    for index, dccriatura in enumerate(self.magizoologo.dccriaturas):
                        print(f"[{index}] {dccriatura.nombre} ({dccriatura.tipo})")

                    opciones = ', '.join(str(i) for i in range(len(self.magizoologo.dccriaturas)))
                    mensaje = f"\nIndique su opcion ({opciones}: "
                    opcion_dccriatura = input(mensaje)

                    if opcion_dccriatura in [str(i) for i in range(len(self.magizoologo.dccriaturas))]:
                        dccriatura = self.magizoologo.dccriaturas[int(opcion_dccriatura)]
                        if dccriatura.estado_salud == "True":

                            self.magizoologo.sanar_dccriatura(dccriatura)

                        else:
                            print("\nEsta DCCriatura esta sana")
                    else:
                        print("\nOpcion invalida")
                else:
                    print("\nTodas las DCCriaturas estan sanas")
            else:
                print( "\nNo tienes energia suficiente")

        elif opcion == "4":
            self.magizoologo.habilidad_especial()

        elif opcion == "5":
            pass

    def dcc(self):
        opcion = input("\n***** Menu DCC *****"
                       +"\nSeleccione una opcion:"
                       +"\n[1] Adoptar una DCCriatura"
                       +"\n[2] Comprar alimentos"
                       +"\n[3] Ver estado de magizoologo"
                       +"\n[4] Volver atras"
                       +"\n"
                       +"\nIndique su opcion (1, 2, 3, o 4): ")
        if opcion == "1":
            dcc.DCC.vender_dccriatura(self.magizoologo)
        elif opcion == "2":
            dcc.DCC.vender_alimento(self.magizoologo)
        elif opcion == "3":
            dcc.DCC.mostrar_estado(self.magizoologo)
        elif opcion == "4":
            pass

    def pasar_al_dia_siguiente(self):

        # resetear
        self.magizoologo.dccriaturas_escapadas_hoy = []
        self.magizoologo.dccriaturas_enfermas_hoy = []
        self.magizoologo.dccriaturas_salud_minima_hoy = []
        
        self.magizoologo.energia_actual = self.magizoologo.energia_total

        DCCriaturas_hambrientas = [i for i in self.magizoologo.dccriaturas if \
                                                            i.nivel_hambre == "hambrienta"]

        print("\n***********************************************")
        print("Has pasado al dia siguiente:")
        print("***********************************************")
        print("Resumen de los eventos de hoy:")
        print("")
        # simular eventos de DCCriaturas:
        for dccriatura in self.magizoologo.dccriaturas:

            # descontar salud si la criatura esta hambrienta
            if dccriatura.nivel_hambre == "hambrienta":
                dccriatura.salud_actual -= pm.SALUD_POR_DIA_SIN_COMER
                print(f"{dccriatura.nombre} perdio salud por estar hambrienta")

            # verificar si la dccriatura fue alimentada hoy
            if not dccriatura.alimentada_hoy:
                dccriatura.dias_sin_comer += 1

            if dccriatura.estado_salud == "True":
                dccriatura.salud_actual -= pm.SALUD_POR_DIA_ENFERMA
                print(f"{dccriatura.nombre} perdio salud por estar enferma")

            if dccriatura.salud_actual <= pm.SALUD_MINIMA_DCCRIATURAS:
                self.magizoologo.dccriaturas_salud_minima_hoy.append(dccriatura)

            # retorna True si la dccriatura se escapa
            if dccriatura.escaparse():
                self.magizoologo.dccriaturas_escapadas_hoy.append(dccriatura)

            # retorna True si la dccriatura se enferma
            if dccriatura.enfermarse():
                self.magizoologo.dccriaturas_enfermas_hoy.append(dccriatura)



            dccriatura.habilidad_especial()

        criaturas_enfermas_hoy = [i.nombre for i in self.magizoologo.dccriaturas_enfermas_hoy]
        print(f"Criaturas que enfermaron hoy: {criaturas_enfermas_hoy}")

        criaturas_escapadas_hoy = [i.nombre for i in self.magizoologo.dccriaturas_escapadas_hoy]
        print(f"Criaturas que escaparon hoy: {criaturas_escapadas_hoy}")

        criaturas_enfermas_total = [i.nombre for i in self.magizoologo.dccriaturas if \
                                                                i.estado_salud == "True"]
        print(f"Criaturas enfermas: {criaturas_enfermas_total}")

        criaturas_escapadas_total = [i.nombre for i in self.magizoologo.dccriaturas if \
                                                            i.estado_escape == "True"]
        print(f"Criaturas escapadas: {criaturas_escapadas_total}")

        print(f"Criaturas hambrientas: {[i.nombre for i in DCCriaturas_hambrientas]}")
        print("***********************************************")
        print(f"Nivel de aprobacion: {dcc.DCC.calcular_aprobacion(self.magizoologo)}")
        # fiscalizar al magizoologo y guardar la informacion de la fiscalizacion en
        # variable "fiscalizacion":
        fiscalizaciones = dcc.DCC.fiscalizar(self.magizoologo)
        # si el magizoologo perdio su licencia:
        if fiscalizaciones["estado licencia"][0] == "perdio":
            print(f"Perdiste tu licencia, motivo: {fiscalizaciones['estado licencia'][1]}")
        # si el magizoologo recupero su licencia:
        elif fiscalizaciones["estado licencia"][0] == "recupero":
            print("Felicidades, recuperaste tu licencia")
        # si el magizoologo continua sin licencia:
        elif self.magizoologo.licencia == "False":
            print("Continuas sin licencia")
        # si el magizoologo continua con su licencia:
        elif self.magizoologo.licencia == "True":
            print("Felicidades, continuas con tu licencia")


        for dccriatura in fiscalizaciones["multas por enfermedad"]:
            if dccriatura:
                print(f"Recibiste una multa porque {dccriatura.nombre} enfermo")

        for dccriatura in fiscalizaciones["multas por escape"]:
            if dccriatura:
                print(f"Recibiste una multa porque {dccriatura.nombre} escapo")

        for dccriatura in fiscalizaciones["multas por salud minima"]:
            if dccriatura:
                print(f"Recibiste una multa porque {dccriatura.nombre} llego a su salud minima")

        # pagar a magizoologo e imprimir cantidad pagada:
        print(f"El DCC te ha pagado {dcc.DCC.pagar_a_magizoologo(self.magizoologo)} sickles")
        print(f"Se te han descontado {fiscalizaciones['total multas']} sickles en multas")
        print(f"Tu saldo actual es: {self.magizoologo.sickles} sickles")

        self.magizoologo.actualizar_archivo()
        for dccriatura in self.magizoologo.dccriaturas:
            dccriatura.actualizar_archivo()
