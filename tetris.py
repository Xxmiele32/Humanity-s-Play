"""
El videojuego Tetris
"""
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=redefined-outer-name
# pylint: disable=consider-using-enumerate / C0200
# pylint: disable=possibly-used-before-assignment
# pylint: disable=bare-except
# Importaciones
import sys
import random
import pygame
from button import Button
pygame.init()
pygame.font.init()
# Variables Globales
s_width = 800
s_height = 700
play_width = 300
play_height = 600
block_size = 30
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
size = (s_width, s_height)
screen = pygame.display.set_mode(size)
# Assets
FondoMenu = pygame.image.load("assets/ZDR.png")
FondoMenu = pygame.transform.scale(FondoMenu, (s_width, s_height))
FondoJuego = pygame.image.load("assets/fondojuego.jpg")
FondoJuego = pygame.transform.scale(FondoJuego, (s_width, s_height))
gameover_sfx = pygame.mixer.Sound("assets/me-game-gameover-101soundboards.mp3")
harddrop_sfx = pygame.mixer.Sound("assets/se-game-harddrop-101soundboards.mp3")
landing_sfx = pygame.mixer.Sound("assets/se-game-landing-101soundboards.mp3")
rotate_sfx = pygame.mixer.Sound("assets/se-game-rotate-101soundboards.mp3")
claerrow_sfx = pygame.mixer.Sound("assets/se-game-single-101soundboards.mp3")
Bonus_sfx = pygame.mixer.Sound("assets/se-game-tetris-101soundboards.mp3")
# las formas de las figuras
S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]


shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape

class Piece(object):
    """
    Esta clase se encarga de dar la informacion mas basica al objeto
    """
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_pos={}):
    """
    Crea la matriz a donde se jugara el tetris
    """
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)] # La matriz contara de 10 columnas y 20 filas

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid

def convert_shape_format(shape):
    """
    Convierte la infromacion de la posicion en las piezas
    """
    positions = []
    format = shape.shape[shape.rotation % len (shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions

def valid_space(shape, grid):
    """
    Verifica si la posicion del jugador quiere es una posicion valida
    """
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    """
    Verifica si el jugador ha perdido
    """
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False

def get_shape():
    """
    Seleciona una pieza al azar
    """
    return Piece(5, 0, random.choice(shapes))

def draw_text_middle(text, size, color, surface):
    """
    Esta funcion sera usada para mostrar al centro de la pantlla si el jugador ha perdido
    """
    font = pygame.font.SysFont('comicsans', size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))

def draw_grid(surface, row, col):
    """
    Dibuja la matriz en la pantalla
    """
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30))  # Lineas horizontales
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height))  # Lineas verticales

def clear_rows(grid, locked):
    """
    Limpia la linea si esta llena
    """
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i 
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc

def draw_next_shape(shape, surface):
    """
    Dibuja cual sera la siguiente figura
    """
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height /2 - 100

    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*30, sy + i*block_size, block_size, block_size), 0)
    surface.blit(label, (sx + 10, sy - 50))

def draw_window(surface, grid, score=0, last_score = 0):
    """
    Crea la ventana con el titulo, el puntuaje y el maximo puntuaje
    """
    surface.blit(FondoJuego, (0,0))
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris', 1, (255,255,255))

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), 10))

    #Score Actual
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height /2 - 100

    surface.blit(label, (sx + 20, sy + 150))

    #Ultimo mejor score
    label = font.render('High Score: ' + str(last_score), 1, (255,255,255))

    sx = top_left_x - 250
    sy = top_left_y + 200

    surface.blit(label, (sx + 20, sy + 150))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j* 30, top_left_y + i * 30, 30, 30), 0)
    draw_grid(surface, 20, 10)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

def update_score(nscore):
    """
    Escribe el ultimo mejor puntuaje en el fichero .txt
    """
    score = max_score()

    with open('scores.txt', 'w', encoding="utf-8") as f:
        if int(score) > int(nscore):
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    """
    Lee cual es el mejor ultimo puntuaje del fichero ,txt
    """
    with open('scores.txt', 'r', encoding="utf-8") as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score

def collision_check(piece, grid):
    """
    Verifica si la pieza actual esta colisionando con la matriz o las piezas ya colocadas
    """
    shape_format = convert_shape_format(piece)
    for x, y in shape_format:
        if x < 0 or x >= 10 or y >= 20:
            return True
        if y >= 0 and grid[y][x] != (0, 0, 0):
            return True
    return False

def hard_drop(current_piece, grid):
    "Esta funcion permite que se pueda hacer que la pieza caiga hasta el fondo"
    while not collision_check(current_piece, grid):
        current_piece.y += 1
    current_piece.y -= 1

def get_font(size):
    """
    Desde la carpeta de assets se coge la fuente y la devuelve al remitente.
    """
    return pygame.font.Font("assets/font.ttf", size)

def main(win):
    """
    El loop principal del juego
    """
    # Creacion de variables
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0
    pygame.mixer.music.load("assets/musicajuego.mp3")
    pygame.mixer.music.play(-1)


    while run:
        grid = create_grid(locked_positions)
        pygame.display.update()
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 >5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid) and current_piece.y > 0):
                current_piece.y -= 1
                change_piece = True
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                run = False
                main_menu()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not(valid_space(current_piece, grid)):
                        current_piece.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not (valid_space(current_piece, grid)):
                        current_piece.y -= 1
                if event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    rotate_sfx.play()
                    if not (valid_space(current_piece, grid)):
                        current_piece.rotation -= 1
                if event.key == pygame.K_SPACE:
                    hard_drop(current_piece, grid)
                    harddrop_sfx.play()

        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            landing_sfx.play()
            if clear_rows(grid, locked_positions) == 4:
                score += clear_rows(grid, locked_positions) * 100
                Bonus_sfx.play()

            else:
                score += clear_rows(grid, locked_positions) * 10
                claerrow_sfx.play()

        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()

        if check_lost(locked_positions):
            run = False
            draw_text_middle("YOU LOST!", 40, (255,255,255), win)
            pygame.mixer.music.stop()
            gameover_sfx.play()
            update_score(score)
            pygame.display.update()
            pygame.time.delay(7000)

def howplay():
    """
    Menu sobre como jugar
    """
    # Cargar imagen de fondo para la ventana "howplay"
    FondoJuego = pygame.image.load("assets/fondojuego.jpg")
    FondoJuego = pygame.transform.scale(FondoJuego, (s_width, s_height))
    
    # Crear un bucle de eventos para mostrar la ventana
    while True:
        screen.blit(FondoJuego, (0, 0))  # Dibujar la imagen de fondo en la ventana
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_BUTTON = Button(image=pygame.image.load("assets/Menubutton.png"), pos=(400, 600),
                            text_input="GO HOME", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        for button in [MENU_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    main_menu()
        
        pygame.display.update()
    # Cerrar la ventana cuando se termine el bucle

def main_menu():
    """
    Esta la estetica del menu y sus botones.
    """
    pygame.mixer.music.load("assets/musicamenu.mp3")
    pygame.mixer.music.play(-1)
    while True:
        screen.blit(FondoMenu, (0, 0))



        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("Humanity's Play", True, "#4631c9")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 50))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 300),
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 450),
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HOWPLAY_BUTTON = Button(image=pygame.image.load("assets/How Play.png"), pos=(400, 600),
                            text_input="HOW TO PLAY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON, HOWPLAY_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.music.stop()
                    main(win)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                if HOWPLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    howplay(win)

        pygame.display.update()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu()  # start game
