import threading
import socket
import time
import json
from collections import defaultdict
from game_engine import GameEngine
from os import path

# TODO: # QUESTION: what if i allow for multiple instances
                #   of the game? like 2 simultaneous games?





class Server:
    # TODO: MAKE A CLIENT OBJECT TO STORE INFORMATION LIKE WHICH SPRITE TO SEND,
    #       IF HAS LOST, NAME,
    # TODO: remove player form game engine players list if disconnects
    # TODO: when removing player from self.players, another player could connect
    #           see what happens

    def __init__(self, host, port, parameters): # TODO: remove parameters as a
        print('Starting server')                #       attribute and read parameters.json
        self.host = host                        #       on each class that uses it
        self.port = port
        self.socket_server = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.lock = threading.RLock() # RLock for recursive methods
        self.socket_server.bind((self.host, self.port))
        self.socket_server.listen()
        self.accept_connections()
        self.players = defaultdict(None) # validated users
        self.parameters = parameters
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
                    print('{:<15s} {:^15s} {:>15s}'.format(
                        'client', 'send', data))
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
        with self.lock:
            if 'CHECK_USERNAME' in dict_request:
                self.check_username(client_socket,
                    dict_request['CHECK_USERNAME'])

            elif 'CHAT_MESSAGE' in dict_request:
                # TODO: use CHAT_MESSAGE command to display players actions in
                # game chat
                response = {
                    "CHAT_MESSAGE": [
                        self.players[client_socket], # author
                        dict_request["CHAT_MESSAGE"] # message
                    ]}
                self.send_to_all(response)

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
        # TODO: check for valid usernames (dont allow '')
        # room is not full:
        if len(self.players) >= self.parameters['players']:
            response = {"FULL": None}
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

    def send_card(self, card, destination, client_socket=False, folder='simple'):
        """ can send a card to a particular socket unless no socket is
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
        type, color = card
        underscore = '' if type in ['reverso', 'color'] else '_'
        card_name = f'{type}{underscore}{color}.png'
        card_path = path.join(dir_path, card_name)

        with open(card_path, 'rb') as file:
            image_data = file.read()

        type_bytes, color_bytes = type.encode('utf-8'), color.encode('utf-8')

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
            'server', f'send ({receiver}): image ', f'{card}: {destination}'))
        # ============== LOG ==============


if __name__ == '__main__':
    host, port = 'localhost', 1111
    parameters = {"TESTING": True}
    server = Server(port, host, parameters)
