# Shadow-Clone-Jutsu
<<<<<<< HEAD

## DNS Step 1
``` python
import socket

def start_server(host, port):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to a specific host and port
    server_socket.bind((host, port))

    print(f"Server started on {host}:{port}")

    while True:
        # Accept a connection from a client
        data,addr = server_socket.recvfrom(512)
        print(data)
# Usage
start_server('localhost', 53)

```
### Usage
```
C:\Users\asus>dig howcode.org @127.0.0.1

```

```
Shadow-Clone-Jutsu>Python ./index.py
Server started on localhost:53
b'\xa2\x90\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x07howcode\x03org\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x0c\x00\n\x00\x08\xb4!\xdb\x01 -7\xa7'
b'\xa2\x90\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x07howcode\x03org\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x0c\x00\n\x00\x08\xb4!\xdb\x01 -7\xa7'
b'\xa2\x90\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x07howcode\x03org\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x0c\x00\n\x00\x08\xb4!\xdb\x01 -7\xa7'
```
=======
try to create lord balancer in browser 

## Can I load balance with javascript ?
Client-side Load Balancing: You can use JavaScript to distribute client requests across multiple backend servers. In this approach, the JavaScript code can be responsible for choosing a server from a predefined list of available servers or by using other criteria to direct the client's request.

## Can i use Browser as Backend Server?
>>>>>>> 964a0b6589b420ce563a04cbade023f2dcb82d62
