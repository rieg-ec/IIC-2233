from generador_de_mazos import sacar_cartas as generate_deck
from os import path
from random import shuffle, choice
from utils import json_hook
import json

# TODO: try to improve play_card method to be more readable and efficient



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
        if self.__turn > len(self.players):
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
                card = self.deck.pop(0)
                # TODO: draw regular cards until ther is 1 regular left
                player.cards.append(card)

        self.discard_pile = choice([i for i in self.deck if i[0]
                        not in ('color', '+2', 'sentido')])
        self.accumulated_draw = 0
        self.game_active = True

    def valid_turn(self, player):
        if player == self.players[self.turn].name:
            return True
        return False

    def valid_card(self, card, player):
        """
        Checking just the card is not enough as sometimes the card itself is
        valid but the player cannot play it even if valid_turn returns True,
        e.g. when last player played a +2 card and current player wants to
        play something else than +2
        """
        if self.valid_turn(player):
            if not card[0] == '+2':
                if self.players[self.turn].must_draw:
                    return False
            if card[0] == self.discard_pile[0] or card[0] == 'color':
                # same type of card or special color card
                return True
            elif card[1] == self.discard_pile[1]:
                # same color of card
                return True
        return False

    def play_card(self, card, player):
        # minimum conditions:
        if self.valid_card(card, player):
            if card[0] == '+2' and not self.players[self.turn].must_draw:
                # * if must_draw is set to True, it means the player has
                # already draw 1 card and cannot play a card
                self.deck.append(self.discard_pile)
                self.discard_pile = card
                self.players[self.turn].cards.remove(card)

                if not self.players[self.turn].cards:
                    self.game_active = False

                self.accumulated_draw += 2
                self.players[self.turn].end_turn()
                self.turn += self.direction
                # next player should draw and pass or play +2
                self.players[self.turn].must_pass = True
                return True

            elif not self.players[self.turn].must_pass:
                self.deck.append(self.discard_pile)
                self.discard_pile = card
                if card[0] == 'sentido':
                    self.direction *= -1
                elif card[0] == 'color':
                    # since after playing a color change card the user changes
                    # its color, remove(card) throws valueError, the fix is
                    # to just remove a random color card from his hand since
                    # what the color parameter of the card is doesn't matter
                    # as the user will change it anyway
                    color_cards = [i for i in self.players[self.turn].cards
                                    if i[0] == 'color']
                    color_card = choice(color_cards)
                    self.players[self.turn].cards.remove(color_card)
                    if not self.players[self.turn].cards:
                        self.game_active = False
                    self.players[self.turn].end_turn()
                    self.turn += self.direction
                    return True
                self.players[self.turn].cards.remove(card)
                if not self.players[self.turn].cards:
                    self.game_active = False
                self.players[self.turn].end_turn()
                self.turn += self.direction
                return True

        return False

    def draw(self, player):
        """
        Implements validations for all posible cases, which in a case being
        valid then calls the draw_card function which asssumes the drawing
        is valid
        """
        if self.valid_turn(player):
            if self.accumulated_draw:
                # if accumulated_draw != 0 means last card was +2,
                # in which case if player starts drawing he cannot play +2 again:
                self.players[self.turn].must_draw = True
                card = self.draw_card(player)
                self.accumulated_draw -= 1
                if not self.is_playing(player):
                    # player lost, accumulated_draw must reset to 0
                    self.accumulated_draw = 0
                    return card
                if self.accumulated_draw == 0:
                    self.players[self.turn].end_turn()
                    self.turn += self.direction
                return card

            else:
                # player is drawing for the first time in its turn, therefore
                # must draw 1 and pass
                card = self.draw_card(player)
                if self.is_playing(player):
                    self.players[self.turn].end_turn()
                    self.turn += self.direction
                return card

        return False

    def draw_card(self, player):
        """
        Assuming the draw is valid, draws a card and checks if
        player looses in which case it is removed from self.players
        """
        card = self.deck.pop(0)
        self.players[self.turn].cards.append(card)
        if len(self.players[self.turn].cards) >\
                self.parameters['card_limit']:
            del self.players[self.turn]
            # if turn direction is to the left, turn index currently
            # returns the player on the right, fix is to substract 1
            if len(self.players) == 1:
                self.game_active = False
            elif self.direction == -1:
                self.turn -= 1
        return card

    def shout_dccuatro(self, player):
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
        if player in self.players: # inactive players cannot use this mechanic
            player_idx = self.players.index(player)
            if len(self.players[player_idx].cards) == 1:
                if not self.players[player_idx].shouted:
                    self.players[player_idx].shouted = True # case (1)
                    return False # no one drawed anything

            must_draw = True
            for opponent in [i for i in self.players
                if i.name != player]:
                if len(opponent.cards) == 1 and not opponent.shouted:
                    must_draw = False
                    drawed_cards = [self.deck.pop(0) for _
                        in range(self.parameters['penalty'])]
                    opponent.cards.extend(drawed_cards)
                    return opponent, drawed_cards # case (4)
            if must_draw:
                drawed_cards = [self.deck.pop(0) for _
                    in range(self.parameters['penalty'])]
                self.players[player_idx].cards.extend(drawed_cards)
                return self.players[player_idx], drawed_cards

        return False

    def is_playing(self, player):
        if player in self.players:
            return True
        return False
