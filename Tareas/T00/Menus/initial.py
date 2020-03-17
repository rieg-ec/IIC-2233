from Menus.followers import FollowersMenu
from Menus.prograposts import PrograPostMenu


class InitialMenu:
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

    def select_menu(self, name):
        menu_input = input("\nBienvenido {}! \n".format(name)
                            +"seleccione una opcion: \n"
                            +"[1] Menu de prograposts \n"
                            +"[2] Menu de seguidores \n"
                            +"[0] Salir \n"
                            +"Indique su opcion (0, 1 o 2): ")

        if menu_input == "1":
            menu = PrograPostMenu(name)
            return menu.interface()

        elif menu_input == "2":
            menu = FollowersMenu(name)
            return menu.interface()

        elif menu_input == "0":
            pass # salir

    def log_in(self):
        user_input = input("\nIngrese su nombre de usuario: ")
        # do something with user_input
        if user_input:
            name = user_input

        self.select_menu(name)



    def sign_up(self):
        user_input = input("\nEscoja un nombre de usuario: ")
        # do something with user_input
        if user_input:
            name = user_input

        self.select_menu(name)
