import socket
from threading import Thread, Lock
import time
import os
import pickle


soket_threads = []
soket_addr = []


class Server(Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port

    def run(self):
        soket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        soket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        soket.bind((self.host, self.port))
        soket.listen(1)
        print("Server açık ve dinliyor")
        # Yukarıda soket yapısı oluşturuldu artık gelen istekleri dinlicez.
        while True:
            conn, addr = soket.accept()
            # print(conn)---->#soket bilgisini tutar
            # print(addr)---->#ip,raddr ikilisini tutar
            create_socket_thread = Soket(conn, self)
            create_socket_thread.start()
            # Bağlanan istemcileri tutar(tipi soket türündendir)
            soket_threads.append(create_socket_thread)
            # Bağlanan istemcilerin ip,raddr ikilisini tutar.Her eleman bir tuple dır.
            soket_addr.append(addr)


class Soket(Thread):
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


class Requests(Thread):
    def __init__(self, conn, soket_thread):
        super().__init__()
        self.conn = conn
        self.lock = Lock()
        self.soket = soket_thread  # sadece silme için ihtiyac duyduk

    def run(self):
        pass

    def select(self):
        try:
            while True:
                select = self.conn.recv(4096).decode("utf-8")
                if select == "connect":
                    data = self.conn.recv(2048).decode("utf-8")
                    for i in soket_threads:
                        if str(i.conn.getpeername()) == data:
                            data = pickle.dumps(i.conn.getpeername())
                            i.conn.send(data)
                elif select == "remove":
                    soket_threads.remove(self.soket)
                    soket_addr.remove(self.conn.getpeername())
                elif select == "list":
                    data = pickle.dumps(soket_addr)
                    self.conn.send(data)

        except ConnectionResetError:
            soket_threads.remove(self.soket)
            soket_addr.remove(self.conn.getpeername())


if __name__ == "__main__":
    server = Server(host="127.0.0.1", port=3963)
    server.start()
