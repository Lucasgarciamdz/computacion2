import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("0.0.0.0", 50011))
s.listen(1)

while True:
    conn, addr = s.accept()
    print(f"New connection from {addr}")

    while True:
        data = conn.recv(1024)
        if data == b"chau":
            print(f"Connection closed by {addr}")
            conn.close()
            break
        print(f"Received data from {addr}: {data}")
