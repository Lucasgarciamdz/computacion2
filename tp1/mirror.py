import os
import argparse
import time


def mirror_text():
    hijo_read, padre_write = os.pipe()
    padre_read, hijo_write = os.pipe()

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="ruta al archivo para ser espejado", type=str, required=True)
    args = parser.parse_args()

    if not os.path.exists(args.f) or not os.access(args.f, os.R_OK):
        raise FileNotFoundError(f"No se pudo abrir el archivo: {args.f}")

    with open(args.f, "r") as archivo_original:
        lineas = archivo_original.readlines()

    largo_linea = []
    for linea in lineas:
        largo_linea.append(len(linea.encode()))
        os.write(padre_write, linea.encode())

    for i in largo_linea:
        rt = os.fork()
        if rt > 0:
            time.sleep(0.5)
            continue
        if rt == 0:
            linea = os.read(hijo_read, i - 1).decode()
            os.read(hijo_read, 1)
            linea = linea + "   |   " + linea[::-1] + "\n"
            os.write(hijo_write, linea.encode())
            exit()

    linea = os.read(padre_read, 2024).decode()
    print(linea)

    os.close(hijo_read)
    os.close(hijo_write)
    os.close(padre_read)
    os.close(padre_write)


if __name__ == "__main__":
    mirror_text()
