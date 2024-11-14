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
import time
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
energy_bar_images = [pygame.image.load(f"assets/barra_energia_{i}.png") for i in range(4)]
gameover_sfx = pygame.mixer.Sound("assets/me-game-gameover-101soundboards.mp3")
harddrop_sfx = pygame.mixer.Sound("assets/se-game-harddrop-101soundboards.mp3")
landing_sfx = pygame.mixer.Sound("assets/se-game-landing-101soundboards.mp3")
rotate_sfx = pygame.mixer.Sound("assets/se-game-rotate-101soundboards.mp3")
claerrow_sfx = pygame.mixer.Sound("assets/se-game-single-101soundboards.mp3")
Bonus_sfx = pygame.mixer.Sound("assets/se-game-tetris-101soundboards.mp3")
Bonus_music = pygame.mixer.Sound("assets/bonus.mp3")
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

def hold_piece(held_piece, current_piece, next_piece, can_hold):
    # Todo:
    # Las piezas despues de guardarlas se colocan donde les da la regalada gana
    # Si vas muy rapido las piezas se fusionan
    """
    Esta funcion se encarga de guardar la figura
    """
    if not can_hold:
        return held_piece, current_piece, next_piece, can_hold

    if held_piece is None:
        held_piece = current_piece
        current_piece = next_piece
        next_piece = get_shape()
    else:
        current_piece, held_piece = held_piece, current_piece

    current_piece.x, current_piece.y = 5, 0

    can_hold = False
    return held_piece, current_piece, next_piece, can_hold

def draw_held_piece(held_piece, surface):
    """
    Dibuja la pieza en la reserva en la interfaz del juego.
    """
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Held Piece', 1, (255,255,255))

    sx = top_left_x - 150  # Ubicación de la pieza en la pantalla
    sy = top_left_y + play_height / 2 - 100

    surface.blit(label, (sx + 10, sy - 50))

    if held_piece is not None:
        format = held_piece.shape[held_piece.rotation % len(held_piece.shape)]
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, held_piece.color, (sx + j * 30, sy + i * block_size, block_size, block_size), 0)

def update_energy_bar(screen, energy_level):
    """Actualiza la barra de energía en función del nivel."""
    image_index = min(energy_level // 2, 3)
    screen.blit(energy_bar_images[image_index], (1,1))

def activate_bonus():
    """Activa el bono con doble puntaje."""
    print("Bonus activado")
    double_points = True
    bonus_active = True
    bonus_end_time = time.time() + 10  # Duración de 10 segundos
    draw_text_middle("BONUS TIME!", 40, (255, 255, 255), win)
    pygame.mixer.music.stop()
    Bonus_music.play()
    return double_points, bonus_active, bonus_end_time

def handle_bonus(bonus_active, bonus_end_time):
    """Controla el tiempo de duración del bono."""
    if bonus_active and time.time() >= bonus_end_time:
        print("Se ha acabado el bonus")
        Bonus_music.stop()
        pygame.mixer.music.play(-1)
        return False, None  # Desactiva el bono
    return True, bonus_end_time

# Example of diagnostic prints to investigate rows_cleared and energy_level issues

def debug_main(win):
    """
    Main game loop with added debug statements to investigate energy_level updates.
    """
    # Initialization
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)
    rows_cleared = 0
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0
    energy_level = 0
    double_points = False
    bonus_active = False
    bonus_end_time = None
    held_piece = None
    can_hold = True
    pygame.mixer.music.load("assets/musicajuego.mp3")
    pygame.mixer.music.play(-1)

    while run:
        grid = create_grid(locked_positions)
        pygame.display.update()
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        # Piece falls over time
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid) and current_piece.y > 0):
                current_piece.y -= 1
                change_piece = True

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                run = False
                main_menu()

            # Key Controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    rotate_sfx.play()
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1
                elif event.key == pygame.K_SPACE:
                    can_hold = False
                    hard_drop(current_piece, grid)
                    harddrop_sfx.play()
                elif event.key == pygame.K_r:
                    if can_hold:
                        held_piece, current_piece, next_piece, can_hold = hold_piece(
                            held_piece, current_piece, next_piece, can_hold
                        )
                elif event.key == pygame.K_g and energy_level >= 1 and not bonus_active:
                    double_points, bonus_active, bonus_end_time = activate_bonus()
                    energy_level = 0  # Reset energy bar

        # Place the current piece on the grid
        shape_pos = convert_shape_format(current_piece)
        for x, y in shape_pos:
            if y > -1:
                grid[y][x] = current_piece.color
        if change_piece:
            for pos in shape_pos:
                locked_positions[(pos[0], pos[1])] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            can_hold = True
            change_piece = False
            landing_sfx.play()

            # Clear rows after placing the piece
            rows_cleared = clear_rows(grid, locked_positions)
            print(f"Debug: Rows cleared = {rows_cleared}")  # Debug print to check rows cleared
            
            if rows_cleared > 0:
                points_to_add = rows_cleared * (100 if rows_cleared == 4 else 10)
                if double_points:
                    points_to_add *= 2
                score += points_to_add
                (Bonus_sfx if rows_cleared == 4 else claerrow_sfx).play()
                
                # Update energy level and print to verify increment
                prev_energy = energy_level  # Track previous energy level for comparison
                energy_level = min(energy_level + max(1, rows_cleared // 2), 7)
                print(f"Debug: Previous energy level = {prev_energy}, New energy level = {energy_level}")  # Debug print

        # Draw the window and update display
        draw_window(win, grid, score, last_score)
        update_energy_bar(win, energy_level)
        draw_next_shape(next_piece, win)
        draw_held_piece(held_piece, win)
        pygame.display.update()

        # Handle bonus duration
        if bonus_active:
            bonus_active, bonus_end_time = handle_bonus(bonus_active, bonus_end_time)
            if not bonus_active:
                double_points = False  # Deactivate double points when bonus ends

        # Check for game over
        if check_lost(locked_positions):
            run = False
            draw_text_middle("YOU LOST!", 40, (255, 255, 255), win)
            pygame.mixer.music.stop()
            gameover_sfx.play()
            update_score(score)
            pygame.display.update()
            pygame.time.delay(7000)

    pygame.display.flip()
    pygame.time.delay(100)

# Note: This code adds debug print statements for rows_cleared and energy_level values.
# It is not executable in this environment, but can be run in a local Pygame environment for testing.


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
                    debug_main(win)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                if HOWPLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    howplay()

        pygame.display.update()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

main_menu()  # start game