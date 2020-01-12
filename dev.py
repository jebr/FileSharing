import http.server
import socketserver
import os
import sys
from urllib.request import urlopen
from http.server import HTTPServer, SimpleHTTPRequestHandler
from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import QApplication, QLabel, QFileDialog, QMessageBox

from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPixmap,  QFont

# PORT = 8080
#
# Handler = http.server.SimpleHTTPRequestHandler
#
# Bind = '127.0.0.1'
#
# Directory = '/Users/Jeroen/FileSharing'
#
# httpd = socketserver.TCPServer(("", PORT), Handler, Bind)
#
# print("serving at port", PORT)
# httpd.serve_forever()
#
#
# httpd.server_close()
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.environ.get("_MEIPASS2", os.path.abspath("."))
    return os.path.join(base_path, relative_path)


HOST, PORT = '127.0.0.1', 12345


class HttpDaemon(QtCore.QThread):
    def run(self):
        self._server = HTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
        self._server.serve_forever()

    def stop(self):
        self._server.shutdown()
        self._server.socket.close()
        self.wait()


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
        self.pushButton_start_server.clicked.connect(self.handleButton)
        # self.pushButton_stop_server.clicked.connect(self.stop_server)


        self.httpd = HttpDaemon(self)

    def handleButton(self):
        if self.button.text() == 'Start':
            self.httpd.start()
            self.button.setText('Test')
        else:
            urlopen('http://%s:%s/index.html' % (HOST, PORT))

    def closeEvent(self, event):
        self.httpd.stop()


def main():
    app = QApplication(sys.argv)
    widget = MainPage()
    widget.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
