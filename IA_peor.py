from logic import all_orientations, can_place, shapes

class WorstPlayer:
    def __init__(self, player_id):
        self.id = player_id

    def get_move(self, board, shapes_left, first_move):
        for pid in shapes_left:
            for orient in all_orientations(shapes[pid]):
                for y in range(len(board)):
                    for x in range(len(board[0])):
                        if can_place(board, (x, y), orient, self.id, first_move):
                            # simplemente devuelve la primera jugada válida (sin criterio)
                            return (pid, orient, (x, y))
        return None
