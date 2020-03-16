class FollowersMenu:
    def __init__(self, user):
        self.logged_user = user

    def interface(self):
        user_input = input("Qué acción desea realizar?")

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
