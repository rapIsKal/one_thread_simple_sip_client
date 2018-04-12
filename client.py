import socket
from utils import *
import time
import select


class Client(object):
    def __init__(self, host, port, number, tcp=True):
        self.host = host
        self.port = port
        self.dataQueue = []
        self.name = None
        self.tcp = True
        self.number = number
        if tcp:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.sock.connect((host, port))
            print("connected to", host, port)
            self.sock.setblocking(0)
            self.name = self.sock.getsockname()
        else:
            self.tcp = False

    def form_message(self, name="REGISTER"):
        if name =="REGISTER":
            message = name + " sip:" + host + ":" + str(port) + " SIP/2.0\r\n"
            #TODO: how to generate tag? - rfc
            message += "From: <sip:"+str(self.number)+"@"+host+":" + str(port) +">;tag=73ADC2C5-7775-4998-A6CC-0928615C0FE9-1\r\n"
            message += "To: <sip:"+str(self.number)+"@"+ host+":"+str(port)+">\r\n"
            #TODO: how to generate call-id?- rfc
            message += "Call-ID: 5580B865-7C02-4A96-88BF-39DFCE11476D-1@"+ host +"\r\n"
            message += "CSeq: 1 REGISTER\r\n"
            message += "Content-Length: 0\r\n"
            #TODO: branch generation and udp/tcp handling
            message += "Via: SIP/2.0/UDP " + self.name[0] + ":" + str(self.name[1]) + \
                ";rport;branch=z9hG4bK323D384F-4520-47B0-A78E-A71D164E8614-1\r\n"
            message += "User-Agent: EpiPhone 8.5.000.72 vgorelov 12132\r\n"
            message += "Expires:3600\r\n"
            message += "Contact: <sip:"+str(self.number) + "@"+self.name[0]+":"+str(self.name[1])+">"+"\r\n"
        message += "\r\n"
        return message

    def expect(self, event):
        msg = self.dataQueue.pop(0)
        lines = msg.split("\r\n")
        if not event in lines[0]:
            raise BaseException("not the right event!")
        return msg


    def send(self, pack):
        if not self.tcp:
            self.sock.sendto(self.form_message(pack).encode(), (self.host, self.port))
        else:
            self.sock.send(self.form_message(pack).encode())
        ready = select.select([self.sock], [], [], 3)
        data =  None
        if ready[0]:
            data = self.sock.recv(1024)
            data = data.decode()
            for sip_msg in data.split("\r\n\r\n"):
                self.dataQueue.append(sip_msg)



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
    cl = Client(host, port, 8666)
    cl.send("REGISTER")
    cl.expect("200")
    cl.read()
    cl.read()
    cl.read()
    time.sleep(3)

