import sys
from controller import Controller
from PyQt5.QtWidgets import QApplication
from utils import json_hook
import json
from ui.login import LoginWindow
from ui.room import RoomWindow
from ui.game import GameWindow
from logic.logic import Logic

if __name__ == '__main__':

    app = QApplication([])

    logic = Logic()

    login_window = LoginWindow()
    login_window.username_signal.connect(
        logic.check_username)
    # valid username signal:
    logic.username_valid_signal.connect(
        login_window.close)
    # invalid username signal:
    logic.username_invalid_signal.connect(
        login_window.invalid_username)


    room_window = RoomWindow()
    # signal emitted when username is valid in login_window
    logic.username_valid_signal.connect(
        room_window.show)
    # signal emitted when new player joins the room:
    logic.new_player_signal.connect(
        room_window.new_player)
    # signal emitted when game starts:
    logic.start_game_signal.connect(
        room_window.close)


    game_window = GameWindow()
    # connect signal to show() and close()
    logic.start_game_signal.connect(game_window.show)
    game_window.text_signal.connect(logic.send_chat_message)
    logic.chat_message_signal.connect(game_window.receive_message)
    logic.player_turn_signal.connect(game_window.change_turn)
    logic.face_down_sprite_signal.connect(
        game_window.store_facedown_sprite)
    logic.opponent_card_signal.connect(
        game_window.update_opponent_hand)
    logic.discard_pile_signal.connect(
        game_window.update_discard_pile)
    logic.hand_card_signal.connect(game_window.update_player_card)
    game_window.play_card_signal.connect(logic.play_card)
    game_window.draw_card_signal.connect(logic.draw_card)
    game_window.shout_signal.connect(logic.shout_dccuatro)
    logic.remove_hand_signal.connect(
        game_window.remove_player_card)
    logic.choose_color_signal.connect(
        game_window.choose_color_popup)
    logic.lost_signal.connect(game_window.loose)
    logic.opponent_lost_signal.connect(game_window.opponent_lost)
    logic.end_game_signal.connect(game_window.end_game)
    game_window.back_to_login_signal.connect(login_window.show)

    login_window.show()
    
    try:
        logic.connect_to_server()
        sys.exit(app.exec_())
    except ConnectionRefusedError:
        print('connection refused from server')
        sys.exit()
