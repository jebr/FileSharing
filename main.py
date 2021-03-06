import sys
import os
import platform
import logging
import subprocess
import http.server
import socketserver

from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog, QMessageBox

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap,  QFont

try:
    os.chdir(os.path.dirname(sys.argv[0]))
except Exception:
    pass


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.environ.get("_MEIPASS2", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


# Set logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# logging.disable(logging.DEBUG)


# PyQT GUI
class MainPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Load Main UI
        loadUi(resource_path('ui_files/main_window.ui'), self)
        # Set Size Application
        self.setFixedSize(640, 480)
        # Set Application Icon
        # self.setWindowIcon(QtGui.QIcon(resource_path('assets/merge-logo.svg')))

        # Logo
        # label_logo
        # self.label_logo = QLabel(self)
        # self.label_logo.setGeometry(50, 40, 50, 50)
        # pixmap = QPixmap(resource_path('assets/merge-logo.svg'))
        # pixmap = pixmap.scaledToWidth(50)
        # self.label_logo.setPixmap(pixmap)

        # Buttons
        self.pushButton_start_server.clicked.connect(self.start_server)
        self.pushButton_stop_server.clicked.connect(self.stop_server)

        self.port = 8080

        self.handler = http.server.SimpleHTTPRequestHandler

        self.bind = '127.0.0.1'

        self.directory = '/Users/Jeroen/FileSharing'

        self.httpd = socketserver.TCPServer(("", self.port), self.handler, self.bind)

    def start_server(self):
        logging.info('Server started at {}'.format(self.port))
        self.httpd.serve_forever()

    def stop_server(self):
        self.httpd.server_close()


def main():
    app = QApplication(sys.argv)
    widget = MainPage()
    widget.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()