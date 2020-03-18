import datetime
from datetime import datetime

class PrograPostMenu:
    def __init__(self, user): # user is picked from array of objects
        self.logged_user = user

    def interface(self):
        user_input = input("\nQue accion desea realizar? \n"
                           +"[1] Publicar algo \n"
                           +"[2] Eliminar una publicacion \n"
                           +"[3] Ver mis propias publicaciones \n"
                           +"[4] Ver las publicaciones de alguien mas \n"
                           +"[5] Ver usuarios seguidos \n"
                           +"[0] Volver atras \n"
                           +"Indique su opcion (1, 2, 3, 4, 5 o 0): ")


        if user_input == "1":
            self.post()
            return self.interface()

        elif user_input == "2":
            self.delete_post()
            return self.interface()

        elif user_input == "3":
            self.see_own_posts()
            return self.interface()


        elif user_input == "4":
            self.see_user_posts()
            return self.interface()

        elif user_input == "5":
            self.see_followed_users()
            return self.interface()


        elif user_input == "0":
            pass # return to start menu without logging out


    def post(self):
        content = input("\nEscriba algo (maximo 140 caracteres): ")
        if len(content) > 140:
            print("Superaste el limite de 140 caracteres. Intentalo de nuevo.")
            return self.post()
        else:
            with open('posts.csv', 'a') as f:
                date = datetime.now().strftime("%Y/%m/%d")
                f.writelines("{},{},{}\n".format(self.logged_user, date, content))
                f.close()
                print("\nContenido publicado.")




    def delete_post(self):
        date = input("\nIngrese la fecha de la publicación que desea eliminar"
                     +" (en formato 'yy/mm/dd'): ")
        date_of_post = datetime.strptime(date, "%Y/%m/%d")

        with open('posts.csv', 'r') as f:
            posts = [i.split(',', 2) for i in f.read().split('\n') if i != ""]
            own_posts = [i for i in posts if i[0] == self.logged_user]
            f.close()

        posts_in_date = [i for i in own_posts if i[1] == date]

        if len(posts_in_date) == 0:
            print("\nNo tienes publicaciones en esa fecha.")

        elif len(posts_in_date) == 1:
            with open('posts.csv', 'w') as f:
                for i in posts:
                    if i not in posts_in_date:
                        str = "{},{},{}\n".format(i[0], i[1], i[2]) # each row of posts.csv as a str
                        f.write(str)
                f.close()
                print("\nPublicacion eliminada: '{}'".format(posts_in_date[0][2]))

        else:
            n_of_posts = len(posts_in_date)
            print("\nTienes %d publicaciones en esa fecha: " %n_of_posts)

            for i in range(n_of_posts):
                print("\n[{}]: {}".format(i+1, posts_in_date[i][2]))

            choice = input("\nCual deseas eliminar?: ")
            post_to_delete = posts_in_date[int(choice)-1]

            with open('posts.csv', 'w') as f:
                for i in posts:
                    if i != post_to_delete:
                        str = "{},{},{}\n".format(i[0], i[1], i[2]) # each row of posts.csv as a str
                        f.write(str)
                f.close()
                print("\nPublicacion eliminada: '{}'".format(post_to_delete[2]))





    def see_own_posts(self):

        with open('posts.csv', 'r') as f:
            posts = [i.split(',', 2) for i in f.read().split('\n')]

            # create array with posts from user:
            own_posts = [i for i in posts if i[0] == self.logged_user]

            # sort by date from less recent to most recent
            # if post_list is empty, nothing happens:
            own_posts = sorted(own_posts, key=lambda x: datetime.strptime(x[1], '%Y/%m/%d'))

            if len(own_posts) == 0:
                print("\n{}, no tienes publicaciones aun.".format(self.logged_user))

            elif len(own_posts) == 1:
                print("\n{}: {}".format(own_posts[0][1], own_posts[0][2]))

            else:
                # from most recent to less recent means that recent posts will output first and
                # less recent will output last, making less recent posts appear bottom
                order = input("\nEn que orden desea ver sus publicaciones? \n"
                              +"[1] desde el mas reciente al menos reciente \n"
                              +"[2] desde el menos reciente al mas reciente \n"
                              +"Ingrese su opcion (1 o 2): ")

                if order == "1":
                    print("\nPublicaciones de {}: ".format(self.logged_user))
                    for i in own_posts[::-1]:
                        print("\n{}: {}".format(i[1], i[2]))


                elif order == "2":
                    print("\nPublicaciones de {}: ".format(self.logged_user))
                    for i in own_posts:
                        print("\n{}: {}".format(i[1], i[2]))

                else:
                    print("\nEnter a valid option")
                    f.close()
                    return self.see_own_posts()

            f.close()


    def see_user_posts(self):
        user_to_stalk = input("\nDe que persona desea ver publicaciones? : ")
        if user_to_stalk != self.logged_user:
            with open("usuarios.csv", 'r') as f:
                users = f.read().split('\n')
                if user_to_stalk not in users:
                    print("\nUsuario no existente.")

                else:
                    with open('posts.csv', 'r') as f:
                        posts = [i.split(',', 2) for i in f.read().split('\n')]

                        if user_to_stalk not in [i[0] for i in posts]:
                            print("\nUsuario no tiene publicaciones.")

                        else:
                            user_to_stalk_posts = [i for i in posts if i[0] == user_to_stalk]
                            sorted_posts = sorted(user_to_stalk_posts, key=lambda x: datetime.strptime(x[1], '%Y/%m/%d'))
                            f.close()

                            if len(sorted_posts) == 1:
                                print("\n[{}]: {}".format(sorted_posts[0][1], sorted_posts[0][2]))

                            else:
                                order = input("\n{} tiene {} publicaciones. en que orden desea verlas?\n".format(user_to_stalk, len(user_to_stalk_posts))
                                      +"[1] desde el mas reciente al menos reciente \n"
                                      +"[2] desde el menos reciente al mas reciente\n"
                                      +"Indique su opcion: ")

                                if order == "1":
                                    for i in sorted_posts[::-1]:
                                        print("\n{}: {}".format(i[1], i[2]))
                                elif order == "2":
                                    for i in sorted_posts:
                                        print("\n{}: {}".format(i[1], i[2]))
                                else:
                                    print("\nEnter a valid option.")
        else:
            print("\nIngrese un nombre distinto al suyo.")



    def see_followed_users(self):
        pass
