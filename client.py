import socket
from utils import *
import time
import select


class Client(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.dataQueue = []
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #this part is for only TCP usage only
        #self.sock.connect((host, port))
        #print("connected to", host, port)
        #self.sock.setblocking(0)
        #self.name = self.sock.getsockname()


    def send(self, pack):
        self.sock.sendto(pack.encode(), (self.host, self.port))
        ready = select.select([self.sock], [], [], 3)
        data =  None
        if ready[0]:
            data = self.sock.recv(1024)
        self.dataQueue.append(data)


    def read(self):
        pack_recv = None
        try:
            pack_recv = self.dataQueue.pop(0)
            print(pack_recv)
        except IndexError:
            pass

    def close(self):
        self.sock.close()


if __name__=="__main__":
    cl = Client(host, port)
    cl.send(register)
    time.sleep(3)

