

def is_king_in_check(color, board):
    """is the king of given color currently in check?"""
    
    king_pos = None
    for r in range(8):
        for c in range(8):
            p = board.grid[r][c]
            if p and p.name in ('K', 'k') and p.color == color:
                king_pos = (r, c)

    if not king_pos:
        return False

   
    enemy = 'black' if color == 'white' else 'white'
    for r in range(8):
        for c in range(8):
            p = board.grid[r][c]
            if p and p.color == enemy:
                if king_pos in p.get_moves(board.grid):
                    return True
    return False


def get_safe_moves(piece, board):
    """filter moves that would leave own king in check"""
    safe = []
    from_pos = (piece.row, piece.col)

    for to_pos in piece.get_moves(board.grid):
        tr, tc = to_pos
        fr, fc = from_pos

       
        captured = board.grid[tr][tc]
        board.grid[tr][tc] = piece
        board.grid[fr][fc] = None
        piece.row, piece.col = tr, tc

        still_in_check = is_king_in_check(piece.color, board)

  
        board.grid[fr][fc] = piece
        board.grid[tr][tc] = captured
        piece.row, piece.col = fr, fc

        if not still_in_check:
            safe.append(to_pos)

    return safe


def has_no_moves(color, board):
    """does this color have zero legal moves left?"""
    for r in range(8):
        for c in range(8):
            p = board.grid[r][c]
            if p and p.color == color:
                if get_safe_moves(p, board):
                    return False
    return True