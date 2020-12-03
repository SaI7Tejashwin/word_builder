import pygame

TILESIZE = 32
BOARD_POS = (250, 125)



def create_grid() :
    board_surf = pygame.Surface((TILESIZE*10 , TILESIZE*10))
    green = False
    for y in range(10):
        for x in range(10):
            rect = pygame.Rect(x*TILESIZE, y*TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(board_surf, pygame.Color('green' if green else 'yellow'), rect)
            green = not green
        green = not green
    return board_surf

def create_board():
    board = []
    for y in range(10):
        board.append([])
        for x in range(10):
            board[y].append(None)

    for x in range(10):
        board[0][x] = ('red', 'player1')
        board[9][x] = ('blue', 'player2')
    return board

def get_square_under_mouse(board):
    mouse_pos = pygame.Vector2(pygame.mouse.get_pos()) - BOARD_POS
    x, y = [int(v // TILESIZE) for v in mouse_pos]
    try: 
        if x >= 0 and y >= 0: return (board[y][x], x, y)
    except IndexError: pass
    return None, None, None

def draw_letters(screen, board, font, selected_piece):
    sx, sy = None, None
    if selected_piece:
        letter,sx, sy = selected_piece

    for y in range(10):
        for x in range(10):
            letter = board[y][x]
            if letter:
                selected = x == sx and y == sy
                s1 = font.render('p', True, pygame.Color('red' if selected else 'black'))
                s2 = font.render('p', True, pygame.Color('darkgrey'))
                pos = pygame.Rect(BOARD_POS[0] + x * TILESIZE+1, BOARD_POS[1] + y * TILESIZE + 1, TILESIZE, TILESIZE)
                screen.blit(s2, s2.get_rect(center=pos.center).move(1, 1))
                screen.blit(s1, s1.get_rect(center = pos.center))

def draw_selector(screen, letter , x, y):
    if letter != None:
        rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
        pygame.draw.rect(screen, (255, 0, 0, 50), rect, 2)

def draw_drag(screen, board, selected_piece, font):
    if selected_piece:
        letter, x, y = get_square_under_mouse(board)
        if x != None:
            rect = (BOARD_POS[0] + x * TILESIZE, BOARD_POS[1] + y * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(screen, (0, 255, 0, 50), rect, 2)

        color, type = selected_piece[0]
        s1 = font.render(type[0], True, pygame.Color(color))
        s2 = font.render(type[1], True, pygame.Color('darkgrey'))
        pos = pygame.Vector2(pygame.mouse.get_pos())
        screen.blit(s2, s2.get_rect(center=pos + (1,1)))
        screen.blit(s1, s1.get_rect(center=pos))
        selected_rect = pygame.Rect(BOARD_POS[0] + selected_piece[1] * TILESIZE, BOARD_POS[1] + selected_piece[2] * TILESIZE, TILESIZE, TILESIZE)
        return (x, y)

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 500))
    clock = pygame.time.Clock()
    board = create_board()
    board_surf = create_grid()
    font = pygame.font.SysFont('', 32)
    selected_piece = None
    drop_pos = None
    while True:
        letter, x, y = get_square_under_mouse(board)
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if letter != None:
                    selected_piece = letter , x, y
            if e.type == pygame.MOUSEBUTTONUP:
                if drop_pos:
                    letter, old_x, old_y = selected_piece
                    board[old_x][old_y] = 0
                    new_x, new_y = drop_pos
                    board[new_y][new_x] = letter
                selected_piece = None
                drop_pos = None
        
        screen.fill(pygame.Color('grey'))
        screen.blit(board_surf, BOARD_POS)
        draw_letters(screen, board, font, selected_piece)
        draw_selector(screen, letter, x, y)
        drop_pos = draw_drag(screen, board, selected_piece, font)

        pygame.display.flip()
        clock.tick(60)
if __name__ == '__main__':
    main()