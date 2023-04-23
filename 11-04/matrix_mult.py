import os

matrix1 = [[1, 2], [4, 5]]
matrix2 = [[7, 3], [4, 8]]


def matrix_mult(matrix1, matrix2):
    fifo_path = "./pipe2"
    os.mkfifo(fifo_path)
    cells = []
    for i in range(2):
        for j in range(2):
            pid = os.fork()
            if pid == 0:
                cell = 0
                for k in range(2):
                    cell += matrix1[i][k] * matrix2[k][j]
                with os.fdopen(fifo_path, os.O_WRONLY) as f:
                    f.write(str(cell))
                f.close()
                os._exit(0)
    with os.fdopen(fifo_path, os.O_WRONLY) as f:
        for _ in range(4):
            cells.append(int(f.readline()))

    result = [[cells[0], cells[1]], [cells[2], cells[3]]]
    return result


result = matrix_mult(matrix1, matrix2)
print(result)
