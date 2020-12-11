from threading import Thread,Lock
import socket
import os
from client_ui import MainWindow
from PyQt5 import QtWidgets
from file_transfer_ui import Dosya_Pencere
import sys
import pickle
import time 
conn_list=[]
class Client(Thread):

    def __init__(self,host,port):
        super().__init__()
        self.host=host
        self.port=port
        self.soket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def run(self):
        self.soket.connect((self.host,self.port))

class Receive(Thread):
    def __init__(self,client):
        super().__init__()
        self.soket=client
        self.lock=Lock()
        self.deger=""
    def run(self):
        self.deger=self.soket.recv(1024).decode("utf-8")
        while self.deger:   
            if self.deger!="s":
                print("thread aktif ve çalışıyor")
                print("data var")
                print(self.deger)
                self.deger=self.soket.recv(1024).decode("utf-8")
            else:
                self.lock.acquire(blocking=True,timeout=-1)
                
            

                    
def show_list():
    client.soket.send("list".encode("utf-8"))
    client_addr_data=client.soket.recv(4096)
    client_addr_data=pickle.loads(client_addr_data)
    MainWindow.list.clear()
    conn_list.clear()
    for i in client_addr_data:
        MainWindow.list.addItem(str(i))
        conn_list.append(i)
def exit():
    client.soket.send("remove".encode("utf-8"))
    client.soket.close()
    conn_list.clear()
    sys.exit()
def connect(target_client,radio1,radio2):
    try:
        
        if radio1:
           print("Zazaza")
        elif radio2:
            #conn_list tuple olarak ip,raddr bilgisi tutulur
            client.soket.send("connect".encode("utf-8"))
            client.soket.send(target_client.text().encode("utf-8"))
            t=Receive(client.soket)
            if not t.is_alive():
                t.start()
            else:
                t.run()
    except AttributeError:
        print("İstemci seçilmedi")

                
        

if __name__ == "__main__":
    client=Client(host="127.0.0.1",port=3963)
    client.start()
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=MainWindow()
    MainWindow.show()
    MainWindow.listelebtn.clicked.connect(show_list)
    MainWindow.baglanbtn.clicked.connect(lambda : connect(MainWindow.list.currentItem(),MainWindow.remote_pc.isChecked(),MainWindow.file_transfer.isChecked()))
    
    if not app.exec():
        exit()

