import socket
import sys
import signal
import glob

class Zones:
    def __init__(self):
        self.zonefiles = glob.glob('zones/*.zone')
    def getzone(self,zdomain):
        print(self.zonefiles)
class Communication: 
    def __init__(self):
        self.TID = ""
        self.rflag = ""
        self.QR = "1"
        self.OPCODE = ""
        self.AA = "1"
        self.TC = "0"
        self.RD = "0"
        self.RA = "0"
        self.Z ="000"
        self.RCODE = "0000"
        self.state = 0
        self.domainstring = ""
        self.domainparts = []
        self.x = 0
        self.y =0
        self.qt = ''
    def getflags(self,flags):
        byte1 = bytes(flags[:1])
        byte2 = bytes(flags[1:2])
        for bit in range(1,5):
            self.OPCODE += str(ord(byte1)&(1<<bit))
        return int(self.QR+self.OPCODE+self.AA+self.TC+self.RD, 2).to_bytes(1,byteorder='big')+int(self.RA+self.Z+self.RCODE, 2).to_bytes(1,byteorder='big')
    def getquestiondomain(self,qdata):
        for byte in qdata:
            if self.state == 1:
                self.domainstring += chr(byte)
                self.x +=1
                if self.x == expectedlength:
                    self.domainparts.append(self.domainstring)
                    self.domainstring =""
                    self.state = 0
                    self.x = 0
                if byte ==0:
                    self.domainparts.append(self.domainstring)
                    break
            else:
                self.state = 1
                expectedlength = byte
            self.x += 1
            self.y += 1

        questiontype = qdata[self.y+1:self.y+3]
        return(self.domainparts,questiontype)
    def getrecs(self,tdata):
        domain,tqectiontype = self.getquestiondomain(tdata)
        if tqectiontype == b'\x00\x01':
            self.qt = 'a'
        zone = zon.getzone(domain)
    def buildresponse(self,data):
        # TransactionId
        TransactionId = data[:2]
        for byte in TransactionId:
            self.TID += hex(byte)[2:]
            #print(hex(byte))

        #Get the Flag
        Flags = self.getflags(data[2:4])
        #Question Count
        QDCOUNT = b'\x00\x01'
        #Answer Count
        #self.getquestiondomain(data[12:])
        self.getrecs(data[12:])
    def getrequest(self,data):
        print(data)
class Server:
    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.server_socket = None
    def start_server(self):
        # Create a socket object
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Bind the socket to a specific host and port
        self.server_socket.bind((self.host, self.port))
        print(f"Server started on {self.host}:{self.port}")
        # Accept a connection from a client
        while True:
            data,addr = self.server_socket.recvfrom(512)
            if not data:
                break
            else:
                com.buildresponse(data)
            #com.getrequest(data)
            # r = buildresponse(data)
            # print(data)
            #server_socket.sendto(b'Hello World',addr)
            #server_socket.sendto(r,addr)
            # # Clean up resources
    def shutdown_handler(self):
        if self.server_socket:
            self.server_socket.close()
            print("Server stopped.")
        sys.exit(0)

com = Communication()
zon = Zones()
sev = Server('localhost',53)
# Usage
sev.start_server()
# sev.server_socket.close()
# sys.exit(0)
