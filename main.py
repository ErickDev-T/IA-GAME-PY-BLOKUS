import pygame, sys
from pygame.locals import *
from logic import make_board, place, can_place, shapes, GRID_SIZE, rotate, reflectX, reflectY, all_orientations, PLAYER_CORNERS
from engine import GameEngine


engine = GameEngine([1, 2, 3 ,4], shapes)  # por ejemplo, 2 jugadores
board = engine.board

#NUM_PLAYERS = 4

#first_move = {}                         # crea un diccionario vacío
#for pid in range(1, NUM_PLAYERS + 1):   # recorre del 1 hasta NUM_PLAYERS
#    first_move[pid] = True              # asigna True a cada jugadoprint(first_move)
#print(first_move)

PIECE_IDS = list(shapes.keys())  # o un orden específico que tú decidas
selected_piece_id = "I3"         # elige una inicial válida

selected_piece_idx = PIECE_IDS.index(selected_piece_id)


orientaciones = all_orientations(shapes[selected_piece_id])
orient_idx = 0

CELL = 25
MARGIN = 2
WIDTH  = GRID_SIZE * (CELL + MARGIN) + MARGIN + 20
HEIGHT = GRID_SIZE * (CELL + MARGIN) + MARGIN +20

pygame.init()
font = pygame.font.SysFont(None, 20)
pygame.display.set_caption("Blokus")
overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
# colores
blanco = (255, 255, 255)

def draw_hud(pantalla, font, engine, selected_piece_id, selected_piece_idx, total_pieces, orient_idx, total_orients):
    current_player = engine.get_current_player()
    texto = f"P{current_player}  |  Pieza: {selected_piece_id} ({selected_piece_idx+1}/{total_pieces})  |  Orient: {orient_idx+1}/{total_orients}"
    surf = font.render(texto, True, (0, 0, 0))
    W, H = pantalla.get_size()
    pantalla.blit(surf, (6, H - surf.get_height() - 6))



def color_of(val):
    if val == -1:        # celda vacía
        return (200, 200, 200)     # gris
    elif val == 1:
        return (59, 130, 246)      # azul
    elif val == 2:
        return (16, 185, 129)       # verde
    elif val == 3:
        return (244, 63, 94)      # verde
    elif val == 4:
        return (234, 179, 8)      # amarillo
    else:
        return (0, 0, 0)


def mouse_to_cell(mx, my, GRID_SIZE, CELL, MARGIN):
    tx = mx - MARGIN
    ty = my - MARGIN
    if tx < 0 or ty < 0:
        return None
    qx, rx = divmod(tx, CELL + MARGIN)
    qy, ry = divmod(ty, CELL + MARGIN)
    if qx < 0 or qx >= GRID_SIZE or qy < 0 or qy >= GRID_SIZE:
        return None
    if rx >= CELL or ry >= CELL:
        return None
    return (qx, qy)


def draw_shadow(pantalla, overlay, board, mx, my, orientaciones, orient_idx, pid, first_move_flag, GRID_SIZE, CELL, MARGIN):
    cell = mouse_to_cell(mx, my, GRID_SIZE, CELL, MARGIN)
    if cell is None:
        return

    pieza = orientaciones[orient_idx]
    cx, cy = cell

    # comprobar que todas las celdas caen dentro
    coords = []
    for (dx, dy) in pieza:
        x, y = cx + dx, cy + dy
        if not (0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE):
            return  # si se sale no dibuja sombra
        coords.append((x, y))

    valido = can_place(board, cell, pieza, engine.get_current_player(), first_move_flag)

    overlay.fill((0, 0, 0, 0))
    base = color_of(engine.get_current_player())
    color = (base[0], base[1], base[2], 110) if valido else (255, 0, 0, 110)

    for (x, y) in coords:
        rx = x * (CELL + MARGIN) + MARGIN
        ry = y * (CELL + MARGIN) + MARGIN
        pygame.draw.rect(overlay, color, (rx, ry, CELL, CELL))

    pantalla.blit(overlay, (0, 0))


clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            if event.key in (K_RIGHT, K_d):
                orient_idx = (orient_idx + 1) % len(orientaciones)
            elif event.key in (K_LEFT, K_a):
                orient_idx = (orient_idx - 1) % len(orientaciones)

            elif event.key == K_UP:
                selected_piece_idx = (selected_piece_idx - 1) % len(PIECE_IDS)
                selected_piece_id = PIECE_IDS[selected_piece_idx]
                orientaciones = all_orientations(shapes[selected_piece_id])
                orient_idx = 0

            elif event.key == K_DOWN:
                selected_piece_idx = (selected_piece_idx + 1) % len(PIECE_IDS)
                selected_piece_id = PIECE_IDS[selected_piece_idx]
                orientaciones = all_orientations(shapes[selected_piece_id])
                orient_idx = 0
#                                              boton izquierdo del mouse
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            cell = mouse_to_cell(mx, my, GRID_SIZE, CELL, MARGIN)
            if cell is not None:
                pieza = orientaciones[orient_idx]
                pid = engine.get_current_player()
                if place(board, cell, pieza, pid, first_move=engine.is_first_move(pid)):
                    if engine.is_first_move(pid):
                        engine.mark_first_move_done(pid)
                    engine.advance_turn()
                    print("Jugador actual:", engine.get_current_player())



    pantalla.fill(blanco)
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            val = board[y][x]
            color = color_of(val)
            rx = x * (CELL + MARGIN) + MARGIN
            ry = y * (CELL + MARGIN) + MARGIN
            pygame.draw.rect(pantalla, color, (rx, ry, CELL, CELL))



    mx, my = pygame.mouse.get_pos()
    pid = engine.get_current_player()

    draw_hud(pantalla, font, engine, selected_piece_id, selected_piece_idx, len(PIECE_IDS), orient_idx, len(orientaciones))
    #que se dibuje tod0 en pantalla

    draw_shadow(
        pantalla, overlay, board, mx, my,
        orientaciones, orient_idx,
        pid, engine.is_first_move(pid),
        GRID_SIZE, CELL, MARGIN
    )
    pygame.display.flip()

    clock.tick(60)



pygame.quit()
sys.exit()
