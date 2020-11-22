from threading import Thread
import socket
import os
from ui import arayüz2
from PyQt5 import QtWidgets
from dosya_transfer_arayüz import Dosya_Pencere
import sys
import pickle
import time

buffer_size=4096

class Client(Thread):
    def __init__(self,host,port):
        super().__init__()
        self.host=host
        self.port=port
        self.soket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def run(self):
        self.soket.connect((self.host,self.port))

def dosya_ekle():
        dosya_ismi=QtWidgets.QFileDialog.getOpenFileName(dosya_ekran,"Dosya Seç",os.getenv("HOME"))
        dosya_ekran.list.insertItem(dosya_ekran.i,dosya_ismi[0])
        dosya_ekran.i+=1

def dosya_gonder():
    try:
        with open(dosya_ekran.list.currentItem().text(),"rb") as file:
            print(len(file.read()))
    except AttributeError:
        print("Gönderilcek dosya yok")

def kapat():
    sock_create.soket.send("Sil".encode("utf-8"))
    sys.exit()
def listele():
    try:
        t=0
        sock_create.soket.send("Listele".encode("utf-8"))
        gelen_data=sock_create.soket.recv(4096)
        data=pickle.loads(gelen_data)
        pencere.list.clear()
        for i in data:
            pencere.list.insertItem(t,str(i))
            t+=1
            #print(tuple(i)[0])
            
    except:
        print("Server açık değil veya ulaşılamıyor")
def baglan(radio1,radio2):
    try:
        if radio1:
            
            sock_create.soket.send("Baglan".encode("utf-8"))
            print("Dosya Transferi seçildi")
            server_cevap=sock_create.soket.recv(2048).decode("utf-8")
            print(server_cevap)
            #pencere.setVisible(False)
            dosya_ekran.show()
            dosya_ekran.ekle.clicked.connect(dosya_ekle)
            dosya_ekran.gonder.clicked.connect(dosya_gonder)
            dosya_ekran.temizle.clicked.connect(lambda : dosya_ekran.list.clear())
        elif radio2:
            print("Ekran Paylaşımı seçildi")
        else:
            print("Seçim yapılmadı")
            pencere.isVisible=True
    except:
        print("Beklenmeyen hata")

def dosya_sec():
    dosya_ismi=QtWidgets.QFileDialog.getOpenFileName(pencere,"Dosya Seç",os.getenv("HOME"))
    return dosya_ismi

if __name__ == "__main__":
    sock_create=Client(host="127.0.0.1",port=3963)
    sock_create.start()
    app=QtWidgets.QApplication(sys.argv)
    pencere=arayüz2()
    dosya_ekran=Dosya_Pencere()
    
    pencere.listelebtn.clicked.connect(listele)
    pencere.baglanbtn.clicked.connect(lambda : baglan(pencere.file_transfer.isChecked(),pencere.remote_pc.isChecked()))
    
    if not app.exec():
        kapat()

