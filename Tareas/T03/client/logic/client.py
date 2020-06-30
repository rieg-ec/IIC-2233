from PyQt5.QtCore import QObject, pyqtSignal
import threading
import json
import socket


class Client(QObject):
    server_message_signal = pyqtSignal(dict)
    server_image_signal = pyqtSignal(list)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        self.socket.connect((self.host, self.port))
        thread = threading.Thread(
            target=self.listen_thread, daemon=True)
        thread.start()

    def listen_thread(self):
        print('listening to server')

        while True:
            prefix = self.socket.recv(1).decode('utf-8') # 0: normal message,
                                                        # 1: image
            if prefix == '0':
                response_bytes_length = self.socket.recv(4)
                response_length = int.from_bytes(
                    response_bytes_length, byteorder='big')
                response = bytearray()
                # the rest of bytes are the response in json
                while len(response) < response_length:
                    read_length = min(4096, response_length - len(response))
                    response.extend(self.socket.recv(read_length))

                data = response.decode('utf-8')
                dict_response = json.loads(data)
                self.server_message_signal.emit(dict_response)

            elif prefix == '1':
                destination = self.socket.recv(1).decode('utf-8')
                for _ in range(3):
                    # destination tells whether the card is a face down card,
                    # or a player hand card or it should be render in discard pile
                    id_b = self.socket.recv(4)
                    id = int.from_bytes(id_b, byteorder='big')

                    length_b = self.socket.recv(4)
                    length = int.from_bytes(length_b, byteorder='little')

                    info = bytearray()
                    while len(info) < length:
                        read_length = min(4096, length - len(info))
                        info.extend(self.socket.recv(read_length))

                    if id == 1:
                        type = info.decode('utf-8')
                    elif id == 2:
                        color = info.decode('utf-8')
                    elif id == 3:
                        sprite = info

                card_tuple = (type, color)
                response = [destination, card_tuple, sprite]
                self.server_image_signal.emit(response)

            elif prefix == b'':
                # lost connection to the server
                break
        self.socket.close()

        # ================ LOGS =====================
        print('---------------------------------')
        print('listen_thread():')
        print('connection closed')
        print('---------------------------------')
        # ================ LOGS =====================

    def send(self, msg):
        """
        First 4 bytes are response length
        msg is a dict
        """
        msg_bytes = json.dumps(msg).encode('utf-8')
        msg_length = len(msg_bytes).to_bytes(4, byteorder='big')
        self.socket.sendall(msg_length + msg_bytes)

if __name__ == '__main__':
    host, port = 'localhost', 1111
    client = Client(host, port)
    client.connect_to_server()
    client.repl()
