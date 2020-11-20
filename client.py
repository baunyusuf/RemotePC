from threading import Thread
import socket
import os
from arayüz import Pencere
from PyQt5 import QtWidgets
import sys
import pickle

class Client(Thread):
    def __init__(self,host,port):
        super().__init__()
        self.host=host
        self.port=port
        self.soket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def run(self):
        self.soket.connect((self.host,self.port))
        

def sil():
    sock_create.soket.send("Sil".encode("utf-8"))
    sys.exit()
def listele():
    try:
        sock_create.soket.send("Listele".encode("utf-8"))
        gelen_data=sock_create.soket.recv(4096)
        data=pickle.loads(gelen_data)
        pencere.textedit.clear()
        for i in data:
            print(i)
            pencere.textedit.append(i)
            print("")
        
    except:
        print("Server açık değil veya ulaşılamıyor")
    

if __name__ == "__main__":
    sock_create=Client(host="127.0.0.1",port=6598)
    sock_create.start()
    app=QtWidgets.QApplication(sys.argv)
    pencere=Pencere()

    pencere.listelebtn.clicked.connect(listele)
    pencere.kapatbtn.clicked.connect(sil)

    if not app.exec():
        sil()
