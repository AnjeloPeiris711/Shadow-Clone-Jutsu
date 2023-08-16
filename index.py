import socket
import sys
import signal
import glob
import json

class Zones:
    
    def __init__(self):
        self.jsonzone = {}
        self.zonefiles = glob.glob('zones/*.zone')
        self.zonedata = None

    def load_zones(self):
        for zone in self.zonefiles:
            with open(zone) as self.zonedata:
                zdata = json.load(self.zonedata)
                zonename = zdata["$origin"]
                self.jsonzone[zonename] = zdata
        return self.jsonzone
    
    def getzone(self,zdomain):
        zonedata = self.load_zones()
        zone_name = '.'.join(zdomain)
        return zonedata[zone_name]
    
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
        self.expectedlength = 0
        self.x = 0
        self.y =0
        self.qt = ''
        self.dnsbody =b''
        self.qbytes = b''
    def getflags(self,flags):
        byte1 = bytes(flags[:1])
        byte2 = bytes(flags[1:2])
        for bit in range(1,5):
            self.OPCODE += str(ord(byte1)&(1<<bit))
        return int(self.QR+self.OPCODE+self.AA+self.TC+self.RD, 2).to_bytes(1,byteorder='big')+int(self.RA+self.Z+self.RCODE, 2).to_bytes(1,byteorder='big')
    
    def getquestiondomain(self,qdata):
        for byte in qdata:
            if self.state == 1:
                if byte != 0:
                    self.domainstring += chr(byte)
                self.x +=1
                if self.x == self.expectedlength:
                    self.domainparts.append(self.domainstring)
                    self.domainstring =""
                    self.state = 0
                    self.x = 0
                if byte ==0:
                    self.domainparts.append(self.domainstring)
                    break
            else:
                self.state = 1
                self.expectedlength = byte
            #self.x += 1
            self.y += 1

        questiontype = qdata[self.y:self.y+2]
        return(self.domainparts,questiontype)
    def buildquestion(self,bdomainname,brectype):
        for part in bdomainname:
            length = len(part)
            self.qbytes += bytes([length])
            for char in part:
                self.qbytes += ord(char).to_bytes(1, byteorder='big')
        if brectype == 'a':
            self.qbytes += (1).to_bytes(2, byteorder='big')

        self.qbytes += (1).to_bytes(2, byteorder='big')

        return self.qbytes

    # if rectype == 'a':
    #     qbytes += (1).to_bytes(2, byteorder='big')

    # qbytes += (1).to_bytes(2, byteorder='big')

    # return qbytes

    def getrecs(self,tdata):
        domain,tqectiontype = self.getquestiondomain(tdata)
        if tqectiontype == b'\x00\x01':
            self.qt = 'a'
        zone = zon.getzone(domain)
        # return(zone[self.qt],self.qt,domain)
        if self.qt in zone:
            value = zone[self.qt]
            return (value, self.qt, domain)
        else:
            return("error")
    
    def buildresponse(self,data):
        # TransactionId
        TransactionId = data[:2]
        # for byte in TransactionId:
        #     self.TID += hex(byte)[2:]
        #     #print(hex(byte))

        #Get the Flag
        Flags = self.getflags(data[2:4])
        #Question Count
        QDCOUNT = b'\x00\x01'
        #Answer Count
        #self.getquestiondomain(data[12:])
        ANCOUNT = len(self.getrecs(data[12:])[0]).to_bytes(2,byteorder='big')
        #Nameserver Count
        NSCOUNT = (0).to_bytes(2,byteorder='big')
        #Additional Count
        ARCOUNT = (0).to_bytes(2,byteorder='big')
        dnsheader = TransactionId+Flags+QDCOUNT+ANCOUNT+NSCOUNT+ARCOUNT
        records,rectype,domainname = self.getrecs(data[12:])
        dnsqustion = self.buildquestion(domainname,rectype)
    def getrequest(self,data):
        # print(data)
        pass

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
