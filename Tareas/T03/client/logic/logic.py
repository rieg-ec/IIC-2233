from PyQt5.QtCore import QObject, pyqtSignal
from logic.client import Client

import sys, json

sys.path.append('..')
from client.utils import json_hook

class Logic(QObject):

    with open('parameters.json', 'r') as file:
        parameters = json.loads(file.read(), object_hook=json_hook)


    # username validation:
    username_valid_signal = pyqtSignal(str, list)
    # username not valid:
    username_invalid_signal = pyqtSignal(str)
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
    # remove a hand card signal:
    remove_hand_signal = pyqtSignal(int)
    # update discard pile signal:
    discard_pile_signal = pyqtSignal(bytearray, tuple)
    # choose color signal:
    choose_color_signal = pyqtSignal(int)
    # signal when player looses:
    lost_signal = pyqtSignal()
    # signal when an opponent looses:
    opponent_lost_signal = pyqtSignal(str)
    # signal when game ends:
    end_game_signal = pyqtSignal(str) # winner as argument

    def __init__(self):
        super().__init__()
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

    def play_card(self, id, card_tuple):
        message = {"PLAY_CARD": [id, card_tuple]}
        self.client.send(message)

    def draw_card(self):
        message = {"DRAW_CARD": None}
        self.client.send(message)

    def shout_dccuatro(self):
        message = {"SHOUT_DCCUATRO": None}
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

        elif key == 'FULL':
            self.username_invalid_signal.emit('GAME IS FULL')

        elif key == 'INVALID_USERNAME':
            self.username_invalid_signal.emit('INVALID USERNAME')

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

        elif key == 'PLAYER_CARD':
            # sent to remove card from hand
            self.remove_hand_signal.emit(args) # card id

        elif key == 'CHOOSE_COLOR':
            card_id = args
            self.choose_color_signal.emit(card_id)

        elif key == 'LOST':
            self.lost_signal.emit()

        elif key == 'OPPONENT_LOST':
            self.opponent_lost_signal.emit(args)

        elif key == 'END':
            self.end_game_signal.emit(args)

    def server_image(self, list_):
        destination, card_tuple, sprite = list_

        if destination == '0':
            self.hand_card_signal.emit(sprite, card_tuple)
        elif destination == '1':
            self.discard_pile_signal.emit(sprite, card_tuple)
        elif destination == '2':
            self.face_down_sprite_signal.emit(sprite)
