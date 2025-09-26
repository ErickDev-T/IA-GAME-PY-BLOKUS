GRID_SIZE = 20

def make_board():
    board = []
    for i in range(20):     # repetir 20 veces las filas
        fila = []
        for j in range(20): # repetir 20 veces las columnas
            fila.append(-1) # agregar -1 en cada celda
        board.append(fila)
    return board
#manera resumida
#def make_board():
#    return [[-1 for _ in range(20)] for _ in range(20)]


b = make_board()
#print(len(b), len(b[0]))




def print_board(board):
    for fila in b:  # Recorre cada fila del tablero
        nueva_fila = []
        for celda in fila:  # Recorre cada número de la fila
            if celda == -1:
                nueva_fila.append(" .")
            else:
                # Convierte el número en string y lo alinea con ancho 2
                nueva_fila.append(str(celda).rjust(2))

        # Une la fila completa en un string con espacios en medio
        linea = " ".join(nueva_fila)
        print(linea)  # Imprime la fila ya formateada
        #forma resumida
        #print(" ".join((str(celda).rjust(2) if celda != -1 else " .") for celda in fila))


#bloques
shapes = [
    {(0,0)},#0
    {(0,0), (1,0)},#1
    {(0,0), (1,0), (0,1), (2,0)},#2
    {(0,0), (1,0), (2,0)},#3
    {(0,0), (1,0), (1,1)},#4
    {(0,0), (0,1), (1,0), (1,1)},#5
]
#print(shapes[6] == shapes[2])

def cell_free(board,x,y):
    if board[y][x] == -1:
        return True
    else:
        return False

#devuelve true si está dentro de los limites de el tablero desde 0 hasta 19
def in_bounds(x, y):
    if (x >= 0 and x < GRID_SIZE) and (y >= 0 and y < GRID_SIZE):
        return True
    else:
        return False


def can_place(board, top_left, shape):
    for (dx, dy) in shape:
        x = top_left[0] + dx
        y = top_left[1] + dy

        if not in_bounds(x, y) or not cell_free(board, x, y):
            return False
    return True

def place(board, top_left, shape, player_id):
    x0, y0 = top_left
    if can_place(board, top_left, shape):
        for (dx, dy) in shape:
            x = x0 + dx
            y = y0 + dy
            board[y][x] = player_id
        return True
    else:
        print("No se pudo colocar")



#print(b[2][3], b[2][4], b[3][3], b[3][4])

#print(cell_free(b, 15, 1))
def rotate(shape):
    rotated = set()
    # formula de rotación (x,y) -> (y,-x) 90 grados
    for (x, y) in shape:
        nuevo = (y, -x)
        rotated.add(nuevo)

    # normalizar para que no queden negativos y llevar a 0,0
    normalized = set()
    minx = min(x for (x,y) in rotated)
    miny = min(y for (x,y) in rotated)

    for (x, y) in rotated:
        ajustado = (x - minx, y - miny)
        normalized.add(ajustado)
    #print(normalized)
    # devolver la pieza ya rotada y normalizada
    return normalized

#print(f"{rotate(shapes[2])}")
#print(f"{shapes[2]}")

def normalize(shape):
    normalizedR = set()
    minx = min(x for (x, y) in shape)
    miny = min(y for (x, y) in shape)

    for (x, y) in shape:
        ajustado = (x - minx, y - miny)
        normalizedR.add(ajustado)
    return normalizedR


def reflectX(shape):
    reflected = set()
    # fórmula de reflejo en el eje X: (x,y) -> (-x,y)
    for (x, y) in shape:
        nuevo = (-x, y)
        reflected.add(nuevo)
    # normalizar para que no queden negativos y llevar a 0,0
    return normalize(reflected)


def reflectY(shape):
    reflected = set()
    # formula de reflejo en el eje y (x,y) -> (-x,y)
    for (x, y) in shape:
        nuevo = (x, -y)
        reflected.add(nuevo)
    #print(reflected)
    # normalizar para que no queden negativos y llevar a 0,0
    return normalize(reflected)



#print(reflect(shapes[2]))
place(b, (0, 0), shapes[2], 0)
place(b, (4, 0), rotate(shapes[2]), 1)
place(b, (6, 0), reflectX(shapes[2]), 2)
place(b, (10, 0), reflectY(shapes[2]), 2)



#print(f" can place ?? {can_place(b, (5,1), shapes[0])}")
#print(f"dentro de to?  {in_bounds(0, 20)}")
#print(f"dentro de to?  {in_bounds(19, 19)}")
#print(f"dentro de to?  {in_bounds(0, 20)}")
#print(f"dentro de to?  {in_bounds(20, 0)}")








print_board(b)