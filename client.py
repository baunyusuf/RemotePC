from threading import Thread
import socket
import os
import pyautogui
from arayüz import Pencere
from PyQt5 import QtWidgets
import sys

class Client(Thread):
    def __init__(self,host,port):
        super().__init__()
        self.host=host
        self.port=port
        self.soket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def run(self):
        self.soket.connect((self.host,self.port))
        

def sil(self):
    client_baslat.soket.send("Sil".encode("utf-8"))
    sys.exit(0)
def listele(self):
    client_baslat.soket.send("Listele".encode("utf-8"))
    

if __name__ == "__main__":
    client_baslat=Client(host="127.0.0.1",port=6598)
    client_baslat.start()
    app=QtWidgets.QApplication(sys.argv)
    pencere=Pencere()
    pencere.kapat.clicked.connect(sil)
    pencere.listele.clicked.connect(listele)




    sys.exit(app.exec())
        

    

        

    
    
    