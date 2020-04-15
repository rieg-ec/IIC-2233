import parametros as pm
from abc import ABC, abstractmethod
import random

import magizoologos
import dccriaturas
import parametros as pm
import dcc
import mainmenu


class LoginMenu:
    def __init__(self):
        self.usuario = "Usuario anonimo" # Usuario actual
        self.magizoologo = None

    def usuarios_registrados(self, solo_nombres=True):
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
            print(f"Sesion {self.usuario} cerrada")

        else:
            print("\nOpcion invalida")

        if opcion != "3":
            return self.interfaz()

    def log_in(self):
        """
        Esta funcion crea el objeto magizoologo asociado al nombre de
        usuario y lo ocupa como argumento al llamar a la funcion MainMenu
        """

        # usuarios con toda la informacion en el archivo magizoologos.csv
        usuarios_registrados = self.usuarios_registrados(solo_nombres=False)
        # nombres de magizoologos para chequear existencia
        nombres = self.usuarios_registrados(solo_nombres=True)

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
            siguiente_menu = mainmenu.MainMenu(self.usuario, self.magizoologo)
            # ir a la interfaz del menu de acciones
            siguiente_menu.interfaz()

        else:
            print("\nUsuario inexistente")
            return self.interfaz()

    def sign_up(self):
        """
        Esta funcion crea el objeto magizoologo y dccriatura con
        valores iniciales al azar y lo guarda en magizoologos.csv y
        criaturas.csv
        """
        # nombres de magizoologos ya ocupados
        usuarios_registrados = self.usuarios_registrados(solo_nombres=True)

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
                        lista_magos = (magizoologos.Docencio, magizoologos.Tareo, \
                                        magizoologos.Hibrido)

                        # instanciar magizoologo
                        magizoologo = lista_magos[int(tipo_mago)](usuario)
                        # instanciar dccriatura
                        dccriatura = lista_dccriaturas[int(tipo_dccriatura)](nombre_dccriatura, \
                                                                                    magizoologo)
                        magizoologo.dccriaturas.append(dccriatura)
                        # guardar informacion de dccriatura en criaturas.csv
                        dccriatura.actualizar_archivo()
                        # guardar informacion de magizoologo en magizoologos.csv
                        magizoologo.actualizar_archivo()

                        print(f"\nUsuario {magizoologo.nombre} creado!")
                    else:
                        print("\nNombre de DCCriatura ocupado")
            else:
                print("\nOpcion invalida")
