
class Piece:
    """base class - every chess piece inherits from this"""

    def __init__(self, color, row, col):
        self.color    = color     
        self.row      = row
        self.col      = col
        self.moved    = False      
        self.name     = ''         

    def get_moves(self, board):
        """each piece overrides this to return list of (row,col) it can move to"""
        raise NotImplementedError

    def is_enemy(self, other):
        """is the other piece an opponent?"""
        return other is not None and other.color != self.color

    def on_board(self, r, c):
        return 0 <= r < 8 and 0 <= c < 8

    def slide(self, board, directions):
        """helper for pieces that slide (rook, bishop, queen)"""
        moves = []
        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            while self.on_board(r, c):
                if board[r][c] is None:
                    moves.append((r, c))
                else:
                    if self.is_enemy(board[r][c]):
                        moves.append((r, c))  # capture then stop
                    break
                r += dr
                c += dc
        return moves


class Pawn(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.name = 'P' if color == 'white' else 'p'

    def get_moves(self, board):
        moves = []
        r, c  = self.row, self.col
     
        direction = -1 if self.color == 'white' else 1


        if self.on_board(r + direction, c) and board[r + direction][c] is None:
            moves.append((r + direction, c))

            
            start_row = 6 if self.color == 'white' else 1
            if r == start_row and board[r + 2 * direction][c] is None:
                moves.append((r + 2 * direction, c))

       
        for dc in [-1, 1]:
            nr, nc = r + direction, c + dc
            if self.on_board(nr, nc) and self.is_enemy(board[nr][nc]):
                moves.append((nr, nc))

        return moves


class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.name = 'R' if color == 'white' else 'r'

    def get_moves(self, board):
        return self.slide(board, [(-1,0),(1,0),(0,-1),(0,1)])


class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.name = 'N' if color == 'white' else 'n'

    def get_moves(self, board):
        moves = []
        jumps = [(-2,-1),(-2,1),(-1,-2),(-1,2),
                 ( 1,-2),( 1,2),( 2,-1),( 2,1)]
        for dr, dc in jumps:
            nr, nc = self.row + dr, self.col + dc
            if self.on_board(nr, nc):
                if board[nr][nc] is None or self.is_enemy(board[nr][nc]):
                    moves.append((nr, nc))
        return moves


class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.name = 'B' if color == 'white' else 'b'

    def get_moves(self, board):
        return self.slide(board, [(-1,-1),(-1,1),(1,-1),(1,1)])


class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.name = 'Q' if color == 'white' else 'q'

    def get_moves(self, board):
      
        all_dirs = [(-1,0),(1,0),(0,-1),(0,1),
                    (-1,-1),(-1,1),(1,-1),(1,1)]
        return self.slide(board, all_dirs)


class King(Piece):
    def __init__(self, color, row, col):
        super().__init__(color, row, col)
        self.name = 'K' if color == 'white' else 'k'

    def get_moves(self, board):
        moves = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = self.row + dr, self.col + dc
                if self.on_board(nr, nc):
                    if board[nr][nc] is None or self.is_enemy(board[nr][nc]):
                        moves.append((nr, nc))
        return moves