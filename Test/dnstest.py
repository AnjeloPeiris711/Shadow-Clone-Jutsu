# import socket, glob, json

# port = 53
# ip = '127.0.0.1'

# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# sock.bind((ip, port))


# while 1:
#     data, addr = sock.recvfrom(512)
#     print(data)

# import sys
# import socket

# __all__ = ['connect', 'get_data']

# # DNSQuery class from http://code.activestate.com/recipes/491264-mini-fake-dns-server/
# class DNSQuery:
#   def __init__(self, data):
#     self.data=data
#     self.domain=''

#     tipo = (ord(data[2]) >> 3) & 15   # Opcode bits
#     if tipo == 0:                     # Standard query
#       ini=12
#       lon=ord(data[ini])
#       while lon != 0:
#         self.domain+=data[ini+1:ini+lon+1]+'.'
#         ini+=lon+1
#         lon=ord(data[ini])

#   def response(self, ip, tld):
#     packet=''
#     if self.domain.endswith('.%s.'%tld):
#       packet+=self.data[:2] + "\x81\x80"
#       packet+=self.data[4:6] + self.data[4:6] + '\x00\x00\x00\x00'   # Questions and Answers Counts
#       packet+=self.data[12:]                                         # Original Domain Name Question
#       packet+='\xc0\x0c'                                             # Pointer to domain name
#       packet+='\x00\x01\x00\x01\x00\x00\x00\x3c\x00\x04'             # Response type, ttl and resource data length -> 4 bytes
#       packet+=str.join('',map(lambda x: chr(int(x)), ip.split('.'))) # 4bytes of IP
#     return packet


# def connect():
#   try:
#     udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udps.setblocking(False)
#     udps.bind(('',53))
#   except Exception as e:
#     print ("Failed to create socket on UDP port 53:", e)
#     sys.exit(1)
#   return udps


# def get_data(udps, tld, ip, verbose=False):
#   try:
#     data, addr = udps.recvfrom(1024)
#     p=DNSQuery(data)
#     r=p.response(ip, tld)
#     if r and verbose:
#       print ('DNS Request: %s -> %s' % (p.domain, ip))
#     udps.sendto(r, addr)
#   except socket.error:
#     pass


# def usage():
#   print ("")
#   print ("Usage:")
#   print ("")
#   print ("\t# devdns [tld] [ip]")
#   print ("")
#   print ("Description:")
#   print ("")
#   print ("\tMiniDNS will respond to all DNS queries with a single IPv4 address.")
#   print ("")
#   print ("\tYou may specify the tld for local development as the first argument on the command line:\n")
#   print ("\t\t# devdns test \n")
#   print ("\tIf no IP address is specified, 'dev' will be used.")
#   print ("")
#   print ("\tYou may specify the IP address to be returned as the second argument on the command line:\n")
#   print ("\t\t# devdns dev 1.2.3.4\n")
#   print ("\tIf no IP address is specified, 127.0.0.1 will be used.")
#   print ("")

#   sys.exit(1)


# if __name__ == '__main__':

#   tld = 'dev'
#   ip = '127.0.0.1'

#   if len(sys.argv) > 3 or '-h' in sys.argv or '--help' in sys.argv:
#     usage()
#   elif len(sys.argv) > 1:
#     tld = sys.argv[1]
#     if len(sys.argv) > 2:
#       ip = sys.argv[2]

#   udps = connect()

#   print ('devDNS :: *.%s. 60 IN A %s\n' % (tld, ip))
  
#   try:
#     while 1:
#       get_data(udps, tld, ip)
#   except KeyboardInterrupt:
#     print ('\nBye!')
#     udps.close()

import argparse
import datetime
import sys
import time
import threading
import traceback
import socketserver
import struct
try:
    from dnslib import *
except ImportError:
    print("Missing dependency dnslib: <https://pypi.python.org/pypi/dnslib>. Please install it with `pip`.")
    sys.exit(2)


class DomainName(str):
    def __getattr__(self, item):
        return DomainName(item + '.' + self)


D = DomainName('junior.home.')
IP = '127.0.0.1'
TTL = 60 * 5

