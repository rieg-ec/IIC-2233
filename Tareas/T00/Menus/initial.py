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
            pass # program stops

        else:
            print("\nINGRESE UNA OPCION VALIDA")
            return self.interface()

    def select_menu(self):
        menu_input = input("\nseleccione una opcion: \n"
                            +"[1] Menu de prograposts \n"
                            +"[2] Menu de seguidores \n"
                            +"[0] Cerrar sesion \n"
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
            return self.interface() # return to log in menu (interface())

        else:
            print("\nINGRESE UNA OPCION VALIDA")
            return self.select_menu()

    def log_in(self):
        user_input = input("\nIngrese su nombre de usuario: ")
        with open("usuarios.csv", "r") as f:
            users = f.read().split("\n")
            f.close()

            if user_input in users and user_input != "":
                self.logged_user = user_input
                print("\nBienvenido {}!".format(self.logged_user))
                self.select_menu()

            else:
                print("\nUsuario no existente")
                return self.interface()


    def sign_up(self):
        user_input = input("\nEscoja un nombre de usuario: ")

        if user_input == "" \
                or user_input.isalnum() is False \
                or user_input.isdigit() is True \
                or user_input.isalpha() is True \
                or len(user_input) < 8:

            print("\nNombre de usuario no valido: \n"
                  +"El nombre de usuario debe contener al menos 1 letra, 1 numero "
                  +"y minimo 8 caracteres.")
            return self.interface()

        else:
            with open("usuarios.csv", "r+") as f:

                users = f.read().split('\n')

                if user_input in users: # username exists
                    print("\nEste usuario ya existe")
                    f.close()
                    return self.interface()


                else:
                    f.writelines(user_input)
                    f.close()
                    print("\nUsuario {} registrado".format(user_input))

                    with open('seguidores.csv', 'r+') as f: # add username to seguidores.csv also
                        users = [i.split(',', 1) for i in f.read().split('\n')]
                        if user_input not in users[::][0]:
                            f.writelines(user_input)

                    return self.log_in()
