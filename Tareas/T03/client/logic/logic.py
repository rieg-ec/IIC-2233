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
    start_game_signal = pyqtSignal(str, list)
    # chat signal: author, message
    chat_message_signal = pyqtSignal(str, str)
    # update current player turn signal:
    player_turn_signal = pyqtSignal(str)
    # update an opponent hand:
    opponent_card_signal = pyqtSignal(str, bool)
    # store face down sprite card:
    face_down_sprite_signal = pyqtSignal(bytearray)
    # update hand signal:
    hand_card_signal = pyqtSignal(bytearray, tuple)
    # update discard pile signal:
    discard_pile_signal = pyqtSignal(bytearray)

    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
        self.client = Client(self.parameters['host'],
            int(self.parameters['port']))
        self.client.server_message_signal.connect(self.server_message)
        self.client.server_image_signal.connect(self.server_image)

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
            # args = (player name, rest of players)
            # send already connected players so the window can show them
            self.username_valid_signal.emit(self.name, args)

        elif key == 'INVALID_USERNAME' or key == 'FULL':
            # TODO: split into 2 cases
            self.username_invalid_signal.emit()

        elif key == 'NEW_PLAYER':
            self.new_player_signal.emit(args, True) # args = player

        elif key == 'PLAYER_LEFT':
            self.new_player_signal.emit(args, False) # args = player

        elif key == 'START':
            opponents = [i for i in args if i != self.name]
            self.start_game_signal.emit(self.name, opponents)

        elif key == 'CHAT_MESSAGE':
            author, message = args
            self.chat_message_signal.emit(author, message)

        elif key == 'TURN':
            self.player_turn_signal.emit(args) # args = player

        elif key == 'OPPONENT_CARD':
            # args will be a list with opponent and whether he lost or gained a card
            # True means gained, False means lost
            self.opponent_card_signal.emit(args[0], args[1]) # args = [opponent, bool]

        elif key == 'VALID_CARD':
            # TODO: args is the card tuple
            pass

        elif key == 'PLAYER_CARD':
            # TODO: deserialize bytearray
            pass

    def server_image(self, list_):
        destination, card_tuple, sprite = list_

        if destination == '0':
            self.hand_card_signal.emit(sprite, card_tuple)
        elif destination == '1':
            self.discard_pile_signal.emit(sprite)
        elif destination == '2':
            self.face_down_sprite_signal.emit(sprite)
