import socket
from threading import Thread,Lock
import threading
import time
import os
import pickle
from PyQt5 import QtWidgets


clients_thread=[]
clients_ip=[]

class Server(Thread):
    def __init__(self,host,port):
        super().__init__()
        self.host=host
        self.port=port
    def run(self):
        soket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        soket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        soket.bind((self.host,self.port))
        soket.listen(1)
        print("Server açık ve dinliyor")
        #Yukarıda soket yapısı oluşturuldu artık gelen istekleri dinlicez.
        while True:
            baglanti=soket.accept()[0]
            #print(type(baglanti.getpeername()[1]))soket raddr int tipinde
            soket_calistir=Soket(baglanti,self)
            soket_calistir.start()
            clients_thread.append(soket_calistir)
            clients_ip.append(baglanti.getpeername())
            #clients_ip.append(baglanti.getpeername()[0])
            print(clients_thread)
            print(len(clients_thread))
    def baglanti_sil(self,kaynak):
        clients_thread.remove(kaynak)
        clients_ip.remove(kaynak.baglanti.getpeername())
        kaynak.baglanti.close()
        print("Bağlı olan istemci sayısı:{}".format(len(clients_thread)))
    def baglanti_liste_al(self,kaynak):
        os.system("clear")
        print(threading.enumerate())
        data=pickle.dumps(clients_ip)
        print("Listes gönderildi")
        kaynak.baglanti.send(data)
    def data_al(self,kaynak):
        i=0
        toplam=0
        x=kaynak.recv(1024)
        while x:
            i+=1
            print("Gelen paket numarası ve boyutu:{}-{}".format(i,len(x)))
            toplam+=len(x)
            print(toplam)
            x=kaynak.recv(1024)
        print("Toplam paket boyutu:{}".format(toplam))
        


class Soket(Thread):
    def __init__(self,baglanti,server):
        super().__init__()
        self.baglanti=baglanti
        self.server=server
        self.lock=Lock()
    def run(self):
        #print(type(self.baglanti))
        print(threading.active_count())
        try:
            while True:
                gsecim=self.baglanti.recv(1024).decode("utf-8")
                if gsecim=="Sil":
                    self.server.baglanti_sil(self)
                    break
                elif gsecim=="Listele":
                    self.server.baglanti_liste_al(self)
                elif gsecim=="Baglan":
                    #hedef_istemci=#Client tan alınan hedef raddr alınmalı
                    self.baglanti.send("Server bağlantı isteğini aldı".encode("utf-8"))
                    self.server.data_al(self.baglanti)
        except (ConnectionRefusedError,ConnectionResetError):
            clients_thread.remove(self)#Bağlantı hatası alındığında bağlı olan istemci listede kalmaması gerektiğinden kullandıldı.


if __name__ == "__main__":
    server=Server(host="127.0.0.1",port=3963)
    server.start()


