from threading import Thread,Lock
import socket
import os
from ui import MainWindow
from PyQt5 import QtWidgets
from dosya_transfer_arayüz import Dosya_Pencere
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
    

def show_list():
    client.soket.send("list".encode("utf-8"))
    client_addr_data=client.soket.recv(4096)
    client_addr_data=pickle.loads(client_addr_data)
    MainWindow.list.clear()
    for i in client_addr_data:
        MainWindow.list.addItem(str(i))
def exit():
    client.soket.send("remove".encode("utf-8"))
    client.soket.close()
    sys.exit()
def client_to_client():
    
    pass


if __name__ == "__main__":
    client=Client(host="127.0.0.1",port=3963)
    client.start()
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=MainWindow()
    MainWindow.show()
    MainWindow.listelebtn.clicked.connect(show_list)

    if not app.exec():
        exit()

