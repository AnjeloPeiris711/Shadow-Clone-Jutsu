# import socket
# import dns.message
# import dns.rdataclass
# import dns.rdatatype
# import requests

# # DNS mappings (for demonstration purposes)
# dns_mappings = {
#     "example.com.": "192.168.1.1",
#     # Add more mappings here
# }

# def resolve_domain(query_domain):
#     if query_domain in dns_mappings:
#         return dns_mappings[query_domain]
#     return None

# def dns_server():
#     udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     udp_socket.bind(("127.0.0.1", 53))

#     while True:
#         data, addr = udp_socket.recvfrom(1024)
#         query = dns.message.from_wire(data)
        
#         if query.question:
#             qname = query.question[0].name.to_text()
#             resolved_ip = resolve_domain(qname)
            
#             if resolved_ip:
#                 response = dns.message.make_response(query)
#                 response.answer.append(
#                     dns.rrset.from_text(qname, dns.rdataclass.IN, dns.rdatatype.A, resolved_ip)
#                 )
#                 udp_socket.sendto(response.to_wire(), addr)

#                 # Fetch and display webpage
#                 webpage = requests.get(f"http://{resolved_ip}")
#                 print(webpage.text)
#             else:
#                 print("Domain not found")

# if __name__ == "__main__":
#     dns_server()
import socketserver
import dns.message
import dns.rdata
import dns.rdatatype

class MyDNSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        socket = self.request[1]

        query = dns.message.from_wire(data)

        domain = query.question[0].name.to_text()
        ip_address = "192.168.1.100"  # Replace with your desired IP address

        response = dns.message.Message(query.id)
        response.question = query.question

        answer = dns.rdata.from_text(dns.rdataclass.IN, dns.rdatatype.A, ip_address)
        response.answer.append(dns.rrset.from_text(domain, 300, dns.rdataclass.IN, dns.rdatatype.A, answer))

        socket.sendto(response.to_wire(), self.client_address)

if __name__ == "__main__":
    server = socketserver.UDPServer(('127.0.0.1', 53), MyDNSHandler)
    server.serve_forever()

