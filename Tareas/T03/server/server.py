import threading
import socket
import json
from utils import json_hook
from game_engine import GameEngine
from os import path

class Server:

    with open('parameters.json', 'r') as file:
        parameters = json.loads(file.read(), object_hook=json_hook)

    def __init__(self, host, port):
        print('Starting server')
        self.host = host
        self.port = port
        self.socket_server = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.lock = threading.RLock() # RLock for recursive methods
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        self.accept_connections()
        self.players = dict() # validated users
        # =========== LOG ===========
        sep = ' ' * 6
        print(f'author{sep}|{sep}action{sep}|{sep}args')

    def accept_connections(self):
        thread = threading.Thread(target=self.accept_connections_thread)
        thread.start()

    def accept_connections_thread(self):
        """
        Threading method listening for connections
        """
        accept_connections = True
        while True:
            client_socket, _ = self.socket_server.accept()
            thread = threading.Thread(
                target=self.listen_client_thread,
                args=(client_socket, ),
                daemon=True)
            thread.start()

    def listen_client_thread(self, client_socket):
        """
        One thread per client constantly listening.
        message will always be a json with the key 'command'
        """
        try:
            while True:
                # first 5 bytes are response length
                request_bytes_length = client_socket.recv(4)
                request_length = int.from_bytes(
                    request_bytes_length, byteorder='big')
                request = bytearray()
                # the rest of bytes are the response in json
                while len(request) < request_length:
                    read_length = min(4096, request_length - len(request))
                    request.extend(client_socket.recv(read_length))

                if request != b'':
                    data = request.decode('utf-8')
                    # ================ LOG ================
                    client = 'client'
                    if client_socket in self.players:
                        client = self.players[client_socket]
                    print('{:<15s} {:^15s} {:>15s}'.format(
                        client, 'send', data))
                    # ================ END ================
                    self.process_request(data, client_socket)
                else:
                    break

        except (ConnectionError, BrokenPipeError):
            # ============== LOG ==============
            print('{:<15s} {:^15s} {:>15s}'.format(
                'server', 'send ', 'error'))
            # ============== LOG ==============

        finally:
            with self.lock: # acquire a lock to read/write to self.players
                if client_socket in self.players:
                    user = self.players[client_socket]
                    msg_to_all = {"PLAYER_LEFT": user}
                    del self.players[client_socket]
                    self.send_to_all(msg_to_all)
                client_socket.close()

    def process_request(self, request, client_socket):
        dict_request = json.loads(request)
        key, args = *dict_request.keys(), *dict_request.values()
        with self.lock:
            if key == 'CHECK_USERNAME':
                self.check_username(client_socket, args)

            elif key == 'CHAT_MESSAGE':
                if client_socket in self.players:
                    response = {
                        "CHAT_MESSAGE": [self.players[client_socket], args]
                        }
                    self.send_to_all(response)

            elif key == 'DRAW_CARD':
                if client_socket in self.players:
                    self.draw_card(client_socket)

            elif key == 'PLAY_CARD':
                if client_socket in self.players:
                    card_id, card_tuple = args[0], tuple(args[1])
                    self.play_card(client_socket, card_id, card_tuple)

            elif key == 'SHOUT_DCCUATRO':
                if client_socket in self.players:
                    self.shout_dccuatro(client_socket)


    def send(self, msg, client_socket):
        prefix = '0'.encode('utf-8') # 0 means we are sending a normal message
        msg_bytes = json.dumps(msg).encode('utf-8')
        msg_length = len(msg_bytes).to_bytes(4, byteorder='big')
        client_socket.sendall(prefix + msg_length + msg_bytes)

        # ============== LOG ==============
        print('{:<15s} {:^15s} {:>15s}'.format(
            'server', 'send', json.dumps(msg)))
        # ============== LOG ==============

    def send_to_all(self, msg):
        """
        Method to send a message to all players connected or only
        to players that are playing, depending on to_players argument
        """
        with self.lock: # acquire lock to read/write to self.players
            for player in self.players:
                self.send(msg, player)

    def check_username(self, client_socket, username):
        """
        check if username is valid:
        1. if room is not full,
        2. if name is not used,
        then join socket to self.players with username as value and
        socket as key, and send NEW_USER: username command to existing players
        """

        if len(self.players) >= self.parameters['players']:
            response = {"FULL": None}
        elif not username.isalnum():
            response = {"INVALID_USERNAME": username}
        elif username in [i for i in self.players.values()]:
            response = {"INVALID_USERNAME": username}
        else:
            # send the player in the first element and the rest of existing
            # players in subsequent elements
            opponents = [i for i in self.players.values()]
            response = {"VALID_USERNAME": [username, *opponents]}
            # update existing players about new player:
            update = {"NEW_PLAYER": username}
            self.send_to_all(update)
            # append new player to existing players
            self.players[client_socket] = username
            # check if room is complete
            if len(self.players) == self.parameters['players']:
                # notify new user about valid username:
                self.send(response, client_socket)
                self.start_game([i for i in self.players.values()])
                return # break
        self.send(response, client_socket)

    def start_game(self, players):
        """
        (1) initialize and start game engine
        (2) send START to everyone with players in turn order as value
        (3) send TURN to everyone with first to play as value
        (4) send face up cards (hand) separately to each player
        (5) send face down sprite once to everyone
        (6) send discard pile card to everyone
        """
        self.game_engine = GameEngine(players)
        self.game_engine.start()
        # send START and players ordered by turn as value:
        self.send_to_all({"START": [i.name for i in self.game_engine.players]})
        # send current turn:
        player_turn = self.game_engine.players[self.game_engine.turn].name
        self.send_to_all({"TURN": player_turn})

        # send face down sprite to everyone:
        self.send_card(('reverso', ''), '2')
        # send discard pile card to everyone:
        self.send_card(self.game_engine.discard_pile, '1')

        # send hand to each player:
        for socket_, player_name in self.players.items():
            cards = [p.cards for p in self.game_engine.players
                        if p.name == player_name][0]
            opponents_sock = [sock for sock, name in self.players.items() if
                    name != player_name]
            for card in cards:
                self.send_card(card, '0', client_socket=socket_)
                for opponent_sock in opponents_sock:
                    # send OPPONENT_CARD command to each opponent of player
                    message = {"OPPONENT_CARD": [player_name, True]}
                    self.send(message, opponent_sock)

    def send_card(self, card_tuple, destination, client_socket=False, folder='simple'):
        """
        can send a card to a particular socket unless no socket is
        passed in which case sends cards to every connected socket """
        """
        card: tuple like ('1', 'azul')
        destination: whether it belongs to discard pile or to the player hand
            0 -> player card
            1 -> discard pile card
            2 -> face down card to be stored in each client
        """
        prefix = '1'.encode('utf-8') # 1 means we are sending a card

        dir_path = path.join('sprites', folder)
        # color cards may have a color assigned from playing it, must ignore:
        type, color = ('color', '') if card_tuple[0] == 'color' else card_tuple
        underscore = '' if type in ['reverso', 'color'] else '_'
        card_name = f'{type}{underscore}{color}.png'
        card_path = path.join(dir_path, card_name)

        with open(card_path, 'rb') as file:
            image_data = file.read()

        type_bytes = type.encode('utf-8')
        """
        when a player draws a color card, it must reset its color att. to '',
        so the server can send a COLOR_CHANGE command if player plays that card
        based on the att. being ''. else, if the player plays a color card with
        an att. that is not '', it means the color was already picked,
        in which case it must keep it.
        """
        if destination == '0':
            # if it goes to the player hand, reset color to ''
            color_bytes = color.encode('utf-8')
        else:
            # if it goes to the discard pile, keep color
            color_bytes = card_tuple[1].encode('utf-8')


        type_length = len(type_bytes).to_bytes(4, byteorder='little')
        color_length = len(color_bytes).to_bytes(4, byteorder='little')
        image_length = len(image_data).to_bytes(4, byteorder='little')

        ids_bytes = list(map(lambda x: x.to_bytes(4,
                                byteorder='big'), (1, 2, 3)))

        message = bytearray(destination.encode('utf-8')
            + ids_bytes[0] + type_length + type_bytes
            + ids_bytes[1] + color_length + color_bytes
            + ids_bytes[2] + image_length + image_data)

        if client_socket:
            client_socket.sendall(prefix + message)
        else:
            for socket in self.players:
                socket.sendall(prefix + message)

        # ============== LOG ==============
        receiver = 'All' if not client_socket else self.players[client_socket]
        print('{:<15s} {:^20s} {:>20s}'.format(
            'server', f'send ({receiver}): image ', f'{card_tuple}: {destination}'))
        # ============== LOG ==============

    def draw_card(self, client_socket):
        """ sends drawed card and updates the game if game engine
        returns a card, else the draw was invalid """

        player = self.players[client_socket]
        drawed_card = self.game_engine.draw_card(player)
        if drawed_card: # returns False if draw as invalid
            # update opponents about the draw
            for socket, name in self.players.items():
                if name != player:
                    self.send({"OPPONENT_CARD": [player, True]}, socket)
            # log action in chat:
            self.send_to_all({"CHAT_MESSAGE": [f'{player}',
                                                'ha robado una carta']})
            # update turn:
            player_turn = self.game_engine.players[self.game_engine.turn].name
            self.send_to_all({"TURN": player_turn})
            # send drawed card to player hand:
            self.send_card(drawed_card, '0', client_socket=client_socket)
            self.check_winner(player)

    def play_card(self, client_socket, card_id, card_tuple):
        """ if game engine returns True, removes card from hand and updates
        the game """
        player = self.players[client_socket]
        if card_tuple == ('color', '') and\
            self.game_engine.valid_card(card_tuple, player):
            # player should pick a color
            self.send({"CHOOSE_COLOR": card_id}, client_socket)
        else:
            if self.game_engine.play_card(card_tuple, player): # play succeed
                # send card id so client can delete it:
                self.send({"PLAYER_CARD": card_id}, client_socket)
                # send command to opponents to delete an opponent card
                for socket, name in self.players.items():
                    if name != player:
                        self.send({"OPPONENT_CARD": [player, False]}, socket)

                chat_message = [f'{player}',
                                f'ha jugado {card_tuple[0]} {card_tuple[1]}']
                self.send_to_all({"CHAT_MESSAGE": chat_message})
                # update turn:
                player_turn = self.game_engine.players[self.game_engine.turn].name
                self.send_to_all({"TURN": player_turn})
                # update discard pile:
                self.send_card(self.game_engine.discard_pile, '1')
                # in case someone throwed +2, notify users in the chat:
                if self.game_engine.players[self.game_engine.turn].must_pass:
                    draws = self.game_engine.accumulated_draw
                    chat_message = [f'{player_turn}', f'debe robar {draws} cartas']
                    self.send_to_all({"CHAT_MESSAGE": chat_message})

                self.check_winner(player)

            else:
                # ============== LOG ==============
                print('{:<15s} {:^15s} {:>15s}'.format(
                    'server', 'play', f'error: {player}, {card_tuple}'))
                # ============== LOG ==============


    def shout_dccuatro(self, client_socket):
        """ if game engine returns False, no one had to draw,
        else it returns the player that mistakenly shouted or
        had to draw and the cards it drawed """
        shouter = self.players[client_socket]
        drawer, drawed_cards = self.game_engine.shout_dccuatro(shouter)
        if drawed_cards:
            for card in drawed_cards:
                for socket, name in self.players.items():
                    if name == drawer:
                        self.send_card(card, '0', client_socket=socket)
                    else:
                        # update opponents view of player hand
                        self.send({"OPPONENT_CARD": [drawer, True]}, socket)
            if drawer == shouter:
                chat_message = [
                    f'{drawer}',
                    f'ha robado {len(drawed_cards)} cartas por haber gritado '
                    +'DCCuatro erroneamente'
                ]
            else:
                chat_message = [
                    f'{drawer}',
                    f'ha robado {len(drawed_cards)} cartas por que {shouter} '
                    +'ha gritado DCCuatro'
                ]
            self.send_to_all({"CHAT_MESSAGE": chat_message})
            # update turn in case there was a change:
            player_turn = self.game_engine.players[self.game_engine.turn].name
            self.send_to_all({"TURN": player_turn})
            self.check_winner(drawer)
        else:
            chat_message = [f'{shouter}', 'ha gritado DCCuatro']
            self.send_to_all({"CHAT_MESSAGE": chat_message})



    def check_winner(self, player):
        """ checks if player is still playing. Also checks if game is active """

        if not self.game_engine.game_active:
            self.send_to_all({"END": self.game_engine.winner})
            self.players = dict()
            return

        if player not in [i.name for i in self.game_engine.players]:

            for socket, name in self.players.items():
                if name == player:
                    self.send({"LOST": None}, socket)
                else:
                    self.send({"OPPONENT_LOST": player}, socket)
            self.send_to_all({"CHAT_MESSAGE": [f'{player}', 'ha perdido']})

        if len(self.players) == 1:
            _, player = *self.players.keys(), *self.players.values()
            self.send_to_all({"END": player})
            self.players = dict()
            return



if __name__ == '__main__':
    host, port = 'localhost', 1111
    parameters = {"TESTING": True}
    server = Server(port, host, parameters)
