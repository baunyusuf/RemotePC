from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QRadioButton, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QLabel
from PyQt5.QtCore import *
import sys
import time
from threading import Thread, Lock
import socket
import pickle

conn_list = []


class Client(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        while True:
            try:
                self.soket.connect((self.host, self.port))
                break
            except ConnectionRefusedError:
                print("a")
                time.sleep(1)


class İzin(QThread):
    sinyal_connect = pyqtSignal(tuple)
    sinyal_list = pyqtSignal(list)

    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.lock = Lock()

    def run(self):
        while True:
            try:
                data = self.conn.soket.recv(2048)
                data = pickle.loads(data)
                if type(data) == tuple:
                    self.sinyal_connect.emit(data)
                else:
                    if type(data) == list:
                        self.sinyal_list.emit(data)
            except ConnectionAbortedError:
                break
            except OSError:
                continue


class File_Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initui()

    def initui(self):
        self.list = QListWidget()
        self.son = QPushButton("Sonlandır")
        vbox = QVBoxLayout()
        vbox.addWidget(self.list)
        vbox.addWidget(self.son)
        self.setLayout(vbox)


class AnaEkran(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = Client(host="127.0.0.1", port=3963)
        self.conn.start()
        self.init_ui()
        self.izin = İzin(self.conn)
        self.izin.sinyal_connect.connect(self.yayinla)
        self.izin.sinyal_list.connect(self.liste)
        self.izin.start()

    def init_ui(self):
        self.filewindow = File_Window()
        self.label_my_ip = QLabel(str(self.conn.soket.getsockname()))
        self.list = QListWidget()
        self.file = QRadioButton("Dosya Paylaşımı")
        self.remote = QRadioButton("Ekran Paylaşımı")
        self.baglanbtn = QPushButton("Bağlan")
        self.listelebtn = QPushButton("Listele")

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.addWidget(self.list)
        vbox.addWidget(self.file)
        vbox.addWidget(self.remote)
        vbox.addWidget(self.baglanbtn)
        vbox.addWidget(self.listelebtn)
        hbox.addStretch()
        hbox.addWidget(self.label_my_ip)
        hbox.addStretch()
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        self.show()
        self.baglanbtn.clicked.connect(self.gonder)
        self.listelebtn.clicked.connect(self.show_list)

    def liste(self, a):
        self.list.clear()
        for i in a:
            if self.conn.soket.getsockname() != i:
                self.list.addItem(str(i))

    def gonder(self):
        try:
            self.conn.soket.send("connect".encode("utf-8"))
            self.conn.soket.send(
                self.list.currentItem().text().encode("utf-8"))
        except OSError:
            pass

    def exit(self):
        self.conn.soket.send("remove".encode("utf-8"))
        self.conn.soket.close()
        conn_list.clear()
        sys.exit()

    def yayinla(self, a):
        ret = QMessageBox.question(
            self, "Onay Kutusu", f"{a} senden izin istiyor ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ret == QMessageBox.Yes:
            print("Bağlantı onaylandı")
            self.hide()
            self.filewindow.show()
            self.filewindow.son.clicked.connect(self.hide())
        elif ret == QMessageBox.No:
            print("Bağlantı onaylanmadı")

    def show_list(self):
        try:
            self.conn.soket.send("list".encode("utf-8"))
        except OSError:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ana_ekran = AnaEkran()
    if not app.exec():
        ana_ekran.exit()
