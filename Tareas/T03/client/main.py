import sys
from controller import Controller
from PyQt5.QtWidgets import QApplication
from utils import json_hook
import json

if __name__ == '__main__':

    app = QApplication([])
    controller = Controller()
    try:
        controller.logic.connect_to_server()
        sys.exit(app.exec_())
    except ConnectionRefusedError:
        print('connection refused from server')
        sys.exit()
