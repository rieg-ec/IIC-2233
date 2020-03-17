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
        user_to_follow = input("A quien desea seguir? : ")
        pass

    def unfollow(self):
        user_to_unfollow = input("A quien desea dejar de seguir? : ")
        pass