soa_record = SOA(
    mname=D.ns1,  # primary name server
    rname=D.andrei,  # email of the domain administrator
    times=(
        201307231,  # serial number
        60 * 60 * 1,  # refresh
        60 * 60 * 3,  # retry
        60 * 60 * 24,  # expire
        60 * 60 * 1,  # minimum
    )
)
ns_records = [NS(D.ns1), NS(D.ns2)]
records = {
    D: [A(IP), AAAA((0,) * 16), MX(D.mail), soa_record] + ns_records,
    D.ns1: [A(IP)],  # MX and NS records must never point to a CNAME alias (RFC 2181 section 10.3)
    D.ns2: [A(IP)],
    D.mail: [A(IP)],
    D.andrei: [CNAME(D)],
}


def dns_response(data):
    request = DNSRecord.parse(data)

    print(request)

    reply = DNSRecord(DNSHeader(id=request.header.id, qr=1, aa=1, ra=1), q=request.q)

    qname = request.q.qname
    qn = str(qname)
    qtype = request.q.qtype
    qt = QTYPE[qtype]

    if qn == D or qn.endswith('.' + D):

        for name, rrs in records.items():
            if name == qn:
                for rdata in rrs:
                    rqt = rdata.__class__.__name__
                    if qt in ['*', rqt]:
                        reply.add_answer(RR(rname=qname, rtype=getattr(QTYPE, rqt), rclass=1, ttl=TTL, rdata=rdata))

        for rdata in ns_records:
            reply.add_ar(RR(rname=D, rtype=QTYPE.NS, rclass=1, ttl=TTL, rdata=rdata))

        reply.add_auth(RR(rname=D, rtype=QTYPE.SOA, rclass=1, ttl=TTL, rdata=soa_record))

    print("---- Reply:\n", reply)

    return reply.pack()


class BaseRequestHandler(socketserver.BaseRequestHandler):

    def get_data(self):
        raise NotImplementedError

    def send_data(self, data):
        raise NotImplementedError

    def handle(self):
        now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')
        print("\n\n%s request %s (%s %s):" % (self.__class__.__name__[:3], now, self.client_address[0],
                                               self.client_address[1]))
        try:
            data = self.get_data()
            print(len(data), data)  # repr(data).replace('\\x', '')[1:-1]
            self.send_data(dns_response(data))
        except Exception:
            traceback.print_exc(file=sys.stderr)


class TCPRequestHandler(BaseRequestHandler):

    def get_data(self):
        data = self.request.recv(8192).strip()
        sz = struct.unpack('>H', data[:2])[0]
        if sz < len(data) - 2:
            raise Exception("Wrong size of TCP packet")
        elif sz > len(data) - 2:
            raise Exception("Too big TCP packet")
        return data[2:]

    def send_data(self, data):
        sz = struct.pack('>H', len(data))
        return self.request.sendall(sz + data)


class UDPRequestHandler(BaseRequestHandler):

    def get_data(self):
        return self.request[0].strip()

    def send_data(self, data):
        return self.request[1].sendto(data, self.client_address)


def main():
    parser = argparse.ArgumentParser(description='Start a DNS implemented in Python.')
    parser = argparse.ArgumentParser(description='Start a DNS implemented in Python. Usually DNSs use UDP on port 53.')
    parser.add_argument('--port', default=5053, type=int, help='The port to listen on.')
    parser.add_argument('--tcp', action='store_true', help='Listen to TCP connections.')
    parser.add_argument('--udp', action='store_true', help='Listen to UDP datagrams.')
    
    args = parser.parse_args()
    if not (args.udp or args.tcp): parser.error("Please select at least one of --udp or --tcp.")

    print("Starting nameserver...")

    servers = []
    if args.udp: servers.append(socketserver.ThreadingUDPServer(('', args.port), UDPRequestHandler))
    if args.tcp: servers.append(socketserver.ThreadingTCPServer(('', args.port), TCPRequestHandler))

    for s in servers:
        thread = threading.Thread(target=s.serve_forever)  # that thread will start one more thread for each request
        thread.daemon = True  # exit the server thread when the main thread terminates
        thread.start()
        print("%s server loop running in thread: %s" % (s.RequestHandlerClass.__name__[:3], thread.name))

    try:
        while 1:
            time.sleep(1)
            sys.stderr.flush()
            sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        for s in servers:
            s.shutdown()

if __name__ == '__main__':
    main()