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
                date = datetime.datetime.now().strftime("%Y/%m/%d")
                f.writelines("{},{},{}\n".format(self.logged_user, date, content))
                f.close()
                print("\nContenido publicado.")




    def delete_post(self):
        date = input("\nIngrese la fecha de la publicación que desea eliminar"
                     +" (en formato 'yy/mm/dd'): ")
        date_of_post = parse(date).strftime("%Y/%m/%d")

        with open('posts.csv', 'r') as f:
            posts = [i.split(',', 2) for i in f.readlines().split('\n')]
            f.close()



    def see_own_posts(self):

        with open('posts.csv', 'r') as f:
            posts = [i.split(',', 2) for i in f.read().split('\n')]

            # create array with posts from user:
            posts_list = [i for i in posts if i[0] == self.logged_user]

            # sort by date from less recent to most recent
            # if post_list is empty, nothing happens:
            posts_list = sorted(posts_list, key=lambda x: datetime.strptime(x[1], '%Y/%m/%d'))

            if len(posts_list) == 0:
                print("{}, no tienes publicaciones aun.".format(self.logged_user))

            else:
                # from most recent to less recent means that recent posts will output first and
                # less recent will output last, making less recent posts appear bottom
                order = input("\nEn que orden desea ver sus publicaciones? \n"
                              +"[1] desde el mas reciente al menos reciente \n"
                              +"[2] desde el menos reciente al mas reciente \n"
                              +"Ingrese su opcion (1 o 2): ")

                if order == "1":
                    print("\nPublicaciones de {}: ".format(self.logged_user))
                    for i in posts_list[::-1]:
                        print("{}: {}".format(i[1], i[2]))


                elif order == "2":
                    print("\nPublicaciones de {}: ".format(self.logged_user))
                    for i in posts_list:
                        print("{}: {}".format(i[1], i[2]))

                else:
                    print("\nEnter a valid option")
                    f.close()
                    return self.see_own_posts()

            f.close()


    def see_user_posts(self):
        pass

    def see_followed_users(self):
        pass
