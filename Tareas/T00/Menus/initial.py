from Menus.followers import FollowersMenu
from Menus.prograposts import PrograPostMenu


class InitialMenu:

    def __init__(self):
        self.logged_user = ""

    def interface(self):
        user_input = input("\nBienvenido a DCCahuin!! \n"
                        +"Seleccione una opción: \n"
                        +"[1] Iniciar sesion \n"
                        +"[2] Registrar usuario \n"
                        +"[0] Salir \n"
                        +"Indique su opcion (0, 1 o 2): ")

        if user_input == "1":
            return self.log_in()

        elif user_input == "2":
            return self.sign_up()

        elif user_input == "0":
            pass

        else:
            print("\nINGRESE UNA OPCION VALIDA")
            return self.interface()

    def select_menu(self):
        menu_input = input("\nBienvenido {}! \n".format(self.logged_user)
                            +"seleccione una opcion: \n"
                            +"[1] Menu de prograposts \n"
                            +"[2] Menu de seguidores \n"
                            +"[0] Salir \n"
                            +"Indique su opcion (0, 1 o 2): ")

        if menu_input == "1": # redirect to Progra posts menu's interface
            menu = PrograPostMenu(self.logged_user)
            menu.interface()
            return self.select_menu()

        elif menu_input == "2": # redirect to followers menu's interface
            menu = FollowersMenu(self.logged_user)
            menu.interface()
            return self.select_menu()

        elif menu_input == "0":
            pass # exit

        else:
            print("\nINGRESE UNA OPCION VALIDA")
            return self.select_menu()

    def log_in(self):
        user_input = input("\nIngrese su nombre de usuario: ")
        # do something with user_input
        if user_input:
            name = user_input

        self.logged_user = name
        self.select_menu()



    def sign_up(self):
        user_input = input("\nEscoja un nombre de usuario: ")
        # do something with user_input
        if user_input:
            # create user
            name = user_input

        self.log_in()
