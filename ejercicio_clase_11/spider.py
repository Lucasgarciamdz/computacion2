import os
import threading

lock = threading.Lock()


def calcular_cant_caracteres(linea, numero_linea):
    with lock:
        print(f"{numero_linea} - La linea: {linea} tiene {len(linea)} caracteres")


def spiderman():
    fifo_path = "./texto_spiderman"
    with os.fdopen(os.open(fifo_path, os.O_RDONLY)) as f:
        lineas = f.readline()

    threads = []
    for i, linea in enumerate(lineas):
        t = threading.Thread(target=calcular_cant_caracteres, args=(linea, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


if __name__ == "__main__":
    spiderman()
