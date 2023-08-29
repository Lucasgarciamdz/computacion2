import socket
import threading as th
import sys


def thread_client(client):
    # Start child process
    print("Child process started...")

    thread_conn, thread_addr = client

    while True:
        data = thread_conn.recv(1024)
        if data == b"chau":
            # Close connection
            print(f"Connection closed by {thread_addr}")
            goodbye = "Goodbye! See you soon!"
            thread_conn.send(goodbye.encode("ascii"))
            break
        print(f"Received data from {thread_addr}: {data.decode('utf-8')}")
        response = f"Received your message! \r\n {data.decode('utf-8').upper()}"
        thread_conn.send(response.encode("ascii"))


def main():
    # Create server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Set port
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 50050
    print("Waiting for connections...")

    # Bind server socket
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(5)

    threads = []
    # Accept client connections
    while True:
        client = server_socket.accept()
        connection, address = client
        print(f"New connection from {address}")

        # Send welcome message
        welcome = "Welcome to the server! Thank you for connecting" + "\r\n"
        connection.send(welcome.encode("ascii"))

        # Start child process
        t = th.Thread(target=thread_client, args=(client,))
        threads.append(t)
        t.start()

        for t in threads:
            t.join()


if __name__ == "__main__":
    main()
