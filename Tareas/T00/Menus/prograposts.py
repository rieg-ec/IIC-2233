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
                           +"[4] Ver mi muro \n"
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
            self.display_wall()
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
            f.close()

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
                return self.see_own_posts()


    def display_wall(self):
        with open('seguidores.csv', 'r') as f:
            user_followers = [i.split(',', 1) for i in f.read().split('\n')] # [[user, followers], ...]
            followers = [i[1].split(',') for i in user_followers if i[0] == self.logged_user]
            f.close()

        if len(followers) == 0:
            print("\nAun no sigues a nadie.")

        else:
            with open('posts.csv', 'r') as f:
                user_date_posts = [i.split(',', 2) for i in f.read().split('\n')] # [[user, date, posts], ...]
                wall = [i for i in user_date_posts if i[0] in followers[0]]
                f.close()

            wall_sorted = sorted(wall, key=lambda x: datetime.strptime(x[1], '%Y/%m/%d'))
            print(wall_sorted)

            if len(wall_sorted) == 0:
                print("\nTus amigos aun no publican nada.")

            else:
                order = input("\nEn que orden desea ver las publicaciones? \n"
                              +"[1] desde el mas reciente al menos reciente \n"
                              +"[2] desde el menos reciente al mas reciente \n"
                              +"Ingrese su opcion (1 o 2): ")

                if order == "1":
                    for i in wall_sorted[::-1]:
                        print("\n{}, {}: {}".format(i[1], i[0], i[2]))


                elif order == "2":
                    for i in wall_sorted:
                        print("\n{}, {}: {}".format(i[1], i[0], i[2]))
                else:
                    print("\nEnter a valid option")
                    return self.display_wall()
