class FollowersMenu:
    def __init__(self, user):
        self.logged_user = user

    def interface(self):
        user_input = input("\nQue accion desea realizar? \n"
                           +"[1] Seguir a alguien \n"
                           +"[2] Dejar de seguir a alguien \n"
                           +"[0] Volver atras \n"
                           +"Indique su opcion (1, 2, o 0): ")

        if user_input == "1":
            self.follow()
            return self.interface()

        elif user_input == "2":
            self.unfollow()
            return self.interface()

        elif user_input == "0":
            pass # exit

        else:
            print("\nINGRESE UNA OPCION VALIDA")
            return self.interface()


    def follow(self):

        user_to_follow = input("\nA quien desea seguir? : ")
        with open('usuarios.csv', 'r') as f:
            users = [i for i in f.read().split('\n')]
            f.close()

        if user_to_follow not in users:
            print("\nUsuario no existente.")

        else:
            with open('seguidores.csv', 'r+') as f:
                user_followers = [i.split(',', 1) for i in f.read().split('\n')] #[[user, followers]]
                followers_list = [i[1] for i in user_followers if i[0] == self.logged_user]
                f.close()

            if user_to_follow in followers_list:
                print("\nYa sigue a este usuario")
            else:
                followers_list.append(user_to_follow)

                with open('seguidores.csv', 'w') as f:
                    for i in user_followers:
                        user = i[0]
                        if user != self.logged_user:
                            followers = i[1]
                        else:
                            followers = followers_list
                        str = [user, followers]
                        print(str)
                    f.close()




    def unfollow(self):
        user_to_unfollow = input("A quien desea dejar de seguir? : ")
