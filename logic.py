GRID_SIZE = 20

def make_board():
    board = []
    for i in range(GRID_SIZE):     # repetir 20 veces las filas
        fila = []
        for j in range(GRID_SIZE): # repetir 20 veces las columnas
            fila.append(-1) # agregar -1 en cada celda
        board.append(fila)
    #print(board)
    return board
#manera resumida
#def make_board():
#    return [[-1 for _ in range(20)] for _ in range(20)]


b = make_board()
#print(len(b), len(b[0]))



def print_board(board):
    # encabezado de columnas
    header = "   " + " ".join(str(c).rjust(2) for c in range(GRID_SIZE))
    print(header)
    for yi, fila in enumerate(board):
        nueva_fila = []
        for celda in fila:
            nueva_fila.append(str(celda).rjust(2) if celda != -1 else " .")
        print(str(yi).rjust(2), " ".join(nueva_fila))


PLAYER_CORNERS = {
    1: (0, 0),                  # arriba-izquierda
    2: (GRID_SIZE-1, GRID_SIZE-1),  # abajo-derecha
    3: (0, GRID_SIZE-1),        # abajo-izquierda
    4: (GRID_SIZE-1, 0),        # arriba-derecha
}

#bloques  offset
shapes = {
    # Monomino
    "I1": {(0,0)},

    # Domino
    "I2": {(0,0), (1,0)},

    # Triominos
    "I3": {(0,0), (1,0), (2,0)},                  # línea de 3
    "L3": {(0,0), (1,0), (1,1)},                  # L de 3

    # Tetrominos
    "O4": {(0,0), (1,0), (0,1), (1,1)},           # cuadrado
    "I4": {(0,0), (1,0), (2,0), (3,0)},           # línea de 4
    "T4": {(0,0), (1,0), (2,0), (1,1)},           # T
    "L4": {(0,0), (0,1), (0,2), (1,0)},           # L de 4
    "S4": {(1,0), (2,0), (0,1), (1,1)},           # S/Z de 4

    # Pentominos
    "I5": {(0,0), (1,0), (2,0), (3,0), (4,0)},    # línea de 5
    "L5": {(0,0), (0,1), (0,2), (0,3), (1,0)},    # L de 5
    "N5": {(1,0), (2,0), (0,1), (1,1), (0,2)},    # N de 5
    "P5": {(0,0), (1,0), (0,1), (1,1), (0,2)},    # P
    "T5": {(0,0), (1,0), (2,0), (1,1), (1,2)},    # T de 5
    "U5": {(0,0), (2,0), (0,1), (1,1), (2,1)},    # U
    "V5": {(0,0), (0,1), (0,2), (1,2), (2,2)},    # V
    "W5": {(0,0), (0,1), (1,1), (1,2), (2,2)},    # W
    "X5": {(1,0), (0,1), (1,1), (2,1), (1,2)},    # X
    "Y5": {(0,0), (1,0), (2,0), (3,0), (1,1)},    # Y
    "Z5": {(0,0), (1,0), (1,1), (2,1), (2,2)},    # Z
    "F5": {(1,0), (0,1), (1,1), (1,2), (2,2)}     # F
}
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


def can_place(board, starting_point, shape, player_id, first_move=False):
    beside = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    diag = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    corner_ok = False
    x0, y0 = starting_point

    required_corner = PLAYER_CORNERS.get(player_id)
    covers_required_corner = False

    for (dx, dy) in shape:
        x, y = x0 + dx, y0 + dy

        #si la celda es valida (dentro de el tablero y libre)
        if not in_bounds(x, y) or not cell_free(board, x, y):
            #  operador ternario
            val = board[y][x] if in_bounds(x, y) else None
            #print("falla libre en:", (x, y), "valor:", val)
            return False

        #primer movimiento
        if first_move and required_corner and (x, y) == required_corner:
            covers_required_corner = True

        # prohibido tocar por lado una pieza propia
        for (ox, oy) in beside:
            nx, ny = x + ox, y + oy
            if in_bounds(nx, ny) and board[ny][nx] == player_id:
                #print("Falla por LADO con tu color en:", (nx, ny))
                return False

        # Debe tocar por esquina alguna pieza propia (excepto primer movimiento)
        for (dx2, dy2) in diag:
            nx, ny = x + dx2, y + dy2
            if in_bounds(nx, ny) and board[ny][nx] == player_id:
                corner_ok = True

    if first_move:
        if not covers_required_corner:
            #print("Falla: tu PRIMER movimiento debe cubrir tu esquina:", required_corner)
            return False
    else:
        if not corner_ok:
            #print("Falla por NO ESQUINA con tu color")
            return False

    return True

