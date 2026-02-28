
import pygame
from board import Board, TILE
from moves import is_king_in_check, get_safe_moves, has_no_moves

WIDTH   = 640
HEIGHT  = 700   

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess - Altamash')
        self.clock  = pygame.time.Clock()

        self.board  = Board()
        self.board.load_images('images/')
        self.board.setup()

  
        self.turn         = 'white'
        self.picked_piece = None
        self.picked_pos   = None
        self.valid_moves  = []
        self.status       = ''

      
        self.white_score  = 0
        self.black_score  = 0

     
        self.points = {
            'P': 1, 'p': 1,
            'N': 3, 'n': 3,
            'B': 3, 'b': 3,
            'R': 5, 'r': 5,
            'Q': 9, 'q': 9,
            'K': 0, 'k': 0,
        }

    
        self.font       = pygame.font.SysFont('Arial', 20, bold=True)
        self.font_small = pygame.font.SysFont('Arial', 15)

    def run(self):
        running = True
        while running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    if my < 640 and 'CHECKMATE' not in self.status and 'STALEMATE' not in self.status:
                        self.handle_click(mx, my)

            self.draw()

        pygame.quit()

    def handle_click(self, mx, my):
        row, col    = self.board.click_to_pos(mx, my)
        clicked     = self.board.get_piece(row, col)
        clicked_pos = (row, col)

        if self.picked_piece:
            if clicked_pos in self.valid_moves:
                self.do_move(clicked_pos)
            elif clicked and clicked.color == self.turn:
                self.pick_piece(row, col)
            else:
                self.picked_piece = None
                self.board.clear_highlights()
        else:
            if clicked and clicked.color == self.turn:
                self.pick_piece(row, col)

    def pick_piece(self, row, col):
        piece = self.board.get_piece(row, col)
        self.picked_piece = piece
        self.picked_pos   = (row, col)
        self.valid_moves  = get_safe_moves(piece, self.board)
        self.board.highlight_picked((row, col))
        self.board.highlight_moves(self.valid_moves)

    def do_move(self, to_pos):
       
        tr, tc   = to_pos
        captured = self.board.get_piece(tr, tc)
        if captured:
            val = self.points.get(captured.name, 0)
            if self.turn == 'white':
                self.white_score += val
            else:
                self.black_score += val

        self.board.move_piece(self.picked_pos, to_pos)
        self.board.clear_highlights()
        self.picked_piece = None

     
        self.turn = 'black' if self.turn == 'white' else 'white'
        self.update_status()

    def update_status(self):
        in_check = is_king_in_check(self.turn, self.board)
        no_moves = has_no_moves(self.turn, self.board)

        if in_check and no_moves:
            winner = 'Black' if self.turn == 'white' else 'White'
            self.status = f'CHECKMATE!  {winner} wins!'
        elif not in_check and no_moves:
            self.status = 'STALEMATE — Draw!'
        elif in_check:
            self.status = 'CHECK!'
        else:
            self.status = ''

    def draw(self):
        self.screen.fill((40, 40, 40))
        self.board.draw(self.screen)
        self.draw_info_bar()
        pygame.display.flip()

    def draw_info_bar(self):
        BAR_Y = 640

       
        pygame.draw.rect(self.screen, (20, 20, 20), (0, BAR_Y, WIDTH, 60))

       
        pygame.draw.line(self.screen, (60, 60, 60), (0, BAR_Y), (WIDTH, BAR_Y), 1)

        black_label = self.font_small.render('Black', True, (170, 170, 170))
        black_score = self.font.render(str(self.black_score), True, (220, 220, 220))
        self.screen.blit(black_label, (18, BAR_Y + 8))
        self.screen.blit(black_score, (18, BAR_Y + 30))

        if self.status:
            color = (255, 80, 80) if 'CHECKMATE' in self.status else (255, 210, 0)
            msg   = self.font.render(self.status, True, color)
        else:
            label = self.turn.capitalize() + "'s Turn"
            color = (255, 255, 255) if self.turn == 'white' else (160, 160, 160)
            msg   = self.font.render(label, True, color)

        msg_x = (WIDTH - msg.get_width()) // 2
        self.screen.blit(msg, (msg_x, BAR_Y + 20))

       
        white_label = self.font_small.render('White', True, (170, 170, 170))
        white_score = self.font.render(str(self.white_score), True, (255, 255, 255))
        self.screen.blit(white_label, (WIDTH - white_label.get_width() - 18, BAR_Y + 8))
        self.screen.blit(white_score, (WIDTH - white_score.get_width() - 18, BAR_Y + 30))
