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
print(len(b), len(b[0]))

b = make_board()


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
    {(0,0)},                 # monomino
    {(0,0), (1,0)},          # dominó
    {(0,0), (1,0), (0,1)}    # L
]



def cell_free(board,x,y):
    if board[x][y] == -1:
        return True
    else:
        return False


#devuelve true si esta dentro de los limites de el tablero desde 0 hasta 19
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
    if can_place(board, top_left, shape) == True:
        for (dx, dy) in shape:
            x = x0 + dx
            y = y0 + dy
            board[y][x] = player_id

place(b, (5, 1), shapes[2], 1)
#print(f" can place ?? {can_place(b, (5,1), shapes[0])}")
#print(f"dentro de to?  {in_bounds(0, 20)}")
#print(f"dentro de to?  {in_bounds(19, 19)}")
#print(f"dentro de to?  {in_bounds(0, 20)}")
#print(f"dentro de to?  {in_bounds(20, 0)}")








print_board(b)