from generador_de_mazos import sacar_cartas as generate_deck
from os import path
from random import shuffle, choice
from utils import json_hook
import json

class GameEngine:

    class Player:
        def __init__(self, name):
            self.name = name
            self.cards = []
            self.shouted = False
            self.end_turn()

        def end_turn(self):
            self.must_pass = False # can only draw or play +2
            self.must_draw = False # can only draw
            if len(self.cards) > 1:
                self.shouted = False

    with open('parameters.json', 'r') as file:
        parameters = json.loads(file.read(), object_hook=json_hook)

    def __init__(self, players):
        shuffle(players)
        self.players = [self.Player(name) for name in players]
        self.game_active = False

    @property
    def turn(self):
        return self.__turn

    @turn.setter
    def turn(self, value):
        self.__turn = value
        if self.__turn > len(self.players) - 1:
            self.__turn = 0
        elif self.__turn < 0:
            self.__turn = len(self.players) - 1

    def start(self):
        """
        (1) first turn is player in 0 index of self.players
        (2) each player is assigned with parameters['initial_hand']
            initial cards from the generated deck
        (3) from the remaining cards, we pick a valid initial card
            to be the discard pile top card
        (4) remaining deck is the draw pile
        """
        self.turn = 0
        self.direction = 1 # to the right
        self.deck = generate_deck(self.parameters['deck_size'])
        for player in self.players:
            for _ in range(self.parameters['initial_hand']):
                card_tuple = self.deck.pop(0)
                player.cards.append(card_tuple)

        self.discard_pile = self.deck.pop(0)
        while self.discard_pile[0] in ['color', '+2', 'sentido']:
            self.discard_pile = self.deck.pop(0)

        self.accumulated_draw = 0
        self.game_active = True

    def valid_turn(self, player):
        if player == self.players[self.turn].name:
            return True
        return False

    def valid_card(self, card_tuple, player):
        """
        returns True if the player can play the card
        """
        if self.valid_turn(player):
            if not card_tuple[0] == '+2':
                if self.players[self.turn].must_pass:
                    return False

            if card_tuple[0] == '+2' and self.players[self.turn].must_draw:
                # has already started drawing, cannot play anything
                return False

            if card_tuple[0] == self.discard_pile[0] or card_tuple[0] == 'color':
                # same type of card or special color card
                return True
            elif card_tuple[1] == self.discard_pile[1]:
                # same color of card
                return True
        return False

    def play_card(self, card_tuple, player):
        # minimum conditions:
        if self.valid_card(card_tuple, player):
            if card_tuple[0] == '+2' and not self.players[self.turn].must_draw:
                # * if must_draw is set to True, it means the player has
                # already draw 1 card and cannot play a card
                self.deck.append(self.discard_pile)
                self.discard_pile = card_tuple
                self.players[self.turn].cards.remove(card_tuple)

                if not self.players[self.turn].cards:
                    self.game_active = False
                    self.winner = player

                self.accumulated_draw += 2
                self.players[self.turn].end_turn()
                self.turn += self.direction
                # next player should draw and pass or play +2
                self.players[self.turn].must_pass = True
                return True

            elif not self.players[self.turn].must_pass:
                self.deck.append(self.discard_pile)
                self.discard_pile = card_tuple
                if card_tuple[0] == 'sentido':
                    self.direction *= -1
                elif card_tuple[0] == 'color':
                    # since after playing a color change card the user changes
                    # its color, remove(card) throws valueError, the fix is
                    # to just remove a random color card from his hand since
                    # what the color parameter of the card is doesn't matter
                    # as the user will change it anyway
                    color_cards = [i for i in self.players[self.turn].cards
                                    if i[0] == 'color']
                    color_card = color_cards.pop(0)
                    self.players[self.turn].cards.remove(color_card)
                    if not self.players[self.turn].cards:
                        self.game_active = False
                        self.winner = player
                    self.players[self.turn].end_turn()
                    self.turn += self.direction
                    return True
                self.players[self.turn].cards.remove(card_tuple)
                if not self.players[self.turn].cards:
                    self.game_active = False
                    self.winner = player

                self.players[self.turn].end_turn()
                self.turn += self.direction
                return True

        return False

    def draw_card(self, player):
        """
        Implements validations for all posible cases, which in a case being
        valid then calls the draw function which asssumes the drawing
        is valid
        """
        if self.valid_turn(player):
            if self.accumulated_draw > 0:
                # if accumulated_draw != 0 means last card was +2,
                # in which case if player starts drawing he cannot play +2 again:
                self.players[self.turn].must_draw = True
                card_tuple = self.draw(player)
                self.accumulated_draw -= 1

                if not self.is_playing(player):
                    # player lost when drawing, accumulated_draw must reset to 0
                    self.accumulated_draw = 0
                    return card_tuple

                if self.accumulated_draw == 0:
                    self.players[self.turn].end_turn()
                    self.turn += self.direction

                return card_tuple

            else:
                # player is drawing for the first time in its turn, therefore
                # must draw 1 and pass
                card_tuple = self.draw(player)
                if self.is_playing(player):
                    self.players[self.turn].end_turn()
                    self.turn += self.direction

                return card_tuple

        return False

    def draw(self, player_name):
        """
        Assuming the draw is valid, draws a card and checks if
        player looses in which case it is removed from self.players
        """
        card_tuple = self.deck.pop(0)
        for p in self.players:
            if p.name == player_name:
                player = p

        player.cards.append(card_tuple)
        if len(player.cards) >\
                self.parameters['card_limit']:
            self.players.remove(player)
            # if turn direction is to the left, turn index currently
            # returns the player on the right, fix is to substract 1
            if len(self.players) == 1:
                self.game_active = False
                self.winner = self.players[0].name

            elif self.direction == -1:
                self.turn -= 1
        return card_tuple

    def shout_dccuatro(self, player_name):
        """
        possible cases:
        player A has 1 card and shouts DCCuatro:
                (1) set playerA.shouted to True
        player A has > 1 cards and shouts DCCuatro:
                if no one has 1 card:
                    (2) PlayerA draws 4 cards
                if player B has 1 card:
                    if player B already shouted:
                        (3) player A draws 4 cards
                    else:
                        (4) player B draws 4 cards
        This method validates shouting DCCuatro and returns False if no one
        has to draw otherwise returns (player name, drawed cards)
        """
        names = [i.name for i in self.players]
        if player_name in names:
            # inactive players cannot use this mechanic
            for p in self.players:
                if p.name == player_name:
                    player = p

            if len(player.cards) == 1:
                if not player.shouted:
                    player.shouted = True # case (1)
                    return False, False # no one drawed anything

            must_draw = True

            for opponent in [i for i in self.players
                if i.name != player_name]:
                if len(opponent.cards) == 1 and not opponent.shouted:  # case (4)
                    drawed_cards = []
                    for _ in range(self.parameters['penalty']):
                        if self.is_playing(opponent.name):
                            drawed_card = self.draw(opponent.name)
                            drawed_cards.append(drawed_card)
                    return opponent.name, drawed_cards

            if must_draw: # case (2) and (3)
                drawed_cards = []
                for _ in range(self.parameters['penalty']):
                    if self.is_playing(player_name):
                        drawed_card = self.draw(player_name)
                        drawed_cards.append(drawed_card)
                    else:
                        self.turn += self.direction
                        self.accumulated_draw = 0
                        return player_name, drawed_cards
                # if player wrong shouted in his turn, must pass:
                if player == self.players[self.turn]:
                    self.accumulated_draw = 0
                    self.turn += self.direction
                return player_name, drawed_cards

        return False, False

    def is_playing(self, player):
        if player in [i.name for i in self.players]:
            return True
        return False
