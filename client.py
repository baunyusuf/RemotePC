import io
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QRadioButton, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QLabel
from PyQt5.QtCore import *
import sys
import time
from threading import Thread, Lock
import socket
import pickle
import os

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
                print("Server aktif değil")
                time.sleep(1)


class İzin(QThread):
    sinyal_connect = pyqtSignal(tuple)
    sinyal_list = pyqtSignal(list)
    cevap_sinyal = pyqtSignal(str)

    def __init__(self, conn):
        super().__init__()
        self.conn = conn
        self.lock = Lock()

    def run(self):
        while True:
            try:
                data = self.conn.soket.recv(4096)
                data = pickle.loads(data)
                if type(data) == tuple:
                    self.sinyal_connect.emit(data)
                    # Break yaptık çünkü bağlantı durumuna göre farklı bir işlem yapabilmek için bu döngüden kurtulmalıyız.(Veri Gönderme işlemi için)
                elif type(data) == list:
                    self.sinyal_list.emit(data)
                elif type(data) == str:
                    self.cevap_sinyal.emit(data)
            except ConnectionAbortedError:
                break
            except OSError:
                continue


class Pencere(QWidget):
    def __init__(self, conn, anaekran):
        super().__init__()
        self.init_ui()
        self.conn = conn
        self.anaekran = anaekran

    def init_ui(self):
        self.defaul = os.getcwd()
        self.label = QLabel(os.getcwd())
        self.dosya_list = QListWidget()
        self.dosya_gonder = QPushButton("Dosya Gönder")
        self.listele = QPushButton("Listele")
        self.sonlandir = QPushButton("Bitir")
        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.label)
        hbox.addStretch()
        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(self.dosya_list)
        vbox.addWidget(self.dosya_gonder)
        vbox.addWidget(self.listele)
        vbox.addWidget(self.sonlandir)
        self.setLayout(vbox)

        for i in os.listdir(self.defaul):
            self.dosya_list.addItem(str(i))

        self.listele.clicked.connect(self.liste)
        self.sonlandir.clicked.connect(self.son)

    def liste(self):
        yeni_yol = self.dosya_list.currentItem().text()
        if os.path.isdir(yeni_yol) == True:
            self.dosya_list.clear()
            for i in os.listdir(os.chdir(yeni_yol)):
                self.dosya_list.addItem(str(i))
        else:
            QMessageBox.about(self, "Bilgilendirme", "Bu bir dizin değildir")

    def son(self):
        self.close()
        self.anaekran.show()


class AnaEkran(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = Client(host="127.0.0.1", port=3856)
        self.conn.start()
        self.init_ui()
        self.izin = İzin(self.conn)
        self.izin.sinyal_connect.connect(self.yayinla)
        self.izin.sinyal_list.connect(self.liste)
        self.izin.cevap_sinyal.connect(self.cevap)
        self.izin.start()

    def init_ui(self):
        self.filewindow = Pencere(self.conn, self)
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
        self.label_my_ip.setText(str(self.conn.soket.getsockname()))
        self.list.clear()
        for i in a:
            if self.conn.soket.getsockname() != i:
                self.list.addItem(str(i))

    def gonder(self):
        try:
            data = ("connect", 1)
            self.conn.soket.send(pickle.dumps(data))
            self.conn.soket.send(pickle.dumps(self.list.currentItem().text()))
        except OSError:
            pass
        except AttributeError:
            print("Hedef secilmedi")

    def exit(self):
        try:
            data = ("remove", 1)
            self.conn.soket.send(pickle.dumps(data))
            self.conn.soket.close()
            conn_list.clear()
            os.system("cls")
            sys.exit()
        except ConnectionResetError:
            sys.exit()

    def yayinla(self, a):
        ret = QMessageBox.question(
            self, "Onay Kutusu", f"{a} senden izin istiyor ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if ret == QMessageBox.Yes:
            print("Bağlantı onaylandı")
            self.hide()
            self.filewindow.show()
        elif ret == QMessageBox.No:
            a = ("Onaylanmadı", str(a))
            b = pickle.dumps(a)
            self.conn.soket.send(b)
            self.izin.start()

    def show_list(self):
        try:
            data = ("list", 1)
            self.conn.soket.send(pickle.dumps(data))
        except OSError:
            pass

    def cevap(self, a):
        QMessageBox.about(self, "Bilgilendirme", a)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ana_ekran = AnaEkran()
    if not app.exec():
        ana_ekran.exit()
