import socket
import multiprocessing
import sys
import os


def connected_client(client):
    # Start child process
    print(f"Child process started...{os.getpid()}")

    child_conn, child_addr = client

    while True:
        data = child_conn.recv(1024)
        if data == b"chau":
            # Close connection
            print(f"Connection closed by {child_addr}")
            goodbye = "Goodbye! See you soon!"
            child_conn.send(goodbye.encode("ascii"))
            break
        print(f"Received data from {child_addr}: {data.decode('utf-8')}")
        response = f"Received your message! \r\n {data.decode('utf-8').upper()}"
        child_conn.send(response.encode("ascii"))


def main():
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Set port
    port = sys.argv[1] if len(sys.argv) > 1 else 50050
    print(f"Waiting for connections...{os.getpid()}")

    # Bind server socket
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)

    # Accept client connections
    while True:
        client = server_socket.accept()
        connection, address = client
        print(f"New connection from {address}")

        # Send welcome message
        welcome = "Welcome to the server! Thank you for connecting" + "\r\n"
        connection.send(welcome.encode("ascii"))

        # Start child process
        child = multiprocessing.Process(target=connected_client, args=(client,))
        child.start()


if __name__ == "__main__":
    main()
