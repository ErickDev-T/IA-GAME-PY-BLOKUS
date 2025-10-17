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



#orientaciones = all_orientations(shapes[selected_piece_id])
orient_idx = 0

CELL = 25
MARGIN = 2
WIDTH  = GRID_SIZE * (CELL + MARGIN) + MARGIN + 20
HEIGHT = GRID_SIZE * (CELL + MARGIN) + MARGIN +20

player_roles = {}  # Diccionario que indica si un jugador es humano o IA

print("Selecciona modo de juego:")
print("1 - Jugador vs Jugador (PvP)")
print("2 - Jugador vs Computadora (PvE)")
print("3 - Computadora vs Computadora (IA vs IA) AUN DESARROLLADA")
modo_input = input("Opción: ").strip()

if modo_input == "1":
    MODO = "PVP"
    player_roles = {1: "Jugador 1", 2: "Jugador 2"}
    ai = None

elif modo_input == "2":
    MODO = "PVE"
    player_roles = {1: "Jugador", 2: "IA"}
    from ai import AIPlayer
    ai = AIPlayer(player_id=2, engine=engine)

# elif modo_input == "3":
#     MODO = "IAvIA"
#     player_roles = {1: "IA 1", 2: "IA 2"}
#     from ai import AIPlayer
#     ai1 = AIPlayer(player_id=1, engine=engine)
#     ai2 = AIPlayer(player_id=2, engine=engine)
#     ai = None  # solo para no romper compatibilidad
else:
    print("Opción inválida. Se usará PvP por defecto.")
    MODO = "PVP"
    player_roles = {1: "Jugador 1", 2: "Jugador 2"}
    ai = None




pygame.init()
font = pygame.font.SysFont(None, 20)
pygame.display.set_caption("Blokus")
overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

pantalla = pygame.display.set_mode((WIDTH, HEIGHT))
# colores
blanco = (255, 255, 255)


def build_available_shapes(pid):

    available_shapes = []
    # recorrer todas las piezas posibles del juego
    for piece_id in PIECE_IDS:
        # consultar al engine si ESTE jugador ya usó esa pieza
        alreadyUse = engine.has_used_piece(pid, piece_id)

        #si no la ha usado la agregamos a la lista de disponibles
        if not alreadyUse:
            available_shapes.append(piece_id)
        #  devolver la lista resultante
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


# --- FIN DE PARTIDA / GANADOR ---

def player_can_move(pid, board):

    remaining = build_available_shapes(pid)
    if not remaining:
        return False

    first_flag = engine.is_first_move(pid)

    # escanea el tablero entero
    for piece_id in remaining: #cada pieza
        orients = all_orientations(shapes[piece_id])
        for orient in orients:
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    cell = (x, y)
                    if can_place(board, cell, orient, pid, first_move=first_flag):
                        print(f" judada disponible en {cell} con la orientacion {orient_idx} con la pieza {piece_id}")
                        return True
    return False


def compute_scores(board):

    #cuenta celdas ocupadas por cada jugador en el tablero

    scores = {}
    for pid in engine.players:
        scores[pid] = 0

    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            val = board[y][x]
            if val in scores:
                scores[val] += 1
    return scores


