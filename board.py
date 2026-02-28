
import pygame
from pieces import Pawn, Rook, Knight, Bishop, Queen, King

TILE      = 80    
ROWS      = 8
COLS      = 8


LIGHT     = (240, 217, 181)
DARK      = (181, 136,  99)
YELLOW    = (246, 246, 105, 180)   
GREEN     = (130, 151, 105, 180)  


class Board:
    def __init__(self):
        self.grid          = [[None] * COLS for _ in range(ROWS)]
        self.images        = {}       
        self.hint_squares  = []      
        self.picked_square = None    

    def setup(self):
        """put all pieces in starting positions"""
        self.grid = [[None] * COLS for _ in range(ROWS)]

        back = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for c, PieceClass in enumerate(back):
            self.grid[0][c] = PieceClass('black', 0, c)
            self.grid[7][c] = PieceClass('white', 7, c)

    
        for c in range(COLS):
            self.grid[1][c] = Pawn('black', 1, c)
            self.grid[6][c] = Pawn('white', 6, c)

    def load_images(self, folder='images/'):
        """load piece PNGs from the images folder"""
       
        keys = ['wK','wQ','wR','wB','wN','wP',
                'bK','bQ','bR','bB','bN','bP']
        for key in keys:
            try:
                img = pygame.image.load(f'{folder}{key}.png')
                self.images[key] = pygame.transform.scale(img, (TILE, TILE))
            except:
                print(f'missing image: {key}.png')

    def get_image_key(self, piece):
        col = 'w' if piece.color == 'white' else 'b'
        name_map = {
            'K': 'K', 'k': 'K',
            'Q': 'Q', 'q': 'Q',
            'R': 'R', 'r': 'R',
            'B': 'B', 'b': 'B',
            'N': 'N', 'n': 'N',
            'P': 'P', 'p': 'P',
        }
        return col + name_map[piece.name]

    def draw(self, screen):
        """draw squares then highlights then pieces"""
       
        for r in range(ROWS):
            for c in range(COLS):
                color = LIGHT if (r + c) % 2 == 0 else DARK
                pygame.draw.rect(screen, color, (c*TILE, r*TILE, TILE, TILE))

       
        if self.picked_square:
            r, c = self.picked_square
            surf = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
            surf.fill(YELLOW)
            screen.blit(surf, (c*TILE, r*TILE))

     
        for r, c in self.hint_squares:
            surf = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
            surf.fill(GREEN)
            screen.blit(surf, (c*TILE, r*TILE))

        
        for r in range(ROWS):
            for c in range(COLS):
                piece = self.grid[r][c]
                if piece:
                    key = self.get_image_key(piece)
                    if key in self.images:
                        screen.blit(self.images[key], (c*TILE, r*TILE))

    def get_piece(self, row, col):
        return self.grid[row][col]

    def set_piece(self, row, col, piece):
        self.grid[row][col] = piece
        if piece:
            piece.row = row
            piece.col = col

    def move_piece(self, from_pos, to_pos):
        fr, fc = from_pos
        tr, tc = to_pos
        piece = self.grid[fr][fc]
        if not piece:
            return
        self.grid[tr][tc]  = piece
        self.grid[fr][fc]  = None
        piece.row   = tr
        piece.col   = tc
        piece.moved = True

    def highlight_moves(self, moves):
        self.hint_squares = moves

    def highlight_picked(self, pos):
        self.picked_square = pos

    def clear_highlights(self):
        self.hint_squares  = []
        self.picked_square = None

    def click_to_pos(self, mouse_x, mouse_y):
        return mouse_y // TILE, mouse_x // TILE