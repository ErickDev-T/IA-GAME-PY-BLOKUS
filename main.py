import pygame, sys
from pygame.locals import *
from logic import make_board, place, can_place, shapes, GRID_SIZE
board = make_board()
first_move_p1 = True
pieza = shapes[2]
#place(board, (0,0), shapes[2], 1, first_move=True)


GRID_SIZE = 20
CELL = 25
MARGIN = 2

HEIGHT = GRID_SIZE * (CELL + MARGIN) + MARGIN
WIDTH = GRID_SIZE * (CELL + MARGIN) + MARGIN
print(HEIGHT, WIDTH)

pygame.init()

pantalla = pygame.display.set_mode((HEIGHT,WIDTH))
pygame.display.set_caption("Blokus")



# constantes de colores
blanco = (255, 255, 255)
rojo   = (255, 0, 0)


def color_of(val):
    if val == -1:        # celda vacía
        return (200,200,200)   # gris
    elif val == 1:       # jugador 1
        return (59,130,246)   # azul
    elif val == 2:       # jugador 2
        return (239,68,68)    # rojo
    else:
        return (0,0,0)   # negro por si acaso



#print("valores", board[0][:10])

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pantalla.fill(blanco)

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            val = board[y][x]  # número (-1, 1 o 2)
            color = color_of(val)  # convierto ese número en color
            rx = x * (CELL + MARGIN) + MARGIN
            ry = y * (CELL + MARGIN) + MARGIN
            pygame.draw.rect(pantalla, color, (rx, ry, CELL, CELL))

        #CELL = 25
        #MARGIN = 2
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                tx = mx - MARGIN
                #print(f"tx: {mx} - {MARGIN} = {tx}")
                ty = my - MARGIN
                #print(f"tx: {my} - {MARGIN} =  {ty}")
                if tx < 0 or ty < 0:
                    #print("no pay eso es < 0")
                    continue
                qx, rx = divmod(tx, CELL + MARGIN)
                #print(f" EL X= divmod({tx} {CELL +   MARGIN}) = {qx, rx}")
                qy, ry = divmod(ty, CELL + MARGIN)
                #print(f" EL Y= divmod({ty} {CELL + MARGIN}) = {qy, ry}")
                if qx < 0 or qx >= GRID_SIZE or qy < 0 or qy >= GRID_SIZE:
                    #print("borde dentroaaaa")

                    continue
                if rx >= CELL or ry >= CELL:
                    #print(f"{ry} >= {CELL} or {ry} >= {CELL}")
                    continue
                #print("celda:", qx, qy)
                ok = place(board, (qx, qy), pieza, 1, first_move=first_move_p1)
                if ok:
                    first_move_p1 = False
    pygame.display.update()
