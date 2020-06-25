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
            player = args.pop(0)
            # signal connected to window_room.show()
            # send already connected player so the window can show them
            self.username_valid_signal.emit(player, args)

        elif key == 'INVALID_USERNAME' or key == 'FULL':
            # TODO: split into 2 cases
            self.username_invalid_signal.emit()

        elif 'NEW_PLAYER' in message:
            self.new_player_signal.emit(args, True)
        elif 'PLAYER_LEFT' in message:
            self.new_player_signal.emit(args, False)

        elif 'START' in message:
            self.start_game_signal.emit()
