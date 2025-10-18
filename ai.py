import time
from copy import deepcopy
from logic import can_place, place, all_orientations, shapes, GRID_SIZE

class AIPlayer:
    def __init__(self, player_id, engine, max_time=5, max_depth=2):

        self.id = player_id
        self.engine = engine
        self.max_time = max_time
        self.max_depth = max_depth
        self.total_nodes_expanded = 0

    # FUNCION PRINCIPAL ELEGIR JUGADA
    def get_move(self):
        start_time = time.time()
        self.total_nodes_expanded = 0
        board = self.engine.board
        first_move = self.engine.is_first_move(self.id)

        # piezas aún no usadas
        shapes_left = [
            sid for sid in self.engine.shapes.keys()
            if not self.engine.has_used_piece(self.id, sid)
        ]

        best_move = None
        best_value = float("-inf")

        # probar todas las combinaciones posibles
        for piece_id in shapes_left:
            for orient in all_orientations(shapes[piece_id]):
                for y in range(GRID_SIZE):
                    for x in range(GRID_SIZE):
                        if time.time() - start_time > self.max_time:
                            return best_move
                        coord = (x, y)
                        if can_place(board, coord, orient, self.id, first_move):
                            new_board = deepcopy(board)
                            place(new_board, coord, orient, self.id, first_move)

                            # llamada a minimax
                            value = self.minimax(
                                new_board,
                                depth=1,
                                alpha=-float("inf"),
                                beta=float("inf"),
                                maximizing=False,
                                start_time=start_time
                            )

                            if value > best_value:
                                best_value = value
                                best_move = (piece_id, orient, coord)
        end_time = time.time()
        elapsed = end_time - start_time

        print(f"\n[IA{self.id}] Mejor valor: {best_value:.2f}")
        print(f"[IA{self.id}] Nodos expandidos: {self.total_nodes_expanded}")
        print(f"[IA{self.id}] Tiempo de ejecución: {elapsed:.2f} s\n")

        return best_move

    # ALGORITMO MINIMAX CON PODA ALFA-BETA
    def minimax(self, board, depth, alpha, beta, maximizing, start_time):
        self.total_nodes_expanded += 1
        # detener si se acaba el tiempo o la profundidad
        if time.time() - start_time > self.max_time or depth >= self.max_depth:
            return self.evaluate(board)

        if maximizing:
            max_eval = float("-inf")
            first_move = self.engine.is_first_move(self.id)
            shapes_left = [
                sid for sid in self.engine.shapes.keys()
                if not self.engine.has_used_piece(self.id, sid)
            ]
            for piece_id in shapes_left:
                for orient in all_orientations(shapes[piece_id]):
                    for y in range(GRID_SIZE):
                        for x in range(GRID_SIZE):
                            coord = (x, y)
                            if can_place(board, coord, orient, self.id, first_move):
                                temp = deepcopy(board)
                                place(temp, coord, orient, self.id, first_move)
                                value = self.minimax(temp, depth + 1, alpha, beta, False, start_time)
                                max_eval = max(max_eval, value)
                                alpha = max(alpha, value)
                                if beta <= alpha:
                                    break
            return max_eval

        else:
            min_eval = float("inf")
            opponent_id = 1 if self.id == 2 else 2

            for piece_id in self.engine.shapes.keys():
                for orient in all_orientations(shapes[piece_id]):
                    for y in range(GRID_SIZE):
                        for x in range(GRID_SIZE):
                            coord = (x, y)
                            if can_place(board, coord, orient, opponent_id, False):
                                temp = deepcopy(board)
                                place(temp, coord, orient, opponent_id, False)
                                value = self.minimax(temp, depth + 1, alpha, beta, True, start_time)
                                min_eval = min(min_eval, value)
                                beta = min(beta, value)
                                if beta <= alpha:
                                    break

            return min_eval

    #se guardaran los tamaños en celdas de todas las piezas que el jugador aún no coloca
    def average_piece_size(self):

        remaining_sizes = []
        for piece_id, shape in self.engine.shapes.items():
            if not self.engine.has_used_piece(self.id, piece_id):
                remaining_sizes.append(len(shape))

        if not remaining_sizes:
            return 0
        return sum(remaining_sizes) / len(remaining_sizes)

    def count_possible_corners(self, board, player_id):

        GRID_SIZE = len(board)
        diag = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        beside = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        count = 0

        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if board[y][x] != -1:
                    continue  # solo nos interesan las vacías

                touches_diag = False
                touches_side = False

                for dx, dy in diag:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        if board[ny][nx] == player_id:
                            touches_diag = True

                for dx, dy in beside:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        if board[ny][nx] == player_id:
                            touches_side = True

                if touches_diag and not touches_side:
                    count += 1

        return count

    # HEURISTICA

    def evaluate(self, board):

        # 1ra HEURISTICA cuantas fichas de el jugador hay BUENO

        my_cells = 0
        for row in board:  # recorrer cada fila del tablero
            for cell in row:  # recorrer cada celda de esa fila
                if cell == self.id:  # si la celda pertenece al jugador actual
                    my_cells += 1  # sumamos 1 a nuestro contador

        # 2da HEURISTICA Cuantas de el enemigo MALO
        opp_cells = 0
        for row in board:  # recorrer cada fila del tablero
            for cell in row:  # recorrer cada celda
                # si la celda NO está vacía (-1) y NO es nuestra
                if cell != -1 and cell != self.id:
                    opp_cells += 1  # entonces pertenece al oponente

        # 3ra HEURISTICA Cuantas vacias Bueno pero no tanto xd El peso 0.1 es bajo porque el espacio libre  no garantiza victoria pero ayuda a tener esacio para seguir jugando.
        empty_cells = 0
        for row in board:  # recorrer cada fila
            for cell in row:  # recorrer cada celda
                if cell == -1:  # si la celda está vacía
                    empty_cells += 1  # sumar 1 al contador de vacías

        # 4ta HEURISTICA esquinas disponibles para seguir jugando
        corners = self.count_possible_corners(board, self.id)

        #5ta HEURISTICA las piezas de el jugador
        avg_piece_size = self.average_piece_size()

        # ponderación

        # 1 heuristicas
        #score = my_cells

        # 2 heuristicas
        #score = (my_cells * 3) - (opp_cells * 2)

        # 3 heuristicas
        #score = (my_cells * 3) - (opp_cells * 2) + (empty_cells * 0.1)

        # 4 heuristicas
        #score = (my_cells * 3) - (opp_cells * 2) + (empty_cells * 0.1) + (corners * 2.5)

        # 5 heuristicas
        score = ((my_cells * 3) - (opp_cells * 2)+ (empty_cells * 0.1) + (corners * 2.5) - (avg_piece_size * 1.5))  # penaliza tener piezas grandes pendientes


        return score
