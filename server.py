import socket
from threading import Thread
import time
import os
import pickle

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
        print("Bağlı olan istemci sayısı:{}".format(len(clients_thread)))
    def baglanti_liste_al(self,kaynak):
        os.system("clear")
        data=pickle.dumps(clients_ip)
        print("Liste gönderildi")
        kaynak.baglanti.send(data)
    def baglanti_istegi(self,kaynak):
        pass
        
class Soket(Thread):
    def __init__(self,baglanti,server):
        super().__init__()
        self.baglanti=baglanti
        self.server=server
    def run(self):
        while True:
            gsecim=self.baglanti.recv(1024).decode("utf-8")
            if gsecim=="Sil":
                self.server.baglanti_sil(self)
            elif gsecim=="Listele":
                self.server.baglanti_liste_al(self)
            elif gsecim=="Baglan":
                self.baglanti.send("Hangi cihaza bağlanmak istiyorsun: ".encode("utf-8"))
                gelen_cevap=self.baglanti.recv(1024).decode("utf-8")
                self.server.baglanti_istegi(gelen_cevap)
            elif gsecim=="TTT":
                print("aaa.py dan geldi soket")

if __name__ == "__main__":
    server=Server(host="127.0.0.1",port=6598)
    server.start()



