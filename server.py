import socket
from threading import Thread,Lock
import threading
import time
import os
import pickle
from PyQt5 import QtWidgets


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


def send_client_list(source_client,req_thread):
        req_thread.lock.acquire(blocking=True,timeout=-1)
        os.system("cls")
        print(soket_threads)
        print(soket_addr)
        soket_addr_data=pickle.dumps(soket_addr)
        source_client.send(soket_addr_data)
        req_thread.lock.release()

def remove_client(source_client,req_thread):
        req_thread.lock.acquire(blocking=True,timeout=-1)
        soket_threads.remove(source_client)
        soket_addr.remove(source_client.conn.getpeername())
        req_thread.lock.release()

def file_transfer(source_client,req_thread):
        req_thread.lock.acquire(blocking=True,timeout=-1)
        gelen_data=source_client.recv(1024).decode("utf-8")
        print(gelen_data)
        req_thread.lock.release()
       
       
        
        
class Soket(Thread):
    def __init__(self,conn,serverclass):
        super().__init__()
        self.conn=conn
        self.serverclass=serverclass
    def run(self):
        print("{} istemcisi için yeni bir thread oluşturuldu ve istekler dinlenmeye başladı".format(self.conn.getpeername()))
        a=Requests(self.conn,self.serverclass,self)
        a.start()
        a.select()
        

class Requests(Thread):
    def __init__(self,conn,serverclass,soket_thread):
         super().__init__()
         self.conn=conn
         self.lock=Lock()
         self.soket=soket_thread#sadece silme için ihtiyac duyduk
    def run(self):
        pass
    def select(self):
       while True:
           select=self.conn.recv(1024).decode("utf-8")
           if select=="list":
               send_client_list(self.conn,self)
           elif select=="remove":
               remove_client(self.soket,self)
           elif select=="connect":
               file_transfer(self.conn,self)





                

if __name__ == "__main__":
    server=Server(host="127.0.0.1",port=3963)
    server.start()