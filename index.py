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

