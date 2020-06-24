import sys
from controller import Controller
from PyQt5.QtWidgets import QApplication
from utils import json_hook
import json

if __name__ == '__main__':
    with open('parameters.json', 'r') as file:
        parameters = json.loads(file.read(), object_hook=json_hook)

    app = QApplication([])
    controller = Controller(parameters)
    try:
        controller.logic.connect_to_server()
        sys.exit(app.exec_())
    except ConnectionRefusedError:
        print('connection refused from server')
        sys.exit()
