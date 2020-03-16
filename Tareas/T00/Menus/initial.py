from Menus.followers import FollowersMenu
from Menus.prograposts import PrograPostMenu


class InitialMenu:
    def interface(self):
        user_input = input("Log in (1) or sign up (2)?")
        if user_input == "1":
            return self.log_in()
        elif user_input == "2":
            return self.sign_up()


    def log_in(self):
        user_input = input("Ingrese su nombre de usuario: ")
        # do something with user_input

        menu_input = input("Indique su opcion (0, 1 o 2)")

        if menu_input == "1":
            menu = FollowersMenu("Ramon")
            return menu.interface()

        elif menu_input == "2":
            menu = PrograPostMenu("Ramon")
            return menu.interface()

        elif menu_input == "0":
            pass # salir

    def sign_up(self):
        user_input = input("Escoja un nombre de usuario: ")
        # do something with user_input


        menu_input = input("Indique su opcion (0, 1 o 2)")

        if menu_input == "1":
            menu = FollowersMenu("Ramon")
            return menu.interface()

        elif menu_input == "2":
            menu = PrograPostMenu("Ramon")
            return menu.interface()

        elif menu_input == "0":
            pass # salir
