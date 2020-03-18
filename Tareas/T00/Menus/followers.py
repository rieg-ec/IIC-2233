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

        elif user_to_follow == self.logged_user:
            print("\nNo puedes seguirte a ti mismo.")

        else:
            with open('seguidores.csv', 'r+') as f:
                user_followers = [i.split(',', 1) for i in f.read().split('\n')] #[[user, followers]] if following someone
                followers_list = [i[1].split(',') for i in user_followers if i[0] == self.logged_user and len(i) > 1 and i[1] != ""]
                f.close()

            if len(followers_list) > 0 and user_to_follow in followers_list[0]:
                print("\nYa sigue a este usuario")

            else:
                if len(followers_list) > 0:
                    followers_list[0].append(user_to_follow)
                else:
                    followers_list.append([user_to_follow])

                with open('seguidores.csv', 'w') as f:
                    for i in user_followers:

                        if i[0] != self.logged_user:
                            if len(i) > 1 and i[1] != "": # i[1] is users followed and not something else than can cause bugs
                                str = "{},{}\n".format(i[0], i[1])
                                f.write(str)

                            else:
                                f.write(i[0] + '\n') # i[1] doesn't exists or isn't important

                        else:
                            str = "{},{}\n".format(self.logged_user, ",".join(i for i in followers_list[0]))
                            f.write(str)

                    f.close()


    def unfollow(self):
        user_to_unfollow = input("\nA quien desea dejar de seguir? : ")
        with open('usuarios.csv', 'r') as f:
            users = [i for i in f.read().split('\n')]
            f.close()

        if user_to_unfollow not in users:
            print("\nUsuario no existente.")

        elif user_to_unfollow == self.logged_user:
            print("\nNo puedes dejar de seguirte a ti mismo.")

        else:
            with open('seguidores.csv', 'r+') as f:
                user_followers = [i.split(',', 1) for i in f.read().split('\n')] #[[user, followers]] if following someone
                followers_list = [i[1].split(',') for i in user_followers if i[0] == self.logged_user and len(i) > 1 and i[1] != ""]
                f.close()

            if len(followers_list) == 0 or user_to_unfollow not in followers_list[0]:
                print("\nNo sigue a este usuario")

            else:

                followers_list[0].remove(user_to_unfollow) # it may result in empty list

                with open('seguidores.csv', 'w') as f:
                    for i in user_followers:
                        if i[0] != self.logged_user:
                            if len(i) > 1 and i[1] != "":
                                str = "{},{}\n".format(i[0], i[1])
                                f.write(str)
                            else:
                                f.write(i[0] + '\n')
                        else:
                            if len(followers_list[0]) > 0:
                                str = "{},{}".format(self.logged_user, ",".join(i for i in followers_list[0]))
                                f.write(str)
                            else:
                                f.write(self.logged_user + '\n')

                    f.close()
