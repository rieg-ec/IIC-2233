import parametros as pm
from collections import defaultdict
import magizoologos # which contains ABC module also
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
        (1) guarda los usuarios registrados en usuarios_registrados, y los nombres de estos en nombres
        (2) si el input del usuario es un usuario existente, crea un objeto Magizoologo con su nombre
        y llama al metodo modificar_parametros() para hacer un override de los parametros iniciales de la clase
        por los existentes
        (3) asigna el objeto magizoologo a self.magizoologo y lo pasa como argumento a MainMenu, clase que recibe
        el nombre y el objeto del magizoologo que inicia sesion como argumentos
        (4) llama a MainMenu.interfaz(), lo que significa ir al "menu de acciones"
        """

        usuarios_registrados = LoginMenu.usuarios_registrados(solo_nombres=False) # info completa
        nombres = LoginMenu.usuarios_registrados(solo_nombres=True) # solo para revisar si usuario
                                                                    # existe

        usuario_input = input("\nNombre de Usuario : ")

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

                    informacion = info # argumento que sera ocupado en modificar_parametros()

            magizoologo.modificar_parametros(*informacion)
            self.magizoologo =  magizoologo
            self.usuario = magizoologo.nombre
            print(f"\nBienvenido(a) {self.usuario}")
            siguiente_menu = MainMenu(self.usuario, self.magizoologo)
            siguiente_menu.interfaz() # Menu de acciones

        else:
            print("\nUsuario inexistente")
            return self.interfaz()

    def sign_up(self):
        usuarios_registrados = LoginMenu.usuarios_registrados(solo_nombres=True)

        usuario = input("\nNombre de usuario : ")

        if usuario.isalnum() == False:
            print("\nNombre de usuario no valido")

        elif usuario.lower() in usuarios_registrados:
            print("\nUsuario existente")

        else:
            tipo_mago = input("\nQue tipo de magizoologo desea ser:"
                              +"\n[0] Docencio"
                              +"\n[1] Tareo"
                              +"\n[2] Hibrido"
                              +"\n"
                              +"\nIndique su opcion (0, 1 o 2): ")

            if tipo_mago in pm.MAGOS.keys(): # para no ocupar tanto espacio con un dict
                lista_magos = (magizoologos.Docencio, magizoologos.Tareo, magizoologos.Hibrido)
                magizoologo = lista_magos[int(tipo_mago)](usuario) # instanciar magizoologo
                magizoologo.actualizar_archivo() # guardar informacion en magizoologos.csv

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
            pass
        elif opcion == "4":
            pass

    def pasar_al_dia_siguiente(self):
        pass
        # print("\n¡¡Has pasado al dia siguiente!!"
        #       +"\n***********************************"
        #       +"\nResumen de los eventos de hoy:"
        #       +"\n"
        #       +"\n"
        #       +f"\nCriaturas que enfermaron: {}"
        #       +f"\nCriaturas que escaparon: {}"
        #       +f"\nCriaturas hambrientas: {}"
        #       +f"\n{'salud'}"
        #       +f"\n{'hambre'}"
        #       +f"\n{'algo mas'}
        #       +"\n***********************************"
        #       +"\nNivel de aprobación: {}"
        #       +"\n{licencia}"
        #       +"\n{multa}"
        #       +"\n{pagos}"
        #       +"\nTu saldo actual es: {self.magizoologo.sickles} sickles")

    def volver(self):
        pass

    def salir():
        pass
