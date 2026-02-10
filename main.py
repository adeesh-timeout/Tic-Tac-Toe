import pygame
import os
import random

# Change Directory # Random Error 01
os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()
pygame.font.init()

run = True
FPS = 30

current_player = random.choice('XO')

BOX_HEIGHT = 100
BOX_WIDTH = BOX_HEIGHT+10
RAD = 10
GAP = 10
ROW = 3
COLUMN = 3
BOARD_WIDTH = (BOX_WIDTH+GAP)*COLUMN + GAP
BOARD_HEIGHT = (BOX_HEIGHT+GAP)*ROW + GAP

is_won = None
check_win = False
winner_box_pos = []
delay_count = 0

SCREEN_WIDTH = BOARD_WIDTH
SCREEN_HEIGHT = BOARD_HEIGHT 

X_IMG = pygame.transform.smoothscale(pygame.image.load('X_img.png'), (80, 80))
O_IMG = pygame.transform.smoothscale(pygame.image.load('O_img.png'), (95, 95))
ICON = pygame.image.load('tic_icon.png')

BOX_MOUSE_POS = [()]

player_pos = [              # Access -> [row][col]
              ["","",""],   # [0][0,1,2]
              ["","",""],
              ["","",""]
             ]

box_colors = []
for _ in range(ROW):
    box_colors.append([])
    for _ in range(COLUMN):
        box_colors[-1].append((0, 36, 100))

markers_list = []
markers_list_count = 0

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('Tic Tac Toe')
pygame.display.set_icon(ICON)
clock = pygame.time.Clock()

class Marker():
    def __init__(self, x, y, pos, marker):
        self.x = x
        self.y = y
        self.marker = marker
        self.pos = tuple(pos)

        player_pos[pos[0]][pos[1]] = self.marker

    def redraw(self):
        if self.marker == 'X':
            screen.blit(X_IMG, (self.x+15, self.y+10))
        else:
            screen.blit(O_IMG, (self.x+8, self.y+3))
        
def draw_board():
    pygame.draw.rect(screen, (0, 104, 199), (0,0, BOARD_WIDTH, BOARD_HEIGHT)) #BG

    for row_n in range(1, ROW+1):
        for col_n in range(1, COLUMN+1):
            box_x = GAP*col_n + BOX_WIDTH*(col_n-1)
            box_y = GAP*row_n + BOX_HEIGHT*(row_n-1)

            pygame.draw.rect(screen, box_colors[row_n-1][col_n-1], (box_x, box_y, BOX_WIDTH,BOX_HEIGHT), border_radius=RAD)
            if BOX_MOUSE_POS[-1] != ('DONE'):
                BOX_MOUSE_POS.append((box_x, box_y, row_n-1, col_n-1))

    if BOX_MOUSE_POS[-1] != ('DONE'):
        BOX_MOUSE_POS.append(('DONE'))

def add_piece():
    global current_player, markers_list_count, is_won

    if pygame.mouse.get_pressed()[0]:
        mouse_pos = pygame.mouse.get_pos()
        for pos in BOX_MOUSE_POS[1:-1]:
            if (pos[0]< mouse_pos[0] < pos[0]+BOX_WIDTH) and pos[1] < mouse_pos[1] < pos[1]+BOX_HEIGHT and player_pos[pos[2]][pos[3]] == '' and is_won == None:
                markers_list.append(Marker(pos[0], pos[1], (pos[2], pos[3]), current_player))
                markers_list_count += 1

                if markers_list_count >= 5: detect_win(current_player)
                if current_player == 'X': current_player = 'O'
                else: current_player = 'X'
    
    if markers_list_count == ROW*COLUMN and is_won == None:
        is_won = 'D'

    # Update/Redraw
    for marker in markers_list:
        marker.redraw()

def detect_win(current_player):
    global is_won, winner_box_pos
    # Diagonals
    if current_player == player_pos[0][0] != '':
        if current_player == player_pos[1][1]:
            if current_player == player_pos[2][2]:
                is_won = current_player
                winner_box_pos = [(0,0),(1,1),(2,2)]

    if current_player == player_pos[0][-1] != '':
        if current_player == player_pos[1][-2]:
            if current_player == player_pos[2][-3]:
                is_won = current_player
                winner_box_pos = [(0,2), (1,1), (2,0)]

    # Horizontal and Vertical
    print(winner_box_pos)
    if is_won == None:
        for row_n in range(ROW): # 0, 1, 2
            winner_box_pos = [(row_n, 0)]

            for col_n in range(1, COLUMN):
                if player_pos[row_n][col_n-1] == player_pos[row_n][col_n] != '':
                    winner_box_pos.append((row_n, col_n))

                else: winner_box_pos = []
        
            if len(winner_box_pos) == 3 and is_won == None:
                is_won = current_player
                break

            if player_pos[0][row_n] == player_pos[1][row_n] == player_pos[2][row_n] != '' and is_won == None: # Since Row == Col, Dangerous, Unreliable
                if is_won == None:
                    is_won = current_player
                    winner_box_pos = [(0,row_n),(1,row_n),(2,row_n)]
                    break

def process_won():
    global box_colors, delay_count
    for pos in winner_box_pos:
        box_colors[pos[0]][pos[1]] = (251, 173, 24)

    if delay_count >= 30:
        pygame.draw.rect(screen, 'black', (0, 120, SCREEN_WIDTH, 100))

        if is_won == 'X':    
            text = font_1.render(f"{is_won} Won", True, (24, 187, 156))
            screen.blit(text, (SCREEN_WIDTH//2-60,130))
            text = font_2.render("Press Enter to Restart", True, (24, 187, 156))
            screen.blit(text, (SCREEN_WIDTH//2-165,170))

        elif is_won == 'O':
            text = font_1.render(f"{is_won} Won", True, (236, 103, 120))
            screen.blit(text, (SCREEN_WIDTH//2-60,130))
            text = font_2.render("Press Enter to Restart", True, (236, 103, 120))
            screen.blit(text, (SCREEN_WIDTH//2-165,170))

        elif is_won == 'D':
            text = font_1.render("Draw", True, 'white')
            screen.blit(text, (SCREEN_WIDTH//2-40,130))
            text = font_2.render("Press Enter to Restart", True, 'white')
            screen.blit(text, (SCREEN_WIDTH//2-165,170))

        keys = pygame.key.get_pressed()

        if keys[pygame.K_RETURN]:
            reset()

    else:
        delay_count += 1

def reset():
    global current_player, is_won, check_win, winner_box_pos, player_pos, box_colors, markers_list, markers_list_count, delay_count

    current_player = random.choice('XO')
    is_won = None
    check_win = False
    winner_box_pos = []
    delay_count = 0
    player_pos = [
              ["","",""],
              ["","",""],
              ["","",""]
             ]
    
    box_colors = []
    for _ in range(ROW):
        box_colors.append([])
        for _ in range(COLUMN):
            box_colors[-1].append((0, 36, 100))

    markers_list = []
    markers_list_count = 0

font_1 = pygame.font.SysFont('Courier New', 40)
font_2 = pygame.font.SysFont('Courier New', 25)

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    draw_board()
    add_piece()

    if is_won:
        process_won()

    clock.tick(FPS)
    pygame.display.update()