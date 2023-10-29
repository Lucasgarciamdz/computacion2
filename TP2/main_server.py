import argparse
import logging
import socket
import multiprocessing as mp
from image_processing import black_and_white


def process_image(image_url):
    logging.info('Processing image')
    black_and_white(image_url)
    logging.info('Image processing finished')


def main():
    parser = argparse.ArgumentParser(description="main server")
    parser.add_argument("-p", "--port", type=int, default=8080, help="port")
    parser.add_argument("-i", "--ip", type=str, default="localhost", help="ip")
    parser.add_argument("-im", "--image", type=str, default="test.jpg", help="image")
    parser.add_argument("-h", "--help", action="help", help="help")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

    server_socket.bind((args.ip, args.port))
    server_socket.listen(1)

    logging.info(f"Listening on {args.ip}:{args.port}")

    while True:
        logging.info("Waiting for connection")
        client_socket = server_socket.accept()
        conn, addr = client_socket
        logging.info(f"Connection from {conn}:{addr}")

        conn.send("Connected".encode())

        try:
            conn.send("Processing your image".encode())
            son = mp.Process(target=process_image, args=(args.image,))
            son.start()
            son.join()
            conn.send("Image processing finished".encode())
            with open(args.image, "rb") as f:
                while True:
                    data = f.read(1024)
                    if not data:
                        break
                    conn.send(data)
        except Exception as e:
            logging.error(f"Error processing image: {e}")
            conn.send(f"Error processing image: {e}".encode())
        finally:
            client_socket.close()


if __name__ == '__main__':
    main()
