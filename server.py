import socket
from threading import Thread, Lock
import time
import os
import pickle
import sys


from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal

soket_threads = []
soket_addr = []


class Server(QThread):

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.soket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.soket.bind((self.host, self.port))
        self.soket.listen(1)

    def run(self):

        print("Server açık ve dinliyor")
        # Yukarıda soket yapısı oluşturuldu artık gelen istekleri dinlicez.
        while True:
            conn, addr = self.soket.accept()
            # print(conn)---->#soket bilgisini tutar
            # print(addr)---->#ip,raddr ikilisini tutar
            create_socket_thread = Soket(conn, self)
            create_socket_thread.start()
            # Bağlanan istemcileri tutar(tipi soket türündendir)
            soket_threads.append(create_socket_thread)
            # Bağlanan istemcilerin ip,raddr ikilisini tutar.Her eleman bir tuple dır.
            soket_addr.append(addr)


class Soket(QThread):

    def __init__(self, conn, serverclass):
        super().__init__()
        self.conn = conn
        self.serverclass = serverclass

    def run(self):
        print("{} istemcisi için yeni bir thread oluşturuldu ve istekler dinlenmeye başladı".format(
            self.conn.getpeername()))
        a = Requests(self.conn, self)
        a.start()
        a.select()


class QSend(QThread):
    def __init__(self):
        super().__init__()
        pass

    def run(self):
        pass


class Requests(QThread):

    def __init__(self, conn, soket_thread):
        super().__init__()
        self.conn = conn
        self.lock = Lock()
        self.soket = soket_thread  # sadece silme için ihtiyac duyduk
        self.target = None

    def run(self):
        pass

    def select(self):
        while True:
            select = pickle.loads(self.conn.recv(4096))
            if select[0] == "connect":
                data = pickle.loads(self.conn.recv(2048))
                for i in soket_threads:
                    if str(i.conn.getpeername()) == data:
                        data = pickle.dumps(self.conn.getpeername())
                        i.conn.send(data)
                # Bağlantı onayı için bekleniyor
            elif select[0] == "remove":
                print(
                    f"{self.conn.getpeername()} adlı cihazın bağlantısı sonlandırılıyor")
                soket_threads.remove(self.soket)
                soket_addr.remove(self.conn.getpeername())
                self.conn.close()
                print("sonlandırıldı.")
                break
            elif select[0] == "list":
                data = pickle.dumps(soket_addr)
                self.conn.send(data)

            elif select[0] == "Onaylanmadı":
                for i in soket_threads:
                    if str(i.conn.getpeername()) == select[1]:
                        i.conn.send(pickle.dumps("Bağlantı izni verilmedi"))


class ServerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initui()
        self.server = Server(host="127.0.0.1", port=3856)

    def initui(self):
        self.start = QPushButton("Başlat")
        self.log = QTextEdit("Server Başladı")
        self.btn = QPushButton("Btn")
        vbox = QVBoxLayout()
        vbox.addWidget(self.log)
        vbox.addWidget(self.start)
        vbox.addWidget(self.btn)

        self.start.clicked.connect(self.baslat)

        self.setLayout(vbox)

        self.show()

    def baslat(self):
        self.server.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    serverwindow = ServerWindow()
    sys.exit(app.exec())
