from PyQt5.QtCore import pyqtSignal
from ui.login import LoginWindow
from ui.room import RoomWindow
from ui.game import GameWindow
from logic.logic import Logic

class Controller:
    """
    Class responsible for managing communications between the ui's and
    the backend as well as connecting the signals
    """
    def __init__(self, parameters):
        self.parameters = parameters
        self.logic = Logic(self.parameters)
        self.connect_login()
        self.connect_room()
        self.connect_game()
        self.login_window.show()

    def connect_login(self):
        self.login_window = LoginWindow(self.parameters)
        self.login_window.username_signal.connect(
            self.logic.check_username)
        # valid username signal:
        self.logic.username_valid_signal.connect(
            self.login_window.close)
        # invalid username signal:
        self.logic.username_invalid_signal.connect(
            self.login_window.invalid_username)

    def connect_room(self):
        self.room_window = RoomWindow(self.parameters)
        # signal emitted when username is valid in login_window
        self.logic.username_valid_signal.connect(
            self.room_window.show)
        # signal emitted when new player joins the room:
        self.logic.new_player_signal.connect(
            self.room_window.new_player)
        # signal emitted when game starts:
        self.logic.start_game_signal.connect(
            self.room_window.close)

    def connect_game(self):
        self.game_window = GameWindow(self.parameters)
        # connect signal to show() and close()
        self.logic.start_game_signal.connect(
            self.game_window.show)
        self.game_window.text_signal.connect(
            self.logic.send_chat_message)
        self.logic.chat_message_signal.connect(
            self.game_window.receive_message)
        self.logic.player_turn_signal.connect(
            self.game_window.change_turn)
        self.logic.face_down_sprite_signal.connect(
            self.game_window.store_facedown_sprite)
        self.logic.opponent_card_signal.connect(
            self.game_window.update_opponent_hand)
        self.logic.discard_pile_signal.connect(
            self.game_window.update_discard_pile)
        self.logic.hand_card_signal.connect(
            self.game_window.update_player_card)
