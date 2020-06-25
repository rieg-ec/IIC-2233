from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QTextEdit, QLineEdit,
    QFrame
)
from PyQt5.QtGui import QPixmap
from os import path


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

class GameWindow(QWidget):

    text_signal = pyqtSignal(str)
    yell_signal = pyqtSignal()

    def __init__(self, parameters):
        super().__init__()
        self.parameters = parameters
        self.initUI()

    def initUI(self):
        self.setGeometry(*self.parameters['game_window_geometry'])

        qhbox = QHBoxLayout() # contains all other layouts
        right_side_vbox = QVBoxLayout() # contains right side layouts with
                                            # game info
        game_box_layout_left = QVBoxLayout() # contains left side opponent cards
        game_box_layout_center = QVBoxLayout() # contains player hbox, card pile
                                                    # and top opponent hbox
        game_box_layout_right = QVBoxLayout() # contains right side opponent cards

        player_cards_hbox = QHBoxLayout() # contains player cards
        top_opponent_cards_hbox = QHBoxLayout() # contains top opponent cards

        # ========== LEFT OPPONENTS CARDS ==========
        self.test_widget_1 = QLabel('LEFT', self)
        self.test_widget_1.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        game_box_layout_left.addWidget(self.test_widget_1)
        game_box_layout_left.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        # ==========================================

        # ========== CENTER  WIDGETS ==========
        self.test_widget_2 = QLabel('TOP', self)
        self.test_widget_3 = QLabel('CENTER', self)
        self.test_widget_4 = QLabel('PLAYER', self)
        self.test_widget_2.setAlignment(Qt.AlignCenter | Qt.AlignTop )
        top_opponent_cards_hbox.setAlignment(Qt.AlignCenter | Qt.AlignTop )
        self.test_widget_3.setAlignment(Qt.AlignCenter)
        self.test_widget_4.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        player_cards_hbox.setAlignment(Qt.AlignCenter | Qt.AlignBottom)
        top_opponent_cards_hbox.addWidget(self.test_widget_2)
        player_cards_hbox.addWidget(self.test_widget_4)
        game_box_layout_center.addLayout(top_opponent_cards_hbox)
        game_box_layout_center.addWidget(self.test_widget_3)
        game_box_layout_center.addLayout(player_cards_hbox)
        # =====================================


        # ========== RIGHT OPPONENTS CARDS ==========
        self.test_widget_5 = QLabel('RIGHT', self)
        self.test_widget_5.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        game_box_layout_right.addWidget(self.test_widget_5)
        # ===========================================


        # ========== RIGHT SIDE WIDGETS =============
        container = QWidget()
        self.turn_label = QLabel('', self)
        self.suit_label = QLabel('', self)

        self.draw_card_label = QLabel(self)
        self.draw_text_label = QLabel('', self)

        yell_text = QLabel('GRITA', self)
        yell_text.setAlignment(Qt.AlignCenter)
        yell_button = QPushButton('DCCUATRO!', self)
        yell_button.clicked.connect(self.yell_signal.emit)

        self.text_output = QTextEdit(self)
        self.text_output.setReadOnly(True)
        self.text_input = QLineEdit(self)
        self.text_input.returnPressed.connect(
            self.text_message)

        right_side_vbox.addWidget(self.turn_label)
        right_side_vbox.addWidget(self.suit_label)

        right_side_vbox.addStretch(0.1)
        right_side_vbox.addWidget(QHLine())
        right_side_vbox.addStretch(0.1)

        right_side_vbox.addWidget(self.draw_card_label)
        right_side_vbox.addWidget(self.draw_text_label)

        right_side_vbox.addStretch(0.1)
        right_side_vbox.addWidget(QHLine())
        right_side_vbox.addStretch(0.1)

        right_side_vbox.addWidget(yell_text)
        right_side_vbox.addWidget(yell_button)

        right_side_vbox.addStretch(0.1)
        right_side_vbox.addWidget(QHLine())
        right_side_vbox.addStretch(0.1)

        right_side_vbox.addWidget(self.text_output)
        right_side_vbox.addWidget(self.text_input)
        # workaround: using a container for a layout to use
        # setMaximumWidth
        container.setLayout(right_side_vbox)
        container.setMaximumWidth(200)
        # ===========================================

        qhbox.addLayout(game_box_layout_left, 1)
        qhbox.addLayout(game_box_layout_center, 1)
        qhbox.addLayout(game_box_layout_right, 1)
        qhbox.addWidget(QVLine())
        qhbox.addWidget(container, 1)

        self.setLayout(qhbox)

    def assign_names(self, names):
        self.name = names.pop(0)

    def text_message(self):
        # TODO: research if lambdas can be pointers tu functions with
        # arguments without calling the argument itself when you pass the lambda
        # as argument like method.connect(lambda) and lambda = some_function(with_args)
        # if possible, make this method a lambda and all others 1 liners also
        self.text_signal.emit(self.text_input.text())
        self.text_input.setText('')

    def change_turn(self, player):
        self.turn_label.setText(f'TURNO DE: {player}')

    def change_color_suit(self, color):
        self.suit_label.setText(f'COLOR: {color}')

    def draw_text(self, number):
        self.draw_text_label.setText(f'ROBA {number} CARTA(S)')

    # TODO: pop up window when playing color change cards to pick color


if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    import sys
    parameters = {"game_window_geometry": [100, 100, 1100, 900]}
    app = QApplication([])
    window = GameWindow(parameters)
    window.show()
    sys.exit(app.exec_())
