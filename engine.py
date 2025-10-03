from logic import make_board

class GameEngine:
    def __init__(self, players, shapes):

        if not players:
            raise ValueError("Debes pasar al menos un jugador")
        self.players = list(players)
        self.num_players = len(self.players)
        self.player_idx = 0                     # índice dentro de self.players
        self.current_player = self.players[0]   # id del jugador actual

        self.board = make_board()               # 20x20 desde logic
        self.shapes = shapes

        # primer movimiento por jugador
        self.first_move = {pid: True for pid in self.players}

        #  piezas usadas por jugador
        self.used_pieces = {pid: set() for pid in self.players}

    #  turnos ---
    def get_current_player(self):
        return self.current_player

    def advance_turn(self):
        self.player_idx = (self.player_idx + 1) % self.num_players
        self.current_player = self.players[self.player_idx]

    # --- primer movimiento ---
    def is_first_move(self, pid=None):
        pid = pid or self.current_player
        return self.first_move.get(pid, False)

    def mark_first_move_done(self, pid=None):
        pid = pid or self.current_player
        if pid in self.first_move:
            self.first_move[pid] = False

    #  marcar pieza usada
    def mark_piece_used(self, pid, piece_id):
        self.used_pieces.setdefault(pid, set()).add(piece_id)
    # marcar como ya usada
    def has_used_piece(self, pid, piece_id):
        return piece_id in self.used_pieces.get(pid, set())



