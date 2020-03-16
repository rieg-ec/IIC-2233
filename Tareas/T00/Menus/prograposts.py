class PrograPostMenu:
    def __init__(self, user): # user is picked from array of objects
        self.logged_user = user

    def interface(self):
        user_input = input("Qué acción desea realizar?")

        if user_input == "1":
            return self.post()

        elif user_input == "2":
            return self.delete_post()

        elif user_input == "3":
            return self.see_own_posts()

        elif user_input == "4":
            return self.see_user_posts()

        elif user_input == "5":
            return self.see_followed_users()


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
