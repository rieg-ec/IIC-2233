

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
        date = "14-07-2000"
        content = "Goood morning"

    def delete_post(self):
        pass

    def see_own_posts(self):
        pass

    def see_user_posts(self):
        pass

    def see_followed_users(self):
        pass
