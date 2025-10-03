import pygame, sys
from pygame.locals import *
from logic import make_board, place, can_place, shapes, GRID_SIZE, rotate, reflectX, reflectY, all_orientations, PLAYER_CORNERS
from engine import GameEngine


engine = GameEngine([1, 2], shapes)  # por ejemplo, 2 jugadores
board = engine.board

#NUM_PLAYERS = 4

#first_move = {}                         # crea un diccionario vacío
#for pid in range(1, NUM_PLAYERS + 1):   # recorre del 1 hasta NUM_PLAYERS
#    first_move[pid] = True              # asigna True a cada jugadoprint(first_move)
#print(first_move)

PIECE_IDS = list(shapes.keys())  # o un orden específico que tú decidas
#selected_piece_id = "I3"         # elige una inicial válida

#selected_piece_idx = PIECE_IDS.index(selected_piece_id)


#orientaciones = all_orientations(shapes[selected_piece_id])
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


def build_available_shapes(pid):
    # 1) Crear contenedor vacío
    available_shapes = []
    # 2) Recorrer TODAS las piezas posibles del juego
    for piece_id in PIECE_IDS:
        # 3) Consultar al engine si ESTE jugador ya usó esa pieza
        alreadyUse = engine.has_used_piece(pid, piece_id)

        # 4) Si NO la ha usado, la agregamos a la lista de disponibles
        if not alreadyUse:
            available_shapes.append(piece_id)

        # 5) Devolver la lista resultante
    return available_shapes


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

pid = engine.get_current_player()
AVAILABLE_SHAPES = build_available_shapes(pid)

selected_piece_idx = 0 if AVAILABLE_SHAPES else -1
selected_piece_id  = AVAILABLE_SHAPES[selected_piece_idx] if AVAILABLE_SHAPES else None

orientaciones = all_orientations(shapes[selected_piece_id]) if selected_piece_id is not None else []
orient_idx = 0


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            # Rotar orientación de la pieza actual
            if event.key in (K_RIGHT, K_d):
                if orientaciones:
                    orient_idx = (orient_idx + 1) % len(orientaciones)
            elif event.key in (K_LEFT, K_a):
                if orientaciones:
                    orient_idx = (orient_idx - 1) % len(orientaciones)
            # Cambiar de pieza (arriba/abajo): SIEMPRE sobre AVAILABLE_SHAPES
            elif event.key in (K_UP, K_DOWN):
                pid_now = engine.get_current_player()
                # Siempre reconstruye la lista de disponibles del jugador actual
                AVAILABLE_SHAPES = build_available_shapes(pid_now)

                if not AVAILABLE_SHAPES:
                    # No hay nada para seleccionar
                    selected_piece_idx = -1
                    selected_piece_id = None
                    orientaciones = []
                    orient_idx = 0
                    print(f"[INFO] P{pid_now} no tiene piezas disponibles.")
                else:
                    # Asegura que el índice esté dentro de rango; si no, arranca en 0
                    if 'selected_piece_idx' not in globals() or selected_piece_idx < 0 or selected_piece_idx >= len(
                            AVAILABLE_SHAPES):
                        selected_piece_idx = 0
                    # Muee el índice según la tecla
                    step = -1 if event.key == K_UP else 1
                    # Repite hasta encontrar una pieza NO usada (o dar la vuelta completa)
                    turns = 0
                    while turns < len(AVAILABLE_SHAPES):
                        selected_piece_idx = (selected_piece_idx + step) % len(AVAILABLE_SHAPES)
                        cand_id = AVAILABLE_SHAPES[selected_piece_idx]
                        # Doble seguro: aunque AVAILABLE_SHAPES ya filtra, verificamos contra el engine
                        if not engine.has_used_piece(pid_now, cand_id):
                            selected_piece_id = cand_id
                            orientaciones = all_orientations(shapes[selected_piece_id])
                            orient_idx = 0
                            print(f"[DBG] Selección -> id {selected_piece_id} (idx {selected_piece_idx})")
                            break
                        turns += 1

                    # Si por alguna razón todas resultan usadas (no debería), resetea

                    if turns >= len(AVAILABLE_SHAPES):
                        print("[WARN] Todas las piezas navegables resultaron usadas; reseteando selección.")
                        selected_piece_idx = -1
                        selected_piece_id = None
                        orientaciones = []
                        orient_idx = 0

        #
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            cell = mouse_to_cell(mx, my, GRID_SIZE, CELL, MARGIN)

            if cell is not None and selected_piece_id is not None:
                pieza = orientaciones[orient_idx]
                pid = engine.get_current_player()

                if not engine.has_used_piece(pid, selected_piece_id):
                    if place(board, cell, pieza, pid, first_move=engine.is_first_move(pid)):
                        engine.mark_piece_used(pid, selected_piece_id)
                        if engine.is_first_move(pid):
                            engine.mark_first_move_done(pid)

                        # (Opcional) si mantienes lista local, puedes sacar la pieza usada:
                        # if selected_piece_id in AVAILABLE_SHAPES:
                        #     rem_at = AVAILABLE_SHAPES.index(selected_piece_id)
                        #     AVAILABLE_SHAPES.pop(rem_at)
                        #     if rem_at <= selected_piece_idx:
                        #         selected_piece_idx = max(0, selected_piece_idx - 1)

                        engine.advance_turn()
                        nuevo_pid = engine.get_current_player()
                        print("jugador ahora:", nuevo_pid)

                        # Recalcular SOLO para el nuevo jugador
                        AVAILABLE_SHAPES = build_available_shapes(nuevo_pid)
                        if AVAILABLE_SHAPES:
                            selected_piece_idx = 0
                            selected_piece_id = AVAILABLE_SHAPES[selected_piece_idx]
                            orientaciones = all_orientations(shapes[selected_piece_id])
                            orient_idx = 0
                        else:
                            selected_piece_idx = -1
                            selected_piece_id = None
                            orientaciones = []
                    else:
                        print(f"[WARN] Movimiento inválido para P{pid} en {cell} con pieza {selected_piece_id}")
                else:
                    print(f"[INFO] Jugador {pid} ya usó la pieza {selected_piece_id}")

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



    draw_hud(pantalla, font, engine, selected_piece_id, selected_piece_idx, len(AVAILABLE_SHAPES), orient_idx, len(orientaciones))
    #que se dibuje tod0 en pantalla

    if selected_piece_id is not None and orientaciones:
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
