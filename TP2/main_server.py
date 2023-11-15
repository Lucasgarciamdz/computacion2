from http.server import BaseHTTPRequestHandler, HTTPServer
import argparse
import logging
import numpy as np
import cv2
import time
import socket


def process_image(image_data):
    logging.debug('Starting image processing')
    time.sleep(5)
    logging.info('Processing image')
    image = cv2.imdecode(np.frombuffer(image_data, np.uint8), -1)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, img_encoded = cv2.imencode('.jpg', gray_image)
    logging.info('Image processing finished')
    logging.debug('Finished image processing')
    return img_encoded.tobytes()


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        logging.debug('Received POST request')
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            logging.info('Processing POST request')
            processed_image = process_image(post_data)
            self.send_response(200)
            self.send_header('Content-type', 'image/jpeg')
            self.end_headers()
            self.wfile.write(processed_image)
            logging.info('Finished processing POST request')
        except Exception as e:
            logging.error(f"Error processing image: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f"Error processing image: {e}".encode())


class DualStackServer(HTTPServer):
    address_family = socket.AF_INET6

    def server_bind(self):
        # TCP Dual Stack (IPv4/v6)
        # As per https://docs.python.org/2/library/socket.html#socket.socket.setsockopt
        self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        HTTPServer.server_bind(self)


def main():
    parser = argparse.ArgumentParser(description="main server")
    parser.add_argument("-p", "--port", type=int, default=8080, help="port")
    parser.add_argument("-i", "--ip", type=str, default="::", help="ip")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    server_address = (args.ip, args.port)
    logging.info(f"Starting server on {args.ip}:{args.port}")
    DualStackServer(server_address, RequestHandler).serve_forever()


if __name__ == '__main__':
    main()
