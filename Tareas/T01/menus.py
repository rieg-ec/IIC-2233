import parametros as pm
from collections import defaultdict
from abc import ABC, abstractmethod
import magizoologos
import dccriaturas
import random
import dcc

class LoginMenu:
    def __init__(self):
        self.usuario = "Usuario anonimo" # Usuario actual
        self.magizoologo = None

    @staticmethod
    def usuarios_registrados(solo_nombres=True):
        """
        esta funcion retorna los nombres de usuarios registrados, o toda la información contenida
        en las lineas de magizoologos.csv, dependiendo el argumento que se le entregue.
        """
        with open('magizoologos.csv', 'r') as f:
            usuarios_registrados = []
            nombres = []
            for i in f.readlines():
                user = i.strip().split(',')
                nombre = user[0]
                usuarios_registrados.append(user)
                nombres.append(nombre.lower()) # lower() para no distinguir entre
                                                # uppercase y lowercase en los nombres de usuario
            f.close()

        if solo_nombres == False:
            return usuarios_registrados
        else:
            return nombres

    def interfaz(self):
        opcion = input("\n***** Menu de inicio *****"
                       +"\nSeleccion una opcion:"
                       +"\n[1] Crear Magizoologo"
                       +"\n[2] Cargar Magizoologo"
                       +"\n[3] Salir"
                       +"\n"
                       +"\nIndique su opcion (1, 2 o 3): ")

        if opcion == "1":
            self.sign_up()

        elif opcion == "2":
            self.log_in()

        elif opcion == "3":
            pass

        else:
            print("\nOpcion invalida")

        if opcion != "3":
            return self.interfaz()


    def log_in(self):
        """
        Esta funcion hace:
        (1) guarda los usuarios registrados en usuarios_registrados,
        y los nombres de estos en nombres
        (2) si el input del usuario es un usuario existente, crea un objeto Magizoologo
        con su nombre y llama al metodo modificar_parametros() para hacer un override
        de los parametros iniciales de la clase por los existentes
        (3) asigna el objeto magizoologo a self.magizoologo y lo pasa como argumento a MainMenu,
        clase que recibe el nombre y el objeto del magizoologo que inicia sesion como argumentos
        (4) llama a MainMenu.interfaz(), lo que significa ir al "menu de acciones"

        TO-DO:

        - documentar mejor
        """

        # usuarios con toda la informacion en el archivo magizoologos.csv
        usuarios_registrados = LoginMenu.usuarios_registrados(solo_nombres=False)
        # nombres de magizoologos para chequear existencia
        nombres = LoginMenu.usuarios_registrados(solo_nombres=True)

        usuario_input = input("\nNombre de Usuario : ")

        # ignorar mayusculas
        if usuario_input.lower() in nombres:
            for info in usuarios_registrados:
                nombre = info.pop(0)
                tipo = info.pop(0)
                if usuario_input.lower() == nombre.lower():
                    if tipo == "Docencio":
                        magizoologo = magizoologos.Docencio(nombre)
                    elif tipo == "Tareo":
                        magizoologo = magizoologos.Tareo(nombre)
                    elif tipo == "Híbrido":
                        magizoologo = magizoologos.Hibrido(nombre)

                    # argumento de modificar_parametros() del magizoologo
                    informacion = info


            # hacer override a los atributos generados random por los ya existentes
            magizoologo.modificar_parametros(*informacion)
            # guardar objeto magizoologo
            self.magizoologo =  magizoologo
            # guardar nombre de magizoologo aparte por conveniencia
            self.usuario = magizoologo.nombre
            print(f"\nBienvenido(a) {self.usuario}")
            # instanciar menu de acciones con usuario loggeado como argumento
            siguiente_menu = MainMenu(self.usuario, self.magizoologo)
            # ir a la interfaz del menu de acciones
            siguiente_menu.interfaz()

        else:
            print("\nUsuario inexistente")
            return self.interfaz()

    def sign_up(self):
        """
        TO-DO:

        - explicar funcionamiento y documentar mejor
        """
        # nombres de magizoologos ya ocupados
        usuarios_registrados = LoginMenu.usuarios_registrados(solo_nombres=True)

        usuario = input("\nNombre de usuario : ")

        # chequear que sea alfanumerico
        if usuario.isalnum() == False:
            print("\nNombre de usuario no valido")

        # chequear que no este ocupado
        elif usuario.lower() in usuarios_registrados:
            print("\nUsuario existente")

        else:
            tipo_mago = input("\nQue tipo de magizoologo desea ser:"
                              +"\n[0] Docencio"
                              +"\n[1] Tareo"
                              +"\n[2] Hibrido"
                              +"\n"
                              +"\nIndique su opcion (0, 1 o 2): ")

            if tipo_mago in ["0", "1", "2"]:
                tipo_dccriatura = input("\nQue DCCriatura deseas adoptar? :"
                                   +"\n[0] Augurey"
                                   +"\n[1] Niffler"
                                   +"\n[2] Erkling"
                                   +"\n"
                                   +"\nIndique su opcion (0, 1 o 2): ")
                if tipo_dccriatura in ["0", "1", "2"]:
                    nombre_dccriatura = input("\nComo deseas llamar a tu DCCriatura?: ")
                    if nombre_dccriatura not in dcc.DCC.dccriaturas_existentes():

                        lista_dccriaturas = (dccriaturas.Augurey, \
                                             dccriaturas.Niffler, dccriaturas.Erkling)
                        lista_magos = (magizoologos.Docencio, magizoologos.Tareo, magizoologos.Hibrido)

                        # instanciar magizoologo
                        magizoologo = lista_magos[int(tipo_mago)](usuario)
                        # instanciar dccriatura
                        dccriatura = lista_dccriaturas[int(tipo_dccriatura)](nombre_dccriatura)
                        magizoologo.dccriaturas_actuales.append(dccriatura)
                        # guardar informacion de dccriatura en criaturas.csv
                        dccriatura.actualizar_archivo()
                        # guardar informacion de magizoologo en magizoologos.csv
                        magizoologo.actualizar_archivo()

                        print(f"\nUsuario {magizoologo.nombre} creado!")
                    else:
                        print("\nNombre de DCCriatura ocupado")
            else:
                print("\nOpcion invalida")



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
            print(self.magizoologo)

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
            self.magizoologo.alimentar_dccriatura()

        elif opcion == "2":
            self.magizoologo.recuperar_dccriatura()

        elif opcion == "3":
            self.magizoologo.sanar_dccriatura()

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
        """
        TO-DO:
        # 1- imprimir criaturas que enfermaron --> se debe simular
        # 2- imprimir criaturas que escaparon --> se debe simular
        # 3- imprimir criaturas que estan hambrientas  --> informacion existente
        4- imprimir eventos de criaturas:
            1- cuales perdieron salud por hambre o por enfermedad

        # 5- imprimir nivel de aprobacion
        # 6- imprimir estado de licencia (si continua, si la pierde o si ya la habia perdido)
        # 7- imprimir multas --> DCC.fiscalizar retornara dict con esta info
        # 8- imprimir pago del DCC --> llamar a pagar_a_magizoologo
        # 9- imprimir pagos en multas --> DCC.fiscalizar retorna tambien esta info
        # 10- imprimir saldo actual
        """

        # resetear
        self.magizoologo.dccriaturas_escapadas_hoy = []
        self.magizoologo.dccriaturas_enfermas_hoy = []
        self.magizoologo.dccriaturas_salud_minima_hoy = []

        DCCriaturas_hambrientas = [i for i in self.magizoologo.dccriaturas_actuales if i.nivel_hambre == "hambrienta"]

        # simular eventos de DCCriaturas:
        for dccriatura in self.magizoologo.dccriaturas_actuales:
            # retorna True si la dccriatura se escapa
            if dccriatura.escaparse():
                self.magizoologo.dccriaturas_escapadas_hoy.append(dccriatura)

            # retorna True si la dccriatura se enferma
            if dccriatura.enfermarse():
                self.magizoologo.dccriaturas_enfermas_hoy.append(dccriatura)


            if dccriatura.salud_actual <= pm.SALUD_MINIMA_DCCRIATURAS:
                self.magizoologo.dccriaturas_salud_minima_hoy.append(dccriatura)

        print("\nHas pasado al dia siguiente:")
        print("***********************************************")
        print("Resumen de los eventos de hoy:")
        print("")
        print(f"Criaturas que enfermaron: {[i.nombre for i in self.magizoologo.dccriaturas_enfermas_hoy]}")
        print(f"Criaturas que escaparon: {[i.nombre for i in self.magizoologo.dccriaturas_escapadas_hoy]}")
        print(f"Criaturas hambrientas: {[i.nombre for i in DCCriaturas_hambrientas]}")
        """TO-DO: mostrar criaturas que perdieron salud"""
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
        for dccriatura in self.magizoologo.dccriaturas_actuales:
            dccriatura.actualizar_archivo()
