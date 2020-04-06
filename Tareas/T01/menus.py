import parametros

class LoginMenu():
    def __init__(self):
        self.usuario = "Usuario anonimo" # Usuario actual

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

    @staticmethod
    def registrar_usuario(nombre, tipo):
        usuarios_registrados = LoginMenu.usuarios_registrados(solo_nombres=False)
        with open('magizoologos.csv', 'a') as f:
            f.write(f"{nombre},{tipo}")
            f.write("\n")

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

        else:
            print("\nOpcion invalida")

        if opcion != "3":
            return self.interfaz()


    def log_in(self):

        usuarios_registrados = LoginMenu.usuarios_registrados(solo_nombres=True)

        usuario = input("\nNombre de Usuario : ")
        if usuario.lower() in usuarios_registrados:
            self.usuario = usuario
            menu = MainMenu(self.usuario)
            print(f"\nBienvenido {self.usuario}")
            menu.interfaz() # ir a menu de acciones

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
                              +"\n[1] Docencio"
                              +"\n[2] Tareo"
                              +"\n[3] Hibrido"
                              +"\n"
                              +"\nIndique su opcion (1, 2 o 3): ")

            if tipo_mago in parametros.magos.keys():
                LoginMenu.registrar_usuario(usuario, parametros.magos[tipo_mago])

            else:
                print("\nOpcion invalida")

        return self.interfaz()



class MainMenu():
    def __init__(self, usuario):
        self.usuario = usuario

    def interfaz(self):
        opcion = input("\n***** Menu de acciones *****"
                       + "\nSeleccione una opcion:"
                       +"\n[1] Menu de cuidar DCCriaturas"
                       +"\n[2] Menu DCC"
                       +"\n[3] Pasar al dia siguiente"
                       +"\n[4] Volver atras"
                       +"\n"
                       +"\nIndique su opcion (1, 2, 3, 4 o 5): ")

        if opcion == "1": # Cuidar criatura
            self.cuidar_dccriaturas()

        elif opcion == "2": # DCC
            self.dcc()

        elif opcion == "3": # Pasar al dia siguiente
            self.pasar_al_dia_siguiente()

        elif opcion == "4":
            print("\nSesion cerrada")
            pass # no hacer nada

        else:
            print("\nOpcion invalida")

        if opcion != "4":
            return self.interfaz()

    def cuidar_dccriaturas(self):
        pass

    def dcc(self):
        pass

    def pasar_al_dia_siguiente(self):
        pass

    def volver(self):
        pass

    def salir():
        pass
