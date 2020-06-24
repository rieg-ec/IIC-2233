from server import Server
from utils import json_hook
import json

if __name__ == '__main__':
    with open('parameters.json', 'r') as file:
        parameters = json.loads(file.read(), object_hook=json_hook)

    host, port = parameters['host'], parameters['port']
    server = Server(host, port, parameters)
