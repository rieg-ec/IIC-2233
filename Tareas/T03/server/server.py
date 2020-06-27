import threading
import socket
import time
import json
from collections import defaultdict

class Server:

    def __init__(self, host, port, parameters):
        print('Starting server')
        self.host = host
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
                request_bytes_length = client_socket.recv(5)
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
        msg_bytes = json.dumps(msg).encode('utf-8')
        msg_length = len(msg_bytes).to_bytes(5, byteorder='big')
        client_socket.sendall(msg_length + msg_bytes)

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

    def send_cards(self):
        """
        Method to send serialized card images
        """
        pass

    def check_username(self, client_socket, username):
        """
        check if username is valid:
        1. if room is not full,
        2. if name is not used,
        then join socket to self.players with username as value and
        socket as key, and send NEW_USER: username command to existing players
        """
        # room is not full:
        with self.lock: # acquire a lock to read/write to self.players
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
                    # send START command to everyone
                    # TODO: transform below command to a function that
                    # sends START command to each player with its corresponding
                    # face up cards, plus each opponent number of face down
                    # cards and the face down card sprite
                    start = {"START": None}
                    self.send_to_all(start)
                    return # break
            self.send(response, client_socket)

        def start_game(self):
            """
            Method called when room fills.
            Creates a new data structure to store sockets, names and cards of
            active players in the form:
                dict[socket] = {'name': name,
                                'cards': [card_1, card_2.. card_n]}
            """
            pass


if __name__ == '__main__':
    host, port = 'localhost', 1111
    parameters = {"TESTING": True}
    server = Server(port, host, parameters)
