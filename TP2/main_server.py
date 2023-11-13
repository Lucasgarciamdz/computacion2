import argparse
import logging
import socket
import multiprocessing as mp
from image_proccessing import black_and_white
import asyncio
from iterm2_tools import images


def process_image(image_url, conn):
    logging.info('Processing image')
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(black_and_white(image_url))
    logging.info('Image processing finished')
    conn.send(result)
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="main server")
    parser.add_argument("-p", "--port", type=int, default=8080, help="port")
    parser.add_argument("-i", "--ip", type=str, default="localhost", help="ip")
    parser.add_argument("-im", "--image", type=str, default="./test.jpeg", help="image")
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
            try:
                images.display_image_file(args.image)
            except Exception as e:
                logging.error(f"Error displaying image: {e}")
            conn.send("Processing your image".encode())
            parent_conn, child_conn = mp.Pipe()
            son = mp.Process(target=process_image, args=(args.image, child_conn))
            son.start()
            image_bw, image_path = parent_conn.recv()
            try:
                images.display_image_file(image_bw)
            except Exception as e:
                logging.error(f"Error displaying image: {e}")
            son.join()
            conn.send("Image processing finished".encode())
            conn.send(image_path.encode())
        except Exception as e:
            logging.error(f"Error processing image: {e}")
            conn.send(f"Error processing image: {e}".encode())
        finally:
            conn.close()


if __name__ == '__main__':
    main()
