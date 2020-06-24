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
        self.clients = defaultdict(None)
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

        with self.lock: # acquire a lock to read/write to self.clients
            if client_socket in self.clients:
                # if not in self.clients means user hasn't authenticated
                # in login window
                user = self.clients[client_socket]
                command = "USER_LEFT"
                msg_to_all = {"USER_LEFT": user}
                del self.clients[client_socket]

                self.send_to_all(msg_to_all)
            else:
                command = user = None

        client_socket.close()

    def process_request(self, request, client_socket):
        dict_request = json.loads(request)

        if 'CHECK_USERNAME' in dict_request:
            self.check_username(client_socket,
                dict_request['CHECK_USERNAME'])


    def send(self, msg, client_socket):
        msg_bytes = json.dumps(msg).encode('utf-8')
        msg_length = len(msg_bytes).to_bytes(5, byteorder='big')
        client_socket.sendall(msg_length + msg_bytes)
        # ============== LOG ==============
        print('{:<15s} {:^15s} {:>15s}'.format(
            'server', 'send', json.dumps(msg)))

    def send_to_all(self, msg, to_players=False):
        """
        Method to send a message to all clients connected or only
        to clients that are playing, depending on to_players argument
        """
        with self.lock: # acquire lock to read/write to self.clients
            if not to_players:
                for client in self.clients:
                    try:
                        self.send(msg, client)
                    except ConnectionError:
                        del self.clients[client]
                        command = {"USER_LEFT": client}
                        self.send_to_all(command)
            else:
                for player in self.players:
                    try:
                        self.send(msg, player)
                    except ConnectionError:
                        del self.players[player]
                        del self.clients[player] # remove from clients also
                        command = {"USER_LEFT": client}
                        self.send_to_all(command)

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
        then join socket to self.clients with username as value and
        socket as key, and send NEW_USER: username command to existing players
        """
        # room is not full:
        with self.lock: # acquire a lock to read/write to self.clients
            if len(self.clients) >= self.parameters['clients']:
                response = {"FULL": None}
            elif username in [i for i in self.clients.values()]:
                response = {"INVALID_USERNAME": username}
            else:
                # send the player in the first element and the rest of existing
                # players in subsequent elements
                opponents = [i for i in self.clients.values()]
                response = {"VALID_USERNAME": [username, *opponents]}
                # update existing clients about new player:
                update = {"NEW_PLAYER": username}
                self.send_to_all(update)
                # append new player to existing players
                self.clients[client_socket] = username
                # check if room is complete
                if len(self.clients) == self.parameters['clients']:
                    # notify new user about valid username:
                    self.send(response, client_socket)
                    # send START command to everyone
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
            command = {"START": None}
            self.players = dict()
            for client in self.clients:
                self.players[client] = {
                    'name': self.clients[client],
                    'cards': ['ace_1', 'spades_2']
                    }




if __name__ == '__main__':
    host, port = 'localhost', 1111
    parameters = {"TESTING": True}
    server = Server(port, host, parameters)
