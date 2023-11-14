import argparse
import logging
import socket
import multiprocessing as mp
from image_proccessing import black_and_white
import asyncio
import os


def process_image(image_url, conn):
    logging.info('Processing image')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(black_and_white(image_url))
    logging.info('Image processing finished')
    conn.send(result)
    conn.close()


def send_image(conn, image_path):
    if os.path.isfile(image_path):
        with open(image_path, 'rb') as img:
            while True:
                data = img.read(1024)
                if not data:
                    break
                conn.sendall(data)
    else:
        logging.error(f"Image not found: {image_path}")


def main():
    parser = argparse.ArgumentParser(description="main server")
    parser.add_argument("-p", "--port", type=int, default=8080, help="port")
    parser.add_argument("-i", "--ip", type=str, default="localhost", help="ip")
    parser.add_argument("-im", "--image", type=str, default="./test.jpeg", help="image")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)

    server_family = socket.AF_INET6 if ":" in args.ip else socket.AF_INET
    server_socket = socket.socket(server_family, socket.SOCK_STREAM)

    server_socket.bind((args.ip, args.port))
    server_socket.listen(1)

    logging.info(f"Listening on {args.ip}:{args.port}")

    while True:
        logging.info("Waiting for connection")
        client_socket, addr = server_socket.accept()
        logging.info(f"Connection from {addr}")

        client_socket.send("Connected".encode())

        try:
            client_socket.send("\nProcessing your image".encode())
            parent_conn, child_conn = mp.Pipe()
            son = mp.Process(target=process_image, args=(args.image, child_conn))
            son.start()
            image_path = parent_conn.recv()
            son.join()
            client_socket.send("\nImage processing finished\n".encode())
            send_image(client_socket, image_path)
        except Exception as e:
            logging.error(f"Error processing image: {e}")
            client_socket.send(f"Error processing image: {e}".encode())
        finally:
            client_socket.close()


if __name__ == '__main__':
    main()
