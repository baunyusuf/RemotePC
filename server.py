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
            #print(conn)---->#connection soketini tutar
            #print(addr)---->#ip,raddr ikilisini tutar
            create_socket_thread=Soket(conn,self)
            create_socket_thread.start()
            soket_threads.append(create_socket_thread)#Bağlanan istemcileri tutar(tipi soket türündendir)
            soket_addr.append(addr)#Bağlanan istemcilerin ip,raddr ikilisini tutar.
    def send_client_list(self,source_client):
        print(soket_threads)
        print(soket_addr)
        soket_addr_data=pickle.dumps(soket_addr)
        source_client.send(soket_addr_data)
    def remove_client(self,source_client,socket_thread):
        soket_threads.remove(socket_thread)
        soket_addr.remove(source_client.getpeername())
    def file_transfer(self):
        pass
        
        
class Soket(Thread):
    def __init__(self,conn,serverclass):
        super().__init__()
        self.conn=conn
        self.serverclass=serverclass
        self.lock=Lock()
    def run(self):
        while True:
            select=self.conn.recv(1024).decode("utf-8")
            if select=="list":
                self.lock.acquire(blocking=True,timeout=-1)
                self.serverclass.send_client_list(self.conn)
                self.lock.release()
            elif select=="remove":
                self.lock.acquire(blocking=True,timeout=-1)
                self.serverclass.remove_client(self.conn,self)
                self.lock.release()
            elif select=="connect":
                self.lock.acquire(blocking=True,timeout=-1)
                self.serverclass.file_transfer()
                self.lock.release()

if __name__ == "__main__":
    server=Server(host="127.0.0.1",port=3963)
    server.start()