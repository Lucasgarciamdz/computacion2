import socket
import argparse


def receive_image(client_socket, image_path):
    with open(image_path, 'wb') as img:
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                img.write(data)
            except socket.error:
                break


def receive_message(client_socket):
    message = client_socket.recv(1024).decode()
    print(message)


def main():
    parser = argparse.ArgumentParser(description="Client")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Server port")
    parser.add_argument("-i", "--ip", type=str, default="localhost", help="Server IP")
    parser.add_argument("-im", "--image", type=str, default="./test.jpeg", help="Image path")
    args = parser.parse_args()

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((args.ip, args.port))
    receive_message(client_socket)  # Receive "Connected" message
    receive_message(client_socket)  # Receive "Processing your image" message
    receive_message(client_socket)  # Receive "Image processing finished" message
    receive_image(client_socket, args.image)
    client_socket.close()


if __name__ == '__main__':
    main()
