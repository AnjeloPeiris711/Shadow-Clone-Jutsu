import dns.message
import dns.query
import dns.resolver
import dns.zone
import socketserver
import threading

# Create a dictionary to store domain name to IP address mappings
dns_data = {
    b'junior.home.': '127.0.0.1',
}

class DNSHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        socket = self.request[1]
        query = dns.message.from_wire(data)

        reply = dns.message.make_response(query)
        question = query.question[0]
        domain = question.name.to_text()

        if domain in dns_data:
            ip_address = dns_data[domain]
            reply.answer.append(dns.rrset.from_text(domain, 300, dns.rdataclass.IN, dns.rdatatype.A, ip_address))
        else:
            resolver = dns.resolver.Resolver()
            answer = resolver.resolve(domain, 'A')
            for rr in answer.rrset:
                reply.answer.append(rr)

        socket.sendto(reply.to_wire(), self.client_address)

if __name__ == '__main__':
    server = socketserver.ThreadingUDPServer(('0.0.0.0', 53), DNSHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()
    server_thread.join()
