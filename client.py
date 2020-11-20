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
        

def kapat():
    sock_create.soket.send("Sil".encode("utf-8"))
    sys.exit()
def listele():
    try:
        sock_create.soket.send("Listele".encode("utf-8"))
        gelen_data=sock_create.soket.recv(4096)
        data=pickle.loads(gelen_data)
        pencere.textedit.clear()
        for i in data:
            pencere.textedit.append(str(i))
            #print(tuple(i)[0])
        
    except:
        print("Server açık değil veya ulaşılamıyor")
def baglan(radio1,radio2):
    #print("Bağlana basıldı")
    #sock_create.soket.send("Baglan".encode("utf-8"))
    try:
        if radio1:
            print("Dosya Transferi seçildi")
            a=int(pencere.Hedef_IP_Line.text())
            print(type(a))
            print(a)
            #dosya_sec()
        elif radio2:
            print("Ekran Paylaşımı seçildi")
        else:
            print("Seçim yapılmadı")
    except:
        print("Beklenmeyen hata")

def dosya_sec():
    dosya_ismi=QtWidgets.QFileDialog.getOpenFileName(pencere,"Dosya Seç",os.getenv("HOME"))
    print(dosya_ismi)

if __name__ == "__main__":
    sock_create=Client(host="127.0.0.1",port=6598)
    sock_create.start()
    app=QtWidgets.QApplication(sys.argv)
    pencere=Pencere()

    pencere.listelebtn.clicked.connect(listele)
    pencere.baglanbtn.clicked.connect(lambda : baglan(pencere.dosya_transferi.isChecked(),pencere.ekran_paylasimi.isChecked()))
    pencere.kapatbtn.clicked.connect(kapat)
    

    if not app.exec():
        kapat()
