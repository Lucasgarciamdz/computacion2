import os
import multiprocessing
import threading


def recibir_y_enviar_texto():
    fifo_path = "./texto_spiderman"
    try:
        os.mkfifo(fifo_path)
    except FileExistsError:
        pass
    texto = str(input("Ingrese el texto a enviar: "))
    with os.fdopen(os.open(fifo_path, os.O_WRONLY), "w") as f:
        f.write(texto)

    spiderman_process = multiprocessing.Process(target=spiderman)
    spiderman_process.start()
    spiderman_process.join()


lock = multiprocessing.Lock()


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
    recibir_y_enviar_texto()
