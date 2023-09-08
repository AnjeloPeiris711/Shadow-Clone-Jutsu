# import dns.message
# import dns.query
# import dns.resolver
# import dns.zone
# import socketserver
# import threading

# # Create a dictionary to store domain name to IP address mappings
# dns_data = {
#     b'junior.home.': '127.0.0.1',
# }

# class DNSHandler(socketserver.BaseRequestHandler):
#     def handle(self):
#         data = self.request[0]
#         socket = self.request[1]
#         query = dns.message.from_wire(data)

#         reply = dns.message.make_response(query)
#         question = query.question[0]
#         domain = question.name.to_text()

#         if domain in dns_data:
#             ip_address = dns_data[domain]
#             reply.answer.append(dns.rrset.from_text(domain, 300, dns.rdataclass.IN, dns.rdatatype.A, ip_address))
#         else:
#             resolver = dns.resolver.Resolver()
#             answer = resolver.resolve(domain, 'A')
#             for rr in answer.rrset:
#                 reply.answer.append(rr)

#         socket.sendto(reply.to_wire(), self.client_address)

# if __name__ == '__main__':
#     server = socketserver.ThreadingUDPServer(('0.0.0.0', 53), DNSHandler)
#     server_thread = threading.Thread(target=server.serve_forever)
#     server_thread.start()
#     server_thread.join()

from dnslib import *
from socketserver import UDPServer, BaseRequestHandler

# Define the domain name and its corresponding IP address
domain_name = "junior.home."
ip_address = "127.0.0.1"

class DNSHandler(BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        dns_request = DNSRecord.parse(data)
        reply = DNSRecord(DNSHeader(id=dns_request.header.id, qr=1, aa=1, ra=1),
                          q=dns_request.q)

        if dns_request.q.qname == domain_name:
            reply.add_answer(RR(rname=dns_request.q.qname, rtype=QTYPE.A,
                                 rclass=1, ttl=60, rdata=A(ip_address)))

        self.request[1].sendto(reply.pack(), self.client_address)

if __name__ == "__main__":
    with UDPServer(("192.168.1.3", 53), DNSHandler) as server:
        server.serve_forever()




