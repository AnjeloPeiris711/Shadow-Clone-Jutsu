import socket

def start_server(host, port):
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific host and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)

    print(f"Server started on {host}:{port}")

    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()
        print(f"New connection from {client_address[0]}:{client_address[1]}")

        # Process the client's request
        # ...

        # Send a response back to the client
        response = "Hello, client!"
        client_socket.send(response.encode())

        # Close the client socket
        client_socket.close()

    # Close the server socket
    server_socket.close()

# Usage
start_server('localhost', 8080)

