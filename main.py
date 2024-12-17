import sys
import pygame as py
from ball import Ball  

# INNITS
py.init()
py.font.init()  # Initialize Pygame's font system

# VARIABLES
WIDTH, HEIGHT = 800, 600
COORDINATE_START_X = 30
COORDINATE_START_Y = 500
BALL_RADIUS = 7
running = True # Dla pętli
x, y = 0, 600
speed = 5

# SETUP
screen = py.display.set_mode((WIDTH, HEIGHT))
font = py.font.SysFont(None, 24)
py.display.set_caption("Rzut ukośny")

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
INPUT_BLANK = (200, 200, 200)
INPUT_SELECTED = (240, 240, 240)

# STATIC ELEMENTS
background = py.Surface((WIDTH, HEIGHT))
background.fill(WHITE)

ground = py.image.load("./img/ground.png")
sky = py.image.load("./img/sky.png") # 800x300
sky = py.transform.scale(sky, (1000, 500) )

# GAME STATE
# 0 - menu: wybór ustawień
# 1 - wykonanie programu
# 2 - ekran końcowy: możliwość resetu
game_state = 0

# --- GAME STATE 0 START ---

# INPUTS
velocity_input_rect = py.Rect(200, 565, 60, 26)  # Position and size of the input field
velocity = ""  # Text the user types
velocity_active = False  # Track if the input is active ( naciśnięty )
velocity_input_color = INPUT_BLANK

angle_input_rect = py.Rect(200, 535, 60, 26) 
angle = ""  
angle_active = False  
angle_input_color = INPUT_BLANK

start_button_rect = py.Rect(300, 550, 50, 26)
start_button_text = font.render("Rzuć", True, (0, 0, 0)) 

# --- GAME STATE 0 END ---

# --- GAME STATE 1 START ---

# BALL
ball = Ball(COORDINATE_START_X, COORDINATE_START_Y)

# number of tick while throw
tick = 0

# --- GAME STATE 1 END ---

# --- GAME STATE 2 START ---

x_filnal_pos = 0
y_filnal_pos = 0

# --- GAME STATE 2 END ---


# ZEGAR
clock = py.time.Clock()


while running:
    
    for event in py.event.get():
        # EXIT WINDOW
        if event.type == py.QUIT:
            running = False
        
        match game_state:
            case 0:
                # INPUTS
                if event.type == py.MOUSEBUTTONDOWN:
                    velocity_active = velocity_input_rect.collidepoint(event.pos)  # Activate if clicked inside   
                    angle_active = angle_input_rect.collidepoint(event.pos)  # Activate if clicked inside   
                    if start_button_rect.collidepoint(event.pos):
                        game_state = 1
                if event.type == py.KEYDOWN and velocity_active:
                    if event.key == py.K_BACKSPACE:
                        velocity = velocity[:-1]
                    else:
                        velocity += event.unicode
                if event.type == py.KEYDOWN and angle_active:
                    if event.key == py.K_BACKSPACE:
                        angle = angle[:-1]
                    else:
                        angle += event.unicode
            case 1:
                """ print('angle: ', float(angle))
                print('velocity: ', float(velocity)) """


            case 2:
                print('case 2')

    # BLIT
    screen.blit(background, (0, 0))
    py.draw.line(screen, BLACK, (COORDINATE_START_X, COORDINATE_START_Y), (COORDINATE_START_X, 0), width=1)
    py.draw.line(screen, BLACK, (COORDINATE_START_X, COORDINATE_START_Y), (2000, COORDINATE_START_Y), width=1)
    
    """ screen.blit(sky, (0, 0))
    screen.blit(ground, (0, 500)) """
   

    match game_state:
        case 0: 
            
            # UPDATE INPUT COLOR
            velocity_input_color = INPUT_BLANK if not velocity_active else  INPUT_SELECTED
            angle_input_color = INPUT_BLANK if not angle_active else  INPUT_SELECTED

            # USER INPUT SECTION
            angle_label = font.render("Kąt (w stopniach): ", True, (0, 0, 0))
            screen.blit(angle_label, (20, 540))

            py.draw.rect(screen, angle_input_color, angle_input_rect)  
            angle_text_surface = font.render(angle, True, (0, 0, 0))  
            screen.blit(angle_text_surface, (angle_input_rect.x + 5, angle_input_rect.y + 5))  

            velocity_label = font.render("Prędkość początkowa: ", True, (0, 0, 0))
            screen.blit(velocity_label, (20, 570))
            
            py.draw.rect(screen, velocity_input_color, velocity_input_rect)  
            velocity_text_surface = font.render(velocity, True, (0, 0, 0))  
            screen.blit(velocity_text_surface, (velocity_input_rect.x + 5, velocity_input_rect.y + 5))  

            py.draw.rect(screen, (150, 150, 150), start_button_rect)
            screen.blit(start_button_text, (start_button_rect.x+5, start_button_rect.y+5 ))
            
            py.draw.circle(screen, (0, 0, 0), (30, 500), BALL_RADIUS)
            
        case 1: 
            # BALL
            x_pos, y_pos, has_landed = ball.update(float(velocity), float(angle), tick)
            screen.blit(ball.image, ball.rect)

            x_filnal_pos = x_pos
            y_filnal_pos = y_pos

            # print("pozycja: ", x_pos, y_pos)
            
            tick+=1

            if has_landed:
                game_state = 2
        case 2: 
            py.draw.circle(screen, (0, 0, 0), (x_filnal_pos, y_filnal_pos), BALL_RADIUS)
        case _:
            running = False


    
    py.display.update()
    clock.tick(60)


py.quit()
sys.exit()

""" 
POMYSŁ:
    - podzielić na 3 etapy

    1. Etap wybierania ustawień:
        - widoczne są ustawienia 
        - i przycisk start
    2. Etap wykonania programu:
        - dodawana jest skala żeby się wszystko mieściło na ekranie
            - przeliczyć maksymalną odległość
            - przeliczyć maksymalną wysokość 
            - ustalić przedziałki 
                - dla osi x: np: do 10, 25, 50, 100, 250, 500, 1000 itd. [m]
                - dla osi y: np: do ...
            - dodać skalę
        - rzut właściwy, animacja itd.
        - wyświetliać dynamicznie czas
    3. wyświetlić na dole 
        - czas lotu 
        - maksymalną odległość x i y
        - przycisk reset: który przenosi do etapu 1
 """