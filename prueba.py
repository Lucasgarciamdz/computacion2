# Importing the modules
import os
import argparse
import time

# Defining a function to mirror the text in a file
def mirror_text():
    # Creating two pipes for communication between parent and child processes
    hijo_read, padre_write = os.pipe()
    padre_read, hijo_write = os.pipe()

    # Parsing the command line argument for the file path
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", help="ruta al archivo para ser espejado", type=str, required=True)
    args = parser.parse_args()

    # Checking if the file path is valid and readable
    if not os.access(args.f, os.R_OK):
        print(f"No se puede acceder al archivo {args.f}")
        exit(1)

    # Reading the lines from the file and storing them in a list
    try:
        with open(args.f, "r") as archivo_original:
            lineas = archivo_original.readlines()
    except (PermissionError, IOError) as e:
        print(f"Error al abrir el archivo: {e}")
        exit(1)

    # Writing the lines to the parent's write end of the pipe
    for linea in lineas:
        os.write(padre_write, linea.encode())

    # Creating a child process for each line to mirror it and write it to the child's write end of the pipe
    for _ in range(len(lineas)):
        rt = os.fork()
        if rt > 0:
            # Parent process waits for a short time and continues to create more child processes
            time.sleep(0.5)
            continue
        if rt == 0:
            # Child process reads a line from the parent's read end of the pipe and reverses it
            linea = os.read(hijo_read, 2024).decode().strip()
            linea = linea + "   |   " + linea[::-1] + "\n"
            # Child process writes the mirrored line to the child's write end of the pipe and exits
            os.write(hijo_write, linea.encode())
            exit()

    # Parent process waits for all child processes to finish
    for _ in range(len(lineas)):
        os.wait()

    # Parent process reads the mirrored lines from the child's read end of the pipe and prints them
    linea = os.read(padre_read, 2024).decode()
    print(linea)

    # Closing all the pipe ends
    os.close(hijo_read)
    os.close(hijo_write)
    os.close(padre_read)
    os.close(padre_write)

# Calling the function when the script is executed
if __name__ == "__main__":
    mirror_text()
