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
            return self.follow()

        elif user_input == "2":
            return self.unfollow()

    def follow(self):
        print("function: follow")
        pass

    def unfollow(self):
        print("function: follow")
        pass
