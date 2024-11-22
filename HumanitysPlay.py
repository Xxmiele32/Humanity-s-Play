"""
El videojuego Humanity's Play
"""
# pylint: disable=invalid-name
# pylint: disable=no-member
# pylint: disable=redefined-outer-name
# pylint: disable=consider-using-enumerate / C0200
# pylint: disable=possibly-used-before-assignment
# pylint: disable=bare-except
# pylint: disable=line-too-long
# Importaciones
import sys
import random
import time
import os
import json
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
probabilidad = 30
unlocked_scenarios = set()
top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
size = (s_width, s_height)
screen = pygame.display.set_mode(size)
current_scenario = 0
# Assetss
FondoMenu = pygame.image.load("assets/ZDR.png")
FondoMenu = pygame.transform.scale(FondoMenu, (s_width, s_height))
FondoJuego = pygame.image.load("assets/fondojuego.jpg")
FondoJuego = pygame.transform.scale(FondoJuego, (s_width, s_height))
Escenario1 = pygame.image.load("assets/fondoacuatico.jpg")
Escenario2 = pygame.image.load("assets/fondodesertico.jpg")
Escenario3 = pygame.image.load("assets/fondourbano.jpg")
energy_bar_images = [pygame.transform.scale(pygame.image.load(f"assets/barra_energia_{i}.png"),(s_width -300, s_height))for i in range(8)]
gameover_sfx = pygame.mixer.Sound("assets/lose.mp3")
harddrop_sfx = pygame.mixer.Sound("assets/colocacionrapida.mp3")
landing_sfx = pygame.mixer.Sound("assets/colocacionpieza.mp3")
rotate_sfx = pygame.mixer.Sound("assets/rotate.mp3")
claerrow_sfx = pygame.mixer.Sound("assets/1linea.mp3")
Bonus_sfx = pygame.mixer.Sound("assets/4lineas.mp3")
Button_sfx = pygame.mixer.Sound("assets/button.mp3")
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

BOMERANG = [['.....',
             '.....',
             '..00.',
             '.00..',
             '.0...',
             '.....'],
            ['.....',
             '.....',
             '.00..',
             '..00.',
             '...0.',
             '.....'],
            ['.....',
             '.....',
             '...0.',
             '..00.',
             '.00..',
             '.....'],
            ['.....',
             '.....',
             '.0...',
             '.00..',
             '..00.',
             '.....']]
UNO = [['.....',
        '.....',
        '.....',
        '..0..',
        '.....',
        '.....']]

H = [['.....',
      '.....',
      '..00.',
      '...0.',
      '.....'],
     ['.....',
      '.....',
      '...0.',
      '..00.',
      '.....'],
      ['.....',
      '.....',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '..00.',
      '..0..',
      '.....']]

CRUZ = [['.....',
          '.0...',
          '..0..',
          '.....',
          '.....'],
         ['.....',
          '..0..',
          '.0...',
          '.....',
          '.....']]

TRES = [['.....',
         '.....',
         '..0..',
         '.0...',
         '..0..',
         '.....'],
        ['.....',
         '.....',
         '..0..',
         '.0.0.',
         '.....',
         '.....'],
        ['.....',
         '.....',
         '..0..',
         '...0.',
         '..0..',
         '.....'],
        ['.....',
         '.....',
         '.....',
         '.0.0.',
         '..0..',
         '.....']]


DOS = [['.....',
        '.0...',
        '.0...',
        '.....',
        '.....'],
       ['.....',
        '.....',
        '.00..',
        '.....',
        '.....']]



