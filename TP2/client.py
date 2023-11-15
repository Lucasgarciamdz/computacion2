import requests
import logging
import subprocess
import platform
import os

logging.basicConfig(level=logging.INFO)


def open_image(image_path):
    if platform.system() == 'Darwin':       # macOS
        subprocess.call(('open', image_path))
    elif platform.system() == 'Windows':    # Windows
        os.startfile(image_path)
    else:                                   # linux variants
        subprocess.call(('xdg-open', image_path))


def ipv4_client():
    logging.info('Starting IPv4 client')
    server_address = '127.0.0.1'
    server_port = 8080

    with open('./test.jpeg', 'rb') as img:
        img_data = img.read()

    logging.info('\nSending POST request to IPv4 server')
    response = requests.post(f'http://{server_address}:{server_port}', data=img_data)

    if response.status_code == 200:
        image_path = 'processed_image_ipv4.jpeg'
        with open(image_path, 'wb') as img:
            img.write(response.content)
        logging.info('\nReceived processed image from IPv4 server\n\n')
        open_image(image_path)
    else:
        logging.error(f"IPv4 Error: {response.status_code}, {response.text}")


def ipv6_client():
    logging.info('Starting IPv6 client')
    server_address = '[::1]'
    server_port = 8080

    with open('./test.jpeg', 'rb') as img:
        img_data = img.read()

    logging.info('\nSending POST request to IPv6 server')
    response = requests.post(f'http://{server_address}:{server_port}', data=img_data)

    if response.status_code == 200:
        image_path = 'processed_image_ipv6.jpeg'
        with open(image_path, 'wb') as img:
            img.write(response.content)
        logging.info('\nReceived processed image from IPv6 server\n\n')
        open_image(image_path)
    else:
        logging.error(f"IPv6 Error: {response.status_code}, {response.text}")


def main():
    ipv4_client()
    ipv6_client()


if __name__ == '__main__':
    main()
