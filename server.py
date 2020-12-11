import socket
from threading import Thread,Lock
import threading
import time
import os
import pickle
from PyQt5 import QtWidgets
import sys


soket_threads=[]
soket_addr=[]

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
            conn,addr=soket.accept()
            #print(conn)---->#soket bilgisini tutar
            #print(addr)---->#ip,raddr ikilisini tutar
            create_socket_thread=Soket(conn,self)
            create_socket_thread.start()
            soket_threads.append(create_socket_thread)#Bağlanan istemcileri tutar(tipi soket türündendir)
            soket_addr.append(addr)#Bağlanan istemcilerin ip,raddr ikilisini tutar.Her eleman bir tuple dır.

class Server_State(Thread):
    def __init__(self):
        super().__init__()
    def run(self):
        pass

       
class Soket(Thread):
    def __init__(self,conn,serverclass):
        super().__init__()
        self.conn=conn
        self.serverclass=serverclass
    def run(self):
        print("{} istemcisi için yeni bir thread oluşturuldu ve istekler dinlenmeye başladı".format(self.conn.getpeername()))
        a=Requests(self.conn,self)
        a.start()
        a.select()
   

class Requests(Thread):
    def __init__(self,conn,soket_thread):
         super().__init__()
         self.conn=conn
         self.lock=Lock()
         self.soket=soket_thread#sadece silme için ihtiyac duyduk
    def run(self):
        pass
    def select(self):
        try:
           while True:
                select=self.conn.recv(1024).decode("utf-8")
                if select=="list":
                    self.lock.acquire(blocking=True,timeout=-1)
                    os.system("cls")
                    print(soket_threads)
                    print(soket_addr)
                    soket_addr_data=pickle.dumps(soket_addr)
                    self.conn.send(soket_addr_data)
                    self.lock.release()
                elif select=="remove":
                    self.lock.acquire(blocking=True,timeout=-1)
                    soket_threads.remove(self.soket)
                    soket_addr.remove(self.conn.getpeername())
                    self.lock.release()
                elif select=="connect":
                    self.lock.acquire(blocking=True,timeout=-1)
                    data=self.conn.recv(2048).decode("utf-8")
                    while data=="connect":
                        data=self.conn.recv(2048).decode("utf-8")
                    self.conn.send(data.encode("utf-8"))
                    time.sleep(1)
                    self.conn.send(data.encode("utf-8"))
                    time.sleep(1)
                    self.conn.send(data.encode("utf-8"))
                    time.sleep(1)
                    self.conn.send("s".encode("utf-8"))
                    self.lock.release()
        except ConnectionResetError:
            soket_threads.remove(self.soket)
            soket_addr.remove(self.conn.getpeername())
            
    def file_receive(self):
        pass
    def file_send(self):
        pass


if __name__ == "__main__":
    server=Server(host="127.0.0.1",port=3963)
    server.start() 