import random
from copy import deepcopy
from logic import can_place, place, all_orientations, shapes, GRID_SIZE

class RandomAI:
    def __init__(self, player_id, engine):
        self.id = player_id
        self.engine = engine

    def get_move(self):
        board = self.engine.board
        first_move = self.engine.is_first_move(self.id)

        # piezas que aun no se usan
        shapes_left = [
            sid for sid in self.engine.shapes.keys()
            if not self.engine.has_used_piece(self.id, sid)
        ]

        random.shuffle(shapes_left)  # liga las piezas

        for piece_id in shapes_left:
            orientations = all_orientations(shapes[piece_id])
            random.shuffle(orientations)

            coords = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
            random.shuffle(coords)

            for orient in orientations:
                for coord in coords:
                    if can_place(board, coord, orient, self.id, first_move):
                        return (piece_id, orient, coord)

        # si no hay jugadas
        return None