shapes = [S, Z, I, O, J, L, T, BOMERANG, H, UNO, CRUZ, TRES, DOS]
shape_colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (128, 0, 128),(255, 165, 0), (64, 224, 208), (100, 149, 237), (255, 192, 203), (128, 128, 128), (0, 128, 128), (255, 255, 255),(123, 104, 238), (186, 85, 211), (70, 130, 180), (255, 69, 0), (154, 205, 50), (47, 79, 79)]

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
    Crea la matriz a donde se jugara Humanity's Play
    """
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]
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


def get_shape(probabilities):
    """
    Genera una nueva pieza basada en probabilidades ajustadas.W
    """
    pieces = []

    # Construir una lista ponderada según las probabilidades ajustadas
    for piece, prob in probabilities.items():
        pieces.extend([piece] * int(prob * 100)) 

    # Elegir una pieza aleatoria de la lista ponderada
    selected_piece = random.choice(pieces)

    # Crear y devolver la estructura de la pieza según tu lógica actual
    if selected_piece == "T":
        return Piece(5, 0, T)
    elif selected_piece == "L":
        return Piece(5, 0, L)
    elif selected_piece == "I":
        return Piece(5, 0, I)
    elif selected_piece == "J":
        return Piece(5, 0, J)
    elif selected_piece == "S":
        return Piece(5, 0, S)
    elif selected_piece == "Z":
        return Piece(5, 0, Z)
    elif selected_piece == "O":
        return Piece(5, 0, O)
    elif selected_piece == "BOMERANG":
        return Piece(5, 0, BOMERANG)
    elif selected_piece == "H":
        return Piece(5, 0, H)
    elif selected_piece == "UNO":
        return Piece(5, 0, UNO)
    elif selected_piece == "CRUZ":
        return Piece(5, 0, CRUZ)
    elif selected_piece == "TRES":
        return Piece(5, 0, TRES)
    elif selected_piece == "DOS":
        return Piece(5, 0, DOS)


def draw_text_middle(text, size, color, surface):
    """
    Esta funcion sera usada para mostrar texto al centro de la pantalla
    """
    font = pygame.font.SysFont('Impact', size, bold=False)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), top_left_y + play_height/2 - label.get_height()/2))

def draw_grid(surface, row, col):
    """
    Dibuja la matriz en la pantalla
    """
    sx = top_left_x
    sy = top_left_y
    for i in range(row):
        pygame.draw.line(surface, (128,128,128), (sx, sy+ i*30), (sx + play_width, sy + i * 30)) 
        for j in range(col):
            pygame.draw.line(surface, (128,128,128), (sx + j * 30, sy), (sx + j * 30, sy + play_height)) 

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
    font = pygame.font.SysFont('Impact', 30)
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

def draw_window(surface, grid, current_scenario, score=0, last_score = 0):
    """
    Crea la ventana con el titulo, el puntuaje y el maximo puntuaje
    """
    backgrounds = {
        0: pygame.image.load("assets/ZDR.png"),
        1: pygame.image.load("assets/fondoacuatico.jpg"),
        2: pygame.image.load("assets/fondodesertico.jpg"),
        3: pygame.image.load("assets/fondourbano.jpg")
    }
    background_image = backgrounds.get(current_scenario)
    background_image = pygame.transform.scale(background_image, (s_width, s_height))
    surface.blit(background_image, (0,0))
    pygame.font.init()
    font = pygame.font.SysFont('Impact', 60)
    label = font.render("Humanity's Play", 1, (255,255,255))

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width() / 2), 10))

    #Puntuaje Actual
    font = pygame.font.SysFont('Impact', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height /2 - 100

    surface.blit(label, (sx + 20, sy + 150))

    #Ultimo mejor puntuaje
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
    """
    Esta funcion se encarga de guardar la figura
    """
    if not can_hold:
        return held_piece, current_piece, next_piece, can_hold

    if held_piece is None:
        held_piece = current_piece
        current_piece = next_piece
        next_piece = get_shape(adjusted_piece_probabilities)
    else:
        current_piece, held_piece = held_piece, current_piece

    current_piece.x, current_piece.y = 5, 0

    can_hold = False
    return held_piece, current_piece, next_piece, can_hold

def draw_held_piece(held_piece, surface):
    """
    Dibuja la pieza en la reserva en la interfaz del juego.
    """
    font = pygame.font.SysFont('Impact', 30)
    label = font.render('Held Piece', 1, (255,255,255))

    sx = top_left_x - 150 
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
    image_index = max(0, min(len(energy_bar_images) - 1, energy_level - 1))
    screen.blit(energy_bar_images[image_index], (-130,300))

def activate_bonus(shop_data):
    """Activa el bono con doble puntaje."""
    print("Bonus activado")
    double_points = True
    bonus_active = True
    bonus_end_time = time.time() + 15 + shop_data["bonus_time"] * 5 
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/bonus.mp3")
    pygame.mixer.music.play(-1)
    return double_points, bonus_active, bonus_end_time

def handle_bonus(bonus_active, bonus_end_time):
    """Controla el tiempo de duración del bono."""
    if bonus_active and time.time() >= bonus_end_time:
        print("Se ha acabado el bonus")
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/musicajuego.mp3")
        pygame.mixer.music.play(-1)
        return False, None
    return True, bonus_end_time


def main_loop(win, player_points, shop_data, unlocked_scenarios, adjusted_piece_probabilities, current_scenario):
    """
    Bucle principal del juego con declaraciones de depuración añadidas para investigar las actualizaciones del nivel de energía.
    """
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)
    rows_cleared = 0
    change_piece = False
    run = True
    current_piece = get_shape(adjusted_piece_probabilities)
    next_piece = get_shape(adjusted_piece_probabilities)
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score = 0
    energy_level = 1
    double_points = False
    bonus_active = False
    bonus_end_time = None
    held_piece = None
    can_hold = True
    paused = False
    pygame.mixer.music.load("assets/musicajuego.mp3")
    pygame.mixer.music.play(-1)

    while run:
        grid = create_grid(locked_positions)
        pygame.display.update() 
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()
        if level_time / 1000 > 5:
            level_time = 0
            if fall_speed > 0.12:
                fall_speed -= 0.005

        if fall_time / 1000 > fall_speed and not paused:
            fall_time = 0
            current_piece.y += 1
            if not (valid_space(current_piece, grid) and current_piece.y > 0):
                current_piece.y -= 1
                change_piece = True
                change_piece = True

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                run = False
                save_game(player_points, shop_data, unlocked_scenarios)
                main_menu(player_points, shop_data, unlocked_scenarios, adjusted_piece_probabilities, current_scenario)

            # Controles de teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not paused:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT and not paused:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN and not paused:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP and not paused:
                    current_piece.rotation += 1
                    rotate_sfx.play()
                    if not valid_space(current_piece, grid):
                        current_piece.rotation -= 1
                elif event.key == pygame.K_SPACE and not paused:
                    can_hold = False
                    hard_drop(current_piece, grid)
                    harddrop_sfx.play()
                elif event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_m:
                    pygame.mixer.music.stop()
                elif event.key == pygame.K_r and not paused:
                    if can_hold:
                        held_piece, current_piece, next_piece, can_hold = hold_piece(
                            held_piece, current_piece, next_piece, can_hold
                        )
                elif event.key == pygame.K_g and energy_level >= 8 and not bonus_active:
                    double_points, bonus_active, bonus_end_time = activate_bonus(shop_data)
                    energy_level = 1
        if paused:
            draw_text_middle("PAUSED", 60, (255, 255, 255), win)
            pygame.display.update()
            continue
        # Place the current piece on the grid
        shape_pos = convert_shape_format(current_piece)
        for x, y in shape_pos:
            if y > -1:
                grid[y][x] = current_piece.color
        if change_piece:
            for pos in shape_pos:
                locked_positions[(pos[0], pos[1])] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape(adjusted_piece_probabilities)
            can_hold = True
            change_piece = False
            landing_sfx.play()

            # Clear rows after placing the piece
            rows_cleared = clear_rows(grid, locked_positions)
           
            if rows_cleared > 0:
                points_to_add = rows_cleared * (100 if rows_cleared == 4 else 10)
                if double_points:
                    points_to_add *= (2 + shop_data["bonus_multiplier"])
                    print("El multiplicador es de:", points_to_add)
                score += points_to_add
                player_points += points_to_add
                print(f"Score actual: {score}, Total acumulado: {player_points}")
                (Bonus_sfx if rows_cleared == 4 else claerrow_sfx).play()
                
                energy_level = max(0, min(energy_level + rows_cleared, 8))


        # Dibujar la ventana y actualizar la pantalla
        draw_window(win, grid, current_scenario, score, last_score)
        draw_next_shape(next_piece, win)
        draw_held_piece(held_piece, win)
        update_energy_bar(win, energy_level)
        if bonus_active:
            bonus_active, bonus_end_time = handle_bonus(bonus_active, bonus_end_time)
            draw_text_middle("BONUS TIME!", 40, (255, 255, 255), win)
            if not bonus_active:
                double_points = False

        # Mirar si has perdido
        if check_lost(locked_positions):
            run = False
            player_points += score
            save_game(player_points, shop_data, unlocked_scenarios)
            draw_text_middle("YOU LOST!", 40, (255, 255, 255), win)
            pygame.mixer.music.stop()
            gameover_sfx.play()
            update_score(score)
            pygame.display.update()
            pygame.time.delay(3000)
            return player_points, shop_data, unlocked_scenarios, current_scenario
    
    pygame.display.update()
    pygame.display.flip()
    pygame.time.delay(100)


def howplay():
    """
    Menu sobre como jugar
    """
    FondoJuego = pygame.image.load("assets/fondojuegoTuto.jpg")
    FondoJuego = pygame.transform.scale(FondoJuego, (s_width, s_height))
    
    while True:
        screen.blit(FondoJuego, (0, 0))  
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        MENU_BUTTON = Button(image=pygame.image.load("assets/Menubutton.png"), pos=(400, 600),
                            text_input="GO HOME", font=get_font(50), base_color="#d7fcd4", hovering_color="White")
        for button in [MENU_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main_menu(player_points, shop_data, unlocked_scenarios, adjusted_piece_probabilities, current_scenario)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Button_sfx.play()
                    main_menu(player_points, shop_data, unlocked_scenarios, adjusted_piece_probabilities, current_scenario)
        
        pygame.display.update()

def shop_menu(player_points, shop_data, unlocked_scenarios, adjusted_piece_probabilities, current_scenario):
    """
    Implementa la lógica de la tienda con botones dinámicos y conexión a la mejora de piezas.
    """
    pygame.mixer.music.load("assets/Hip Shop.mp3")
    pygame.mixer.music.play(-1)
    custom_background = pygame.image.load("assets/custom_background.jpg")
    custom_background = pygame.transform.scale(custom_background, (s_width, s_height))
    shop_background = pygame.image.load("assets/shop_background.png")
    shop_background = pygame.transform.scale(shop_background, (s_width, s_height))
    Margen = pygame.image.load("assets/button.png")
    Margen = pygame.transform.scale(Margen, (s_width - 705, s_height - 645))

    while True:
        screen.blit(custom_background, (0, 0))
        screen.blit(shop_background, (0, 0))

        SHOP_MOUSE_POS = pygame.mouse.get_pos()

        # Texto para puntos acumulados
        POINTS_TEXT = get_font(20).render(f"PUNTOS: {player_points}", True, "#ffffff")
        POINTS_RECT = POINTS_TEXT.get_rect(center=(400, 50))
        screen.blit(POINTS_TEXT, POINTS_RECT)

        # Botones de las piezas
        FIGURA_T_BUTTON = Button(image=Margen, pos=(205, 580),
                                 text_input="FIGURA T", font=get_font(10), base_color="White", hovering_color="Green")
        FIGURA_L_BUTTON = Button(image=Margen, pos=(307, 580),
                                 text_input="FIGURA L", font=get_font(10), base_color="White", hovering_color="Green")
        FIGURA_I_BUTTON = Button(image=Margen, pos=(408, 580),
                                 text_input="FIGURA I", font=get_font(10), base_color="White", hovering_color="Green")
        FIGURA_J_BUTTON = Button(image=Margen, pos=(509, 580),
                                 text_input="FIGURA J", font=get_font(10), base_color="White", hovering_color="Green")
        FIGURA_S_BUTTON = Button(image=Margen, pos=(612, 578),
                                 text_input="FIGURA S", font=get_font(10), base_color="White", hovering_color="Green")
        FIGURA_Z_BUTTON = Button(image=Margen, pos=(205, 523),
                                 text_input="FIGURA Z", font=get_font(10), base_color="White", hovering_color="Green")
        FIGURA_O_BUTTON = Button(image=Margen, pos=(307, 523),
                                 text_input="FIGURA O", font=get_font(10), base_color="White", hovering_color="Green")
        BACK_BUTTON = Button(image=Margen, pos=(400, 100),
                             text_input="VOLVER", font=get_font(10), base_color="White", hovering_color="Red")
        ESCENARIO_1_BUTTON = Button(image=Margen, pos=(552, 270),
                                    text_input="ESCENARIO 1", font=get_font(8),
                                    base_color="White", hovering_color="Green")
        ESCENARIO_2_BUTTON = Button(image=Margen, pos=(550, 332),
                                    text_input="ESCENARIO 2", font=get_font(8),
                                    base_color="White", hovering_color="Green")
        ESCENARIO_3_BUTTON = Button(image=Margen, pos=(550, 393),
                                    text_input="ESCENARIO 3", font=get_font(8),
                                    base_color="White", hovering_color="Green")
        BONUS_TIME_BUTTON = Button(image=Margen, pos=(408, 523),
                           text_input="TIEMPO BONUS", font=get_font(7), base_color="White", hovering_color="Green")
        BONUS_MULTIPLIER_BUTTON = Button(image=Margen, pos=(509, 524),
                                 text_input="BONUS MULTI", font=get_font(7), base_color="White", hovering_color="Green")
        DONATION_BUTTON = Button(image=Margen, pos=(611, 523),
                                 text_input="DONAR", font=get_font(10), base_color="White", hovering_color="Green")
        # Dibuja los botones
        for button in [FIGURA_T_BUTTON, FIGURA_L_BUTTON, FIGURA_I_BUTTON, FIGURA_J_BUTTON, FIGURA_S_BUTTON, FIGURA_Z_BUTTON, FIGURA_O_BUTTON, ESCENARIO_1_BUTTON, ESCENARIO_2_BUTTON, ESCENARIO_3_BUTTON, BONUS_TIME_BUTTON, BONUS_MULTIPLIER_BUTTON , DONATION_BUTTON, BACK_BUTTON]:
            button.changeColor(SHOP_MOUSE_POS)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Maneja las mejoras de probabilidades
                if FIGURA_T_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    player_points, adjusted_piece_probabilities = update_shop("T", player_points, shop_data)
                    Button_sfx.play()
                    save_game(player_points, shop_data, unlocked_scenarios)
                if FIGURA_L_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    Button_sfx.play()
                    player_points, adjusted_piece_probabilities = update_shop("L", player_points, shop_data)
                    save_game(player_points, shop_data, unlocked_scenarios)
                if FIGURA_I_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    Button_sfx.play()
                    player_points, adjusted_piece_probabilities = update_shop("I", player_points, shop_data)
                    save_game(player_points, shop_data, unlocked_scenarios)
                if FIGURA_J_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    Button_sfx.play()
                    player_points, adjusted_piece_probabilities = update_shop("J", player_points, shop_data)
                    save_game(player_points, shop_data, unlocked_scenarios)
                if FIGURA_S_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    Button_sfx.play()
                    player_points, adjusted_piece_probabilities = update_shop("S", player_points, shop_data)
                    save_game(player_points, shop_data, unlocked_scenarios)
                if FIGURA_Z_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    Button_sfx.play()
                    player_points, adjusted_piece_probabilities = update_shop("Z", player_points, shop_data)
                    save_game(player_points, shop_data, unlocked_scenarios)
                if FIGURA_O_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    Button_sfx.play()
                    player_points, adjusted_piece_probabilities = update_shop("O", player_points, shop_data)
                    save_game(player_points, shop_data, unlocked_scenarios)
                if ESCENARIO_1_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    Button_sfx.play()
                    if 1 not in unlocked_scenarios:
                        if player_points >= 300:
                            player_points -= 300
                            unlocked_scenarios.add(1)
                            print("Escenario 1 desbloqueado.")
                        else:
                            print("No tienes suficientes puntos.")
                    current_scenario = 1
                # Escenario 2
                if ESCENARIO_2_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    Button_sfx.play()
                    if 2 not in unlocked_scenarios:
                        if player_points >= 300:
                            player_points -= 300
                            unlocked_scenarios.add(2)
                            print("Escenario 2 desbloqueado.")
                        else:
                            print("No tienes suficientes puntos.")
                    current_scenario = 2
                # Escenario 3
                if ESCENARIO_3_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    Button_sfx.play()
                    if 3 not in unlocked_scenarios:
                        if player_points >= 300:
                            player_points -= 300
                            unlocked_scenarios.add(3)
                            print("Escenario 3 desbloqueado.")
                        else:
                            print("No tienes suficientes puntos.")
                    current_scenario = 3
                if BONUS_TIME_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    Button_sfx.play()
                    if shop_data["bonus_time"] < 3:
                        if player_points >= 100:
                            player_points -= 100
                            shop_data["bonus_time"] += 1
                            print(f"Tiempo bonus mejorado al nivel {shop_data['bonus_time']}!")
                        else:
                            print("No tienes suficientes puntos para mejorar el tiempo bonus.")
                    else:
                        print("El tiempo bonus ya está en el nivel máximo.")

                if BONUS_MULTIPLIER_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    Button_sfx.play()
                    if shop_data["bonus_multiplier"] < 3:
                        if player_points >= 100:
                            player_points -= 100
                            shop_data["bonus_multiplier"] += 1
                            print(f"Multiplicador mejorado al nivel {shop_data['bonus_multiplier']}!")
                        else:
                            print("No tienes suficientes puntos para mejorar el multiplicador.")
                    else:
                        print("El multiplicador ya está en el nivel máximo.")
                if DONATION_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    Button_sfx.play()
                    donated = player_points
                    player_points -= player_points
                    if donated == 0:
                        print("Steve: Pero tu me ves la cara de tonto o que?")
                    elif donated < 100:
                        print("Steve: Gracias por la calderilla... supongo")
                    elif donated < 500:
                        print("Steve: No hubiera sido mejor gastar este dinero en comprar algunos de mis articulos?")
                    elif donated < 1000:
                        print("Steve: ¡Muchas gracias! Podre gastar este dinero en el alquiler de este mes")
                    elif donated < 5000:
                        print("Steve: Realmente eres bueno en este juego, eh?")
                    elif donated < 10000:
                        print("Steve: A casa platita *emoji de dinero*")
                    elif donated < 25000:
                        print("Steve: Voy a ser el proximo milste bist")
                    elif donated < 50000:
                        print("Sea quien sea que lea esto y dando igual cuanto anime hayas visto porfavor mira Houseki no kuni")
                    elif donated < 10000000:
                        print("Estoy escribiendo esto a las 0:53 de la noche mientras escucho (chill breakcore songs to fall asleep listening to [part 2)]... Realmente deberia de parar ya")
                # Volver al menú principal
                if BACK_BUTTON.checkForInput(SHOP_MOUSE_POS):
                    Button_sfx.play()
                    pygame.mixer.music.stop()
                    return player_points, shop_data, unlocked_scenarios, adjusted_piece_probabilities, current_scenario
                

        pygame.display.update()

def update_shop(selected_piece, player_points, shop_data):
    """
    Mejora la probabilidad de aparición de una pieza seleccionada.
    """
    cost_per_level = 100
    max_level = 3

    if selected_piece in shop_data:
        if shop_data[selected_piece] < max_level and player_points >= cost_per_level:
            shop_data[selected_piece] += 1
            player_points -= cost_per_level
            print(f"¿Mejoraste la pieza {selected_piece} ahora tiene un 5% mas probabilidad de aparecer!. Nivel actual: {shop_data[selected_piece]}")
            
            adjusted_piece_probabilities = calculate_piece_probabilities(shop_data)
            save_game(player_points, shop_data, unlocked_scenarios) 
            return player_points, adjusted_piece_probabilities 
        else:
            print("No tienes suficientes puntos o la mejora ya está en el nivel máximo.")
    
    return player_points, calculate_piece_probabilities(shop_data)  

def unlock_scenario(scenario_number, points):
    """
    Desbloquea un escenario si el jugador tiene suficientes puntos.
    """
    unlock_cost = 300 

    if points >= unlock_cost:
        points -= unlock_cost
        unlocked_scenarios.add(scenario_number) 
        print(f"Escenario {scenario_number} desbloqueado.")
    else:
        print("No tienes suficientes puntos para desbloquear este escenario.")

    return points

piece_probabilities = {
    'T': {'base_prob': 10, 'level': 0},
    'L': {'base_prob': 10, 'level': 0},
    'I': {'base_prob': 10, 'level': 0},
    'J': {'base_prob': 10, 'level': 0},

    'S': {'base_prob': 10, 'level': 0},
    'Z': {'base_prob': 10, 'level': 0},
    'O': {'base_prob': 10, 'level': 0},

    'BOMERANG': {'base_prob': 10, 'level': 0},  
    'H': {'base_prob': 10, 'level': 0},
    'UNO': {'base_prob': 10, 'level': 0},

    'CRUZ': {'base_prob': 10, 'level': 0},
    'TRES': {'base_prob': 10, 'level': 0},
    'DOS': {'base_prob': 10, 'level': 0},  
}
# Datos de la tienda: nivel de mejora por cada pieza
shop_data = {
    "T": 0,  
    "L": 0,  
    "I": 0,  
    "J": 0,  
    "S": 0,  
    "Z": 0,  
    "O": 0,  
    "bonus_time": 0,
    "bonus_multiplier": 0,
}

# Función para calcular las probabilidades ajustadas
def calculate_piece_probabilities(shop_data):
    """
    Calcula las probabilidades ajustadas de las piezas basado en los niveles de la tienda.
    :param shop_data: Diccionario que contiene los niveles de mejora de cada pieza.
    :return: Diccionario con las probabilidades ajustadas de cada pieza.
    """
    total_prob = 0
    adjusted_probs = {}

    for piece, data in piece_probabilities.items():
        adjusted_prob = data['base_prob'] + (probabilidad * shop_data.get(piece, 0))
        adjusted_probs[piece] = adjusted_prob
        total_prob += adjusted_prob

    for piece in adjusted_probs:
        adjusted_probs[piece] = adjusted_probs[piece] / total_prob

    return adjusted_probs

# Inicializar probabilidades ajustadas
adjusted_piece_probabilities = calculate_piece_probabilities(shop_data)


def save_game(player_points, shop_data, unlocked_scenarios):
    """
    Guarda el progreso del jugador en un archivo JSON.
    """
    if not isinstance(unlocked_scenarios, set): 
        unlocked_scenarios = set()
    try:
        save_data = {
            "player_points": player_points,
            "shop_data": shop_data,
            "unlocked_scenarios": list(unlocked_scenarios),
            "current_scenario": current_scenario
        }
        with open('save_data.json', 'w') as file:
            json.dump(save_data, file)
        print("Progreso guardado con éxito.")
    except Exception as e:
        print(f"Error al guardar los datos: {e}")


def load_game():
    """
    Carga el progreso del jugador desde un archivo JSON.
    Si el archivo no existe o está vacío, devuelve valores predeterminados.
    """
    if not os.path.exists('save_data.json') or os.path.getsize('save_data.json') == 0:
        print("Archivo de guardado no encontrado o vacío. Inicializando nuevo progreso.")
        return 0, {"T": 0, "L": 0, "I": 0, "J": 0, "S": 0, "Z": 0, "O": 0, "bonus_time": 0, "bonus_multiplier": 0}, set(), 0
    try:
        with open('save_data.json', 'r') as file:
            save_data = json.load(file)
            player_points = save_data["player_points"]
            shop_data = save_data["shop_data"]
            unlocked_scenarios = set()
            current_scenario = save_data.get("current_scenario", 0)
            print("Progreso cargado con éxito.")
            return player_points, shop_data, unlocked_scenarios, current_scenario
    except json.JSONDecodeError:
        print("El archivo de guardado está corrupto. Inicializando nuevo progreso.")
        return 0, {"T": 0, "L": 0, "I": 0, "J": 0, "S": 0, "Z": 0, "O": 0, "bonus_time": 0, "bonus_multiplier": 0}, set(), 0


def main_menu(player_points, shop_data, unlocked_scenarios, adjusted_piece_probabilities, current_scenario):
    """
    Esta la estetica del menu y sus botones.
    """
    pygame.mixer.music.load("assets/musicamenu.mp3")
    pygame.mixer.music.play(-1)
    print("Entrando al menú principal")
    menu_running = True
    while menu_running:
        screen.blit(FondoMenu, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(50).render("Humanity's Play", True, "#4631c9")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 50))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(400, 150),
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(400, 300),
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        HOWPLAY_BUTTON = Button(image=pygame.image.load("assets/Guide Rect.png"), pos=(400, 450),
                            text_input="HOW TO PLAY", font=get_font(30), base_color="#d7fcd4", hovering_color="White")
        SHOP_BUTTON = Button(image=pygame.image.load("assets/Shop Rect.png"), pos=(400, 600),
                            text_input="SHOP", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON, HOWPLAY_BUTTON, SHOP_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Button_sfx.play()
                save_game(player_points, shop_data, unlocked_scenarios)
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Button_sfx.play()
                    pygame.mixer.music.stop()
                    player_points, shop_data, unlocked_scenarios, current_scenario = main_loop(win, player_points, shop_data, unlocked_scenarios, adjusted_piece_probabilities, current_scenario)
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    save_game(player_points, shop_data, unlocked_scenarios)
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                if HOWPLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    Button_sfx.play()
                    howplay()
                if SHOP_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if SHOP_BUTTON.checkForInput(MENU_MOUSE_POS):
                        Button_sfx.play()
                        player_points, shop_data, unlocked_scenarios, adjusted_piece_probabilities, current_scenario = shop_menu(player_points, shop_data, unlocked_scenarios, adjusted_piece_probabilities, current_scenario)
        pygame.display.update()
    return player_points, shop_data, unlocked_scenarios, current_scenario


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Humanity's play")
player_points, shop_data, unlocked_scenarios, current_scenario = load_game()
adjusted_piece_probabilities = calculate_piece_probabilities(shop_data)
player_points, shop_data, unlocked_scenarios, current_scenario = main_menu(player_points, shop_data, unlocked_scenarios, adjusted_piece_probabilities, current_scenario) # aqui
save_game(player_points, shop_data, unlocked_scenarios)
