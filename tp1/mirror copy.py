import os
import argparse


def mirror_text(f):
    hijo_read, padre_write = os.pipe()
    padre_read, hijo_write = os.pipe()

    # try:
    #     parser = argparse.ArgumentParser()
    #     parser.add_argument("-f", help="ruta al archivo para ser espejado")
    #     args = parser.parse_args()
    #     if args.f is None:
    #         raise ValueError("Error: ingrese una ruta valida")
    # except Exception as e:
    #     print(e)
    #     return

    archivo_original = open(f, "r")
    lineas = archivo_original.readlines()
    archivo_original.close()

    for linea in lineas:
        os.write(padre_write, linea.encode())
    largo_lineas_espejadas = []
    for i in range(len(lineas)):
        largo_linea = len(lineas[i].encode())
        linea = os.read(hijo_read, largo_linea - 1).decode()
        os.read(hijo_read, 1).decode()
        linea = linea + "   |   " + linea[::-1] + "\n"
        os.write(hijo_write, linea.encode())
        largo_lineas_espejadas.append(len(linea.encode()))

    for i in range(len(lineas)):
        linea = os.read(padre_read, largo_lineas_espejadas[i]).decode()
        print(linea)

    os.close(hijo_read)
    os.close(hijo_write)
    os.close(padre_read)
    os.close(padre_write)


mirror_text("/Users/mymac/Documents/itc_soluciones/computacion2/sample_text.txt")
