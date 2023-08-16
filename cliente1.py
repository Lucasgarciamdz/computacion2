import socket


def iniciar_cliente():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("0.0.0.0", 50011))
        while True:
            data = input("Ingrese un mensaje: ")
            s.send(data.encode())
            if data == "chau":
                break


if __name__ == "__main__":
    iniciar_cliente()
