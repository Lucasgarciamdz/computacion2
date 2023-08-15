import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(("0.0.0.0", 50011))

s.listen(5)

conn, addr = s.accept()


if __name__ == "__main__":
    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("Recibido:", data.decode())
        conn.send(data)
    conn.close()
    s.close()
