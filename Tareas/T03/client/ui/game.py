from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QTextEdit, QLineEdit,
    QFrame
)
from PyQt5.QtGui import QPixmap, QTransform
from ui.utils import ColorDialog, EndGameDialog

from os import path
import sys, json

sys.path.append('..')
from client.utils import json_hook


class GameWindow(QWidget):

    with open('parameters.json', 'r') as file:
        parameters = json.loads(file.read(), object_hook=json_hook)


    class QHLine(QFrame):
        """ Horizontal line separator """
        def __init__(self):
            super().__init__()
            self.setFrameShape(QFrame.HLine)
            self.setFrameShadow(QFrame.Sunken)

    class QVLine(QFrame):
        """ Vertical line separator """
        def __init__(self):
            super().__init__()
            self.setFrameShape(QFrame.VLine)
            self.setFrameShadow(QFrame.Sunken)

    class NamedQHBoxLayout(QHBoxLayout):
        """ Has name attribute to be identified by name """
        def __init__(self, rotation):
            super().__init__()
            self.name = None
            self.cards = []
            self.rotation = rotation

        def addWidget(self, widget):
            super().addWidget(widget)
            self.cards.append(widget)

        def removeWidget(self, widget):
            super().removeWidget(widget)
            self.cards.remove(widget)
            widget.deleteLater()


    class NamedQVBoxLayout(QVBoxLayout):
        """ Has name attribute to be identified by name """
        def __init__(self, rotation):
            super().__init__()
            self.name = None
            self.cards = []
            self.rotation = rotation

        def addWidget(self, widget):
            super().addWidget(widget)
            self.cards.append(widget)

        def removeWidget(self, widget):
            super().removeWidget(widget)
            self.cards.remove(widget)
            widget.deleteLater()

    class CardLabel(QLabel):
        """ class to display cards and handle events """
        play_card_signal = pyqtSignal(int, tuple)
        draw_card_signal = pyqtSignal()
        _id = 0
        # id is used when 2 cards have same color and type to distinguish
        def __init__(self, parent, discard_pile=False,
                    opponent=False, draw=False, player=False):
            super().__init__(parent)
            self.setMaximumSize(100, 140)
            self.setMinimumSize(90, 100)
            self.discard_pile = discard_pile
            self.opponent = opponent
            self.draw = draw
            self.player = player
            self.setMinimumWidth(100)

        def mousePressEvent(self, e):
            """ sends a signal depending on which card it is """
            if self.player:
                self.play_card_signal.emit(self.id, self.card_tuple)
            elif self.draw:
                self.draw_card_signal.emit()

        def setPixmap(self, bytes, card_tuple=None):
            """ optional argument card_tuple for hand cards, stores the tuple """
            super().setPixmap(bytes)

            if card_tuple:
                # only hand cards get passed a card tuple
                self.card_tuple = card_tuple
                self.id = self._id
                GameWindow.CardLabel._id += 1

    text_signal = pyqtSignal(str)
    shout_signal = pyqtSignal()
    play_card_signal = pyqtSignal(int, tuple)
    draw_card_signal = pyqtSignal()
    back_to_login_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(*self.parameters['game_window_geometry'])

        qhbox = QHBoxLayout() # contains all other layouts
        right_side_vbox = QVBoxLayout() # contains right side layouts with
                                            # game info
        game_box_layout_center = QVBoxLayout() # contains player hbox, card pile
                                                    # and top opponent hbox
        self.hand_layouts = dict()
        self.hand_layouts['top'] = self.NamedQHBoxLayout(180) # contains top opponent cards
        self.hand_layouts['self'] = self.NamedQHBoxLayout(0) # contains player cards
        self.hand_layouts['right'] = self.NamedQVBoxLayout(270) # contains right side opponent cards
        self.hand_layouts['left'] = self.NamedQVBoxLayout(90) # contains left side opponent cards

        # ========== LEFT OPPONENTS CARDS ==========
        self.hand_layouts['left'].setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        # ==========================================

        # ========== TOP CARDS ==========
        self.hand_layouts['top'].setAlignment(Qt.AlignCenter | Qt.AlignTop)
        game_box_layout_center.addLayout(self.hand_layouts['top'], 1)
        # ===============================

        # ========== PILE CARDS ==========
        self.discard_pile = self.CardLabel(self, discard_pile=True)
        game_box_layout_center.addWidget(self.discard_pile, 1, Qt.AlignCenter)
        # ================================

        # ========== PLAYER CARDS ==========
        self.player_card_labels = [] # to store card labels
        self.hand_layouts['self'].setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        game_box_layout_center.addLayout(self.hand_layouts['self'], 1)
        # ==================================


        # ========== RIGHT OPPONENTS CARDS ==========
        self.hand_layouts['right'].setAlignment(Qt.AlignCenter | Qt.AlignRight)
        # ===========================================


        # ========== RIGHT SIDE WIDGETS =============
        self.turn_label = QLabel('', self)
        self.suit_label = QLabel('', self)
        self.draw_card_label = self.CardLabel(self, draw=True)
        self.draw_card_label.draw_card_signal.connect(
            self.draw_card_signal.emit)
        self.draw_text_label = QLabel('ROBA CARTA', self)
        shout_text = QLabel('GRITA', self)
        shout_button = QPushButton('DCCUATRO!', self)
        shout_button.clicked.connect(self.shout_signal.emit)

        self.text_output = QTextEdit(self)
        self.text_output.setReadOnly(True)
        self.text_input = QLineEdit(self)
        self.text_input.returnPressed.connect(
            self.send_message)

        right_side_vbox.addWidget(self.turn_label, 1, Qt.AlignCenter)
        right_side_vbox.addWidget(self.suit_label, 1, Qt.AlignCenter)

        right_side_vbox.addWidget(self.QHLine())

        right_side_vbox.addStretch(1)
        right_side_vbox.addWidget(self.draw_card_label, 2, Qt.AlignCenter)
        right_side_vbox.addWidget(self.draw_text_label, 2, Qt.AlignCenter)
        right_side_vbox.addStretch(1)

        right_side_vbox.addWidget(self.QHLine())

        right_side_vbox.addWidget(shout_text, 1, Qt.AlignCenter)
        right_side_vbox.addWidget(shout_button, 1)

        right_side_vbox.addWidget(self.QHLine())

        right_side_vbox.addWidget(self.text_output, 7)
        right_side_vbox.addWidget(self.text_input, 1)
        # workaround: using a container for a layout to use
        # setMaximumWidth
        container = QWidget()
        container.setLayout(right_side_vbox)
        container.setMaximumWidth(250)
        # ===========================================

        qhbox.addLayout(self.hand_layouts['left'], 1)
        qhbox.addLayout(game_box_layout_center, 1)
        qhbox.addLayout(self.hand_layouts['right'], 1)
        qhbox.addWidget(self.QVLine())
        qhbox.addWidget(container, 1)

        self.setLayout(qhbox)

    def resetUI(self):
        for layout in self.hand_layouts.values():
            for card in layout.cards.copy():
                layout.removeWidget(card)

        self.discard_pile.setPixmap(QPixmap())
        self.turn_label.setText('')
        self.suit_label.setText('')
        self.text_output.setPlainText('')


    def show(self, self_name, opponents):
        """
        assigns name of players to its corresponding layout in the interface
        based on turn order
        (1) if there's only one opponent, it gets assigned to top layout
        (2) else, opponents are assigned in a loop startin from right layout
        """
        self.hand_layouts['self'].name = self_name
        self.setWindowTitle(self_name)
        if len(opponents) == 1:
            self.hand_layouts['top'].name = opponents[0]
        else:
            layouts = ['right', 'top', 'left']
            for opponent in opponents:
                layout = layouts.pop(0)
                self.hand_layouts[layout].name = opponent

        self.resetUI()
        super().show()

    def receive_message(self, author, message):
        history = self.text_output.toPlainText()
        new = f'{author}: {message}'
        self.text_output.setPlainText(history + f'\n{new}\n')
        self.text_output.verticalScrollBar().setValue(
            self.text_output.verticalScrollBar().maximum())

    def send_message(self):
        self.text_signal.emit(self.text_input.text())
        self.text_input.setText('')

    def change_turn(self, player):
        self.turn_label.setText(f'TURNO DE: {player}')

    def draw_text(self, number):
        self.draw_text_label.setText(f'ROBA {number} CARTA(S)')

    def store_facedown_sprite(self, sprite):
        """ store face down card sprite """
        self.face_down = QPixmap()
        self.face_down.loadFromData(sprite, 'PNG')

        self.draw_card_label.setPixmap(self.face_down.scaled(
            self.draw_card_label.width(), self.draw_card_label.height()))

    def update_opponent_hand(self, opponent, bool):
        """ add/remove face down card label to an opponent hand """
        for l in self.hand_layouts.values():
            if l.name == opponent:
                layout = l
        if bool:
            # add facedown card to an opponent hand
            card = self.CardLabel(self, opponent=True)
            transform = QTransform()
            transform.rotate(layout.rotation)
            card.setPixmap(self.face_down.transformed(
                transform).scaled(card.width(), card.height()))
            layout.addWidget(card)
        else:
            card = layout.cards[0]
            layout.removeWidget(card)

    def update_player_card(self, sprite, card_tuple):
        """ add a card to player hand """
        pixmap = QPixmap()
        pixmap.loadFromData(sprite, 'PNG')
        card_label = self.CardLabel(self, player=True)
        card_label.play_card_signal.connect(self.play_card)
        card_label.setPixmap(pixmap.scaled(card_label.width(),
            card_label.height()), card_tuple)
        self.player_card_labels.append(card_label)
        self.hand_layouts['self'].addWidget(card_label)

    def remove_player_card(self, id):
        for label in self.player_card_labels:
            if label.id == id:
                self.player_card_labels.remove(label)
                self.hand_layouts['self'].removeWidget(label)

    def update_discard_pile(self, sprite, card_tuple):
        """ update the card in the discard pile """
        _, color = card_tuple
        card = QPixmap()
        card.loadFromData(sprite, 'PNG')
        self.discard_pile.setPixmap(card.scaled(
            self.discard_pile.width(), self.discard_pile.height()))
        # let players know which color is in play:
        text_colors = {
            'verde': 'green',
            'rojo': 'red',
            'azul': 'blue',
            'amarillo': 'yellow'
        }
        self.suit_label.setText('COLOR: '
            + f'<font color="{text_colors[color]}">{color.upper()}</font>')

    def play_card(self, id, card_tuple):
        self.play_card_signal.emit(id, card_tuple)

    def choose_color_popup(self, card_id):
        """ pick a color when playing a color card """
        color_popup = ColorDialog(self)
        send_color = lambda color: self.play_card_signal.emit(
            card_id, ('color', color))
        color_popup.color_signal.connect(send_color)

    def loose(self):
        for card in self.hand_layouts['self'].cards.copy():
            self.hand_layouts['self'].removeWidget(card)
        lost_label = QLabel('ESPECTADOR', self)
        self.hand_layouts['self'].addWidget(lost_label)

    def opponent_lost(self, opponent):
        """ removes all cards from looser layout, and places text instead """
        for layout in self.hand_layouts.values():
            if layout.name == opponent:
                for card in layout.cards.copy():
                    layout.removeWidget(card)

                lost_label = QLabel('ESPECTADOR', self)
                layout.addWidget(lost_label)

    def end_game(self, winner):
        end_popup = EndGameDialog(self, winner)
        end_popup.back_to_login_signal.connect(self.back_to_login_signal.emit)
        end_popup.back_to_login_signal.connect(self.close)


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    parameters = {"game_window_geometry": [100, 100, 1300, 900]}
    app = QApplication([])
    window = GameWindow(parameters)
    window.show('me', ['peter', 'maca'])
    sys.exit(app.exec_())
