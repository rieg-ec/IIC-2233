from PyQt5.QtCore import QObject, pyqtSignal
import threading
import json
import socket


class Client(QObject):
    server_message_signal = pyqtSignal(dict)

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
            response_bytes_length = self.socket.recv(5)
            response_length = int.from_bytes(
                response_bytes_length, byteorder='big')
            response = bytearray()
            # the rest of bytes are the response in json
            while len(response) < response_length:
                read_length = min(4096, response_length - len(response))
                response.extend(self.socket.recv(read_length))

            if response != b'':
                data = response.decode('utf-8')
                dict_response = json.loads(data)
                self.server_message_signal.emit(dict_response)
            else:
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
        msg_length = len(msg_bytes).to_bytes(5, byteorder='big')
        self.socket.sendall(msg_length + msg_bytes)

if __name__ == '__main__':
    host, port = 'localhost', 1111
    client = Client(host, port)
    client.connect_to_server()
    client.repl()
