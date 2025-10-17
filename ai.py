import time
from copy import deepcopy
from logic import can_place, place, all_orientations, shapes, GRID_SIZE

class AIPlayer:
    def __init__(self, player_id, engine, max_time=10, max_depth=5):

        self.id = player_id
        self.engine = engine
        self.max_time = max_time
        self.max_depth = max_depth

    # FUNCION PRINCIPAL ELEGIR JUGADA
    def get_move(self):
        start_time = time.time()
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
        return best_move

    # ALGORITMO MINIMAX CON PODA ALFA-BETA
    def minimax(self, board, depth, alpha, beta, maximizing, start_time):
        # detener si se acaba el tiempo o la profundidad
        if time.time() - start_time > self.max_time or depth >= self.max_depth:
            return self.evaluate(board)

        if maximizing:
            # turno de la IA
            max_eval = float("-inf")
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    if board[y][x] == -1:
                        temp = deepcopy(board)
                        temp[y][x] = self.id
                        eval = self.minimax(temp, depth+1, alpha, beta, False, start_time)
                        max_eval = max(max_eval, eval)
                        alpha = max(alpha, eval)
                        if beta <= alpha:
                            break
            return max_eval
        else:
            # turno del oponente (humano o IA contraria)
            min_eval = float("inf")
            opponent_id = 1 if self.id != 1 else 2
            for y in range(GRID_SIZE):
                for x in range(GRID_SIZE):
                    if board[y][x] == -1:
                        temp = deepcopy(board)
                        temp[y][x] = opponent_id
                        eval = self.minimax(temp, depth+1, alpha, beta, True, start_time)
                        min_eval = min(min_eval, eval)
                        beta = min(beta, eval)
                        if beta <= alpha:
                            break
            return min_eval

    # HEURISTICA DE EVALUACION
    def evaluate(self, board):
        my_cells = sum(cell == self.id for row in board for cell in row)
        opp_cells = sum(cell not in (-1, self.id) for row in board for cell in row)
        empty_cells = sum(cell == -1 for row in board for cell in row)

        # ponderación básica
        score = (my_cells * 3) - (opp_cells * 2) + (empty_cells * 0.1)
        return score