def show_game_over_banner(pantalla, font, text):

    W, H = pantalla.get_size()
    title_font = pygame.font.SysFont(None, 48)
    msg_surf = title_font.render("GAME OVER", True, (0, 0, 0))
    sub_surf = font.render(text, True, (0, 0, 0))

    overlay_local = pygame.Surface((W, 120), pygame.SRCALPHA)
    overlay_local.fill((255, 255, 255, 220))
    pantalla.blit(overlay_local, (0, H//2 - 60))

    pantalla.blit(msg_surf, ( (W - msg_surf.get_width())//2, H//2 - 50 ))
    pantalla.blit(sub_surf, ( (W - sub_surf.get_width())//2, H//2 + 10 ))


def advance_to_next_player_or_end():

    global AVAILABLE_SHAPES, selected_piece_idx, selected_piece_id, orientaciones, orient_idx, consecutive_passes

    checked = 0
    while checked < len(engine.players):
        pid_now = engine.get_current_player()

        if player_can_move(pid_now, board):
            # reset de pases y preparar su selección
            consecutive_passes = 0
            AVAILABLE_SHAPES = build_available_shapes(pid_now)
            if AVAILABLE_SHAPES:
                selected_piece_idx = 0
                selected_piece_id  = AVAILABLE_SHAPES[selected_piece_idx]
                orientaciones = all_orientations(shapes[selected_piece_id])
                orient_idx = 0
            else:
                # piezas agotadas
                consecutive_passes += 1
                engine.advance_turn()
                checked += 1
                continue
            return (False, None)
        else:
            # no tiene jugadas pase automatico
            consecutive_passes += 1
            print(f"jugador {pid_now} no tiene jugadas consecutivos={consecutive_passes}")
            engine.advance_turn()
            checked += 1

        # todos pasan seguido
        if consecutive_passes >= len(engine.players):
            # calcular ganador
            scores = compute_scores(board)
            # máximo puntaje
            best_pid = max(scores, key=scores.get)
            # chequear si hay empate
            best_score = scores[best_pid]
            empatados = [p for p, sc in scores.items() if sc == best_score]
            if len(empatados) > 1:
                msg = f"Empate con {best_score} casillas: " + ", ".join([f'P{p}' for p in empatados])
            else:
                best_pid = max(scores, key=scores.get)
                best_score = scores[best_pid]
                empatados = [p for p, sc in scores.items() if sc == best_score]

                def nombre_jugador(pid):
                    return player_roles.get(pid, f"P{pid}")

                if len(empatados) > 1:
                    nombres = [nombre_jugador(p) for p in empatados]
                    msg = f"Empate con {best_score} casillas entre " + " y ".join(nombres)
                else:
                    ganador = nombre_jugador(best_pid)
                    msg = f"Gana {ganador} con {best_score} casillas"

            return (True, msg)

    return (False, None)

consecutive_passes = 0
game_over = False
game_over_msg = None


while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        elif event.type == KEYDOWN:
            # rotar orientacion de la pieza actual
            if event.key in (K_RIGHT, K_d):
                if orientaciones:
                    orient_idx = (orient_idx + 1) % len(orientaciones)
            elif event.key in (K_LEFT, K_a):
                if orientaciones:
                    orient_idx = (orient_idx - 1) % len(orientaciones)
            # cambiar de pieza sobre AVAILABLE_SHAPES
            elif event.key in (K_UP, K_DOWN):
                pid_now = engine.get_current_player()
                # siempre reconstruye la lista de disponibles del jugador actual
                AVAILABLE_SHAPES = build_available_shapes(pid_now)

                if not AVAILABLE_SHAPES:
                    # no hay nada para seleccionar
                    selected_piece_idx = -1
                    selected_piece_id = None
                    orientaciones = []
                    orient_idx = 0
                    print(f" P{pid_now} no tiene piezas disponibles")
                else:
                    # asegura que el indice esté dentro de rango si n arranca en 0
                    if 'selected_piece_idx' not in globals() or selected_piece_idx < 0 or selected_piece_idx >= len(
                            AVAILABLE_SHAPES):
                        selected_piece_idx = 0
                    step = -1 if event.key == K_UP else 1
                    # repite hasta encontrar una pieza no usada
                    turns = 0
                    while turns < len(AVAILABLE_SHAPES):
                        selected_piece_idx = (selected_piece_idx + step) % len(AVAILABLE_SHAPES)
                        cand_id = AVAILABLE_SHAPES[selected_piece_idx]

                        if not engine.has_used_piece(pid_now, cand_id):
                            selected_piece_id = cand_id
                            orientaciones = all_orientations(shapes[selected_piece_id])
                            orient_idx = 0
                            #print(f"id {selected_piece_id} (idx {selected_piece_idx})")
                            break
                        turns += 1

                    if turns >= len(AVAILABLE_SHAPES):
                        selected_piece_idx = -1
                        selected_piece_id = None
                        orientaciones = []
                        orient_idx = 0
            #elif event.key == K_p:
             #   # el jugador actual decide pasar manualmente
              #  pid_now = engine.get_current_player()
               # print(f"[INFO] Jugador {pid_now} presiona PASAR (P).")
                #consecutive_passes += 1
                #engine.advance_turn()
                #is_over, msg = advance_to_next_player_or_end()


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
                        AVAILABLE_SHAPES = build_available_shapes(pid)
                        # reinicia pases siempre que alguien jugo
                        consecutive_passes = 0
                        if engine.is_first_move(pid):
                            engine.mark_first_move_done(pid)

                        # cambia de turno y resuelve auto-pases o fin
                        engine.advance_turn()
                        is_over, msg = advance_to_next_player_or_end()

                        # --- Turno automático de la IA (si aplica) ---
                        if MODO == "PVE":
                            pid_now = engine.get_current_player()
                            if pid_now == 2 and not game_over:
                                print("IA Pensando ...")
                                ai_move = ai.get_move()

                                if ai_move:
                                    piece_id, orient, coord = ai_move
                                    first_flag = engine.is_first_move(pid_now)

                                    if place(board, coord, orient, pid_now, first_move=first_flag):
                                        engine.mark_piece_used(pid_now, piece_id)
                                        AVAILABLE_SHAPES = build_available_shapes(pid_now)
                                        if first_flag:
                                            engine.mark_first_move_done(pid_now)

                                        print(f"IA jugo la pieza {piece_id} en {coord}")
                                        engine.advance_turn()
                                        is_over, msg = advance_to_next_player_or_end()
                                        if is_over:
                                            game_over = True
                                            game_over_msg = msg
                                else:
                                    print("IA No encontro jugada valida.")

                        if is_over:
                            game_over = True
                            game_over_msg = msg
                            print("GAME OVER", msg)


                    else:
                        print(f" movimiento invalido para P{pid} en {cell} con pieza {selected_piece_id}")
                else:
                    print(f"jugador {pid} ya uso la pieza {selected_piece_id}")

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

    if game_over:
        show_game_over_banner(pantalla, font, game_over_msg)
    pygame.display.flip()

    clock.tick(60)





pygame.quit()
sys.exit()