def place(board, starting_point, shape, player_id, first_move=False):
    x0, y0 = starting_point
    if can_place(board, starting_point, shape, player_id, first_move=first_move):
        for (dx, dy) in shape:
            x = x0 + dx
            y = y0 + dy
            board[y][x] = player_id
        return True
    else:
        #print("No se pudo colocar")
        return False


def normalize(shape):
    normalizedR = set()
    minx = min(x for (x, y) in shape)
    miny = min(y for (x, y) in shape)

    for (x, y) in shape:
        ajustado = (x - minx, y - miny)
        normalizedR.add(ajustado)
    return normalizedR

#print(b[2][3], b[2][4], b[3][3], b[3][4])

#print(cell_free(b, 15, 1))
def rotate(shape):
    rotated = set()
    # formula de rotacion (x,y) -> (y,-x) 90 grados
    for (x, y) in shape:
        nuevo = (y, -x)
        rotated.add(nuevo)



    # devolver la pieza ya rotada y normalizada
    return normalize(rotated)

#print(f"{rotate(shapes[2])}")
#print(f"{shapes[2]}")


def reflectX(shape):
    reflected = set()
    for (x, y) in shape:
        nuevo = (x, -y)
        reflected.add(nuevo)
    # normalizar para que no queden negativos y llevar a 0,0
    return normalize(reflected)


def reflectY(shape):
    reflected = set()
    for (x, y) in shape:
        nuevo = (-x, y)
        reflected.add(nuevo)
    #print(reflected)
    # normalizar para que no queden negativos y llevar a 0,0
    return normalize(reflected)
L4 = {(0,0), (0,1), (0,2), (1,0)}

def all_orientations(shape):
    orig = normalize(shape)
    base = orig
    orientations = set()
    for _ in range(4):
        orientations.add(frozenset(base))
        base = rotate(base)
    #print("A", len(orientations))

    ref = reflectX(orig)
    for _ in range(4):
        orientations.add(frozenset(ref))
        ref = rotate(ref)
    lista = [set(fs) for fs in orientations]
    #print("TOTAL", len(orientations))

    return lista

#print(len(all_orientations(L4)))
#place(b, (0,0), shapes[2], 1)
# place(b, (0,1), reflectX(shapes[2]), 1)

# place(b, (4,1), reflectY(shapes[2]), 1)
# place(b, (0,5), rotate(shapes[2]), 1)
# place(b, (3,6), rotate(rotate(shapes[2])), 1)
# place(b, (8,5), rotate(rotate(rotate(shapes[2]))), 1)












#print(reflect(shapes[2]))
#place(b, (0,0), shapes[1], 1, first_move=True)
#place(b, (GRID_SIZE-1, GRID_SIZE-1), shapes[0], 2, first_move=True)
#place(b, (0, GRID_SIZE-1), shapes[0], 3, first_move=True)
#place(b, (GRID_SIZE-1, 0), shapes[0], 4, first_move=True)



#place(b, (GRID_SIZE-1, GRID_SIZE-1), shapes[1], 2, first_move=True)
#place(b, (3,1), rotate(shapes[4]), 1)


#place(b, (5,2), rotate(shapes[1]), 1)

#place(b, (6, 0), reflectX(shapes[2]), 2)
#place(b, (10, 0), reflectY(shapes[2]), 2)



#print(f" can place ?? {can_place(b, (5,1), shapes[0])}")
#print(f"dentro de to?  {in_bounds(0, 20)}")
#print(f"dentro de to?  {in_bounds(19, 19)}")
#print(f"dentro de to?  {in_bounds(0, 20)}")
#print(f"dentro de to?  {in_bounds(20, 0)}")




#print_board(b)