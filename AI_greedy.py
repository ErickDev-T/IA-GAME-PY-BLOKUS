from copy import deepcopy
from logic import can_place, place, all_orientations, shapes, GRID_SIZE

class GreedyAI:
    def __init__(self, player_id, engine):
        self.id = player_id
        self.engine = engine

    def get_move(self):
        board = self.engine.board
        first_move = self.engine.is_first_move(self.id)

        shapes_left = [
            sid for sid in self.engine.shapes.keys()
            if not self.engine.has_used_piece(self.id, sid)
        ]

        best_move = None
        best_value = float("-inf")

        # probar todas las jugadas posibles
        for piece_id in shapes_left:
            for orient in all_orientations(shapes[piece_id]):
                for y in range(GRID_SIZE):
                    for x in range(GRID_SIZE):
                        coord = (x, y)
                        if can_place(board, coord, orient, self.id, first_move):
                            temp = deepcopy(board)
                            place(temp, coord, orient, self.id, first_move)

                            value = self.evaluate(temp)
                            if value > best_value:
                                best_value = value
                                best_move = (piece_id, orient, coord)

        return best_move

    def evaluate(self, board):

        #ve tablero solo para este turno

        my_cells = sum(row.count(self.id) for row in board)
        opp_id = 1 if self.id == 2 else 2
        opp_cells = sum(row.count(opp_id) for row in board)
        empty = sum(row.count(-1) for row in board)

        # heuristica sencilla
        score = (my_cells * 3) - (opp_cells * 2) + (empty * 0.1)
        return score
