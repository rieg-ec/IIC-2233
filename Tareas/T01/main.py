
from menus import LoginMenu, MainMenu


def main():
    login_menu = LoginMenu()
    login_menu.interfaz()
    print(f"Hasta pronto {login_menu.usuario} :)")


if __name__ == "__main__":
    main()
