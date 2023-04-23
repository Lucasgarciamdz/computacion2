import os
import sys


def main():
    # Creamos un pipe
    r, w = os.pipe()

    # Creamos un proceso hijo
    pid = os.fork()
    if pid == 0:
        # Proceso hijo
        # Cerramos el descriptor de escritura del pipe
        os.close(w)
        # Leemos del pipe
        while True:
            line = os.read(r, 1024)
            if line == b'':
                break
            print("El proceso hijo recibió la línea: ", line)
            print("El proceso hijo encontró ", len(line.split()), " palabras.")
        # Cerramos el descriptor de lectura del pipe
        os.close(r)
    else:
        # Proceso padre
        # Cerramos el descriptor de lectura del pipe
        os.close(r)
        # Abrimos el archivo
        f = open(sys.argv[1], 'r')
        # Leemos el archivo línea a línea
        for line in f:
            # Escribimos en el pipe
            os.write(w, line.encode())
        # Cerramos el archivo
        f.close()
        # Cerramos el descriptor de escritura del pipe
        os.close(w)
