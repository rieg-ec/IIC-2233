from PyQt5.QtCore import QObject, pyqtSignal
from logic.client import Client


class Logic(QObject):
    # username validation:
    username_valid_signal = pyqtSignal(str, list)
    # username not valid:
    username_invalid_signal = pyqtSignal()
    # new player joined or left room:
    new_player_signal = pyqtSignal(str, bool)
    # all players joined:
    start_game_signal = pyqtSignal()
    # chat signal: author, message
    chat_message_signal = pyqtSignal(str, str)

    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
        self.client = Client(self.parameters['host'],
            int(self.parameters['port']))
        self.client.server_message_signal.connect(self.server_message)

    def connect_to_server(self):
        self.client.connect_to_server()

    def check_username(self, name):
        message = {"CHECK_USERNAME": name}
        self.client.send(message)

    def send_chat_message(self, chat_message):
        """ Sends a chat message to the server """
        message = {"CHAT_MESSAGE": chat_message}
        self.client.send(message)

    def server_message(self, message):
        """
        This method handles the commands sent from the server
        to the client object and sends signals to the controller
        """
        key, args = *message.keys(), *message.values()
        # username validation
        if key == 'VALID_USERNAME':
            """
            username_valid_signal is connected to room_window.show()
            and login_window.close()
            """
            self.name = args.pop(0) # store our name
            self.opponents = {name: None for name in args} # store opponents
                                                        # names and number of cards
            # signal connected to window_room.show()
            # send already connected player so the window can show them
            self.username_valid_signal.emit(self.name, args)

        elif key == 'INVALID_USERNAME' or key == 'FULL':
            # TODO: split into 2 cases
            self.username_invalid_signal.emit()

        elif key == 'NEW_PLAYER':
            self.new_player_signal.emit(args, True)
            self.opponents[args] = None # store new opponent name

        elif key == 'PLAYER_LEFT':
            self.new_player_signal.emit(args, False)

        elif key == 'START':
            self.start_game_signal.emit()

        elif key == 'CHAT_MESSAGE':
            author, message = args
            self.chat_message_signal.emit(author, message)
