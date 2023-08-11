import socket
import sys
import signal

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
    def getflags(self,flags):
        byte1 = bytes(flags[:1])
        byte2 = bytes(flags[1:2])
        for bit in range(1,5):
            self.OPCODE += str(ord(byte1)&(1<<bit))
        return int(self.QR+self.OPCODE+self.AA+self.TC+self.RD, 2).to_bytes(1,byteorder='big')+int(self.RA+self.Z+self.RCODE, 2).to_bytes(1,byteorder='big')
    def buildresponse(self,data):
        # TransactionId
        TransactionId = data[:2]
        for byte in TransactionId:
            self.TID += hex(byte)[2:]
            #print(hex(byte))

        #Get the Flag
        Flags = self.getflags(data[2:4])
        print(Flags)
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
sev = Server('localhost',53)
# Usage
sev.start_server()
# sev.server_socket.close()
# sys.exit(0)
