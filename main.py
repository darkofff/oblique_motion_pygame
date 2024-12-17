import sys
import pygame as py
from ball import Ball  

# INNITS
py.init()
py.font.init()  # Initialize Pygame's font system

# VARIABLES
WIDTH, HEIGHT = 800, 600
COORDINATE_START_X = 10
COORDINATE_START_Y = 500
BALL_RADIUS = 7
GRAVITY = -9.81

running = True # Dla pętli
""" x, y = 0, 600 """

# SETUP
screen = py.display.set_mode((WIDTH, HEIGHT))
font = py.font.SysFont(None, 24)
py.display.set_caption("Rzut ukośny")

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
INPUT_BLANK = (200, 200, 200)
INPUT_SELECTED = (240, 240, 240)

# STATIC ELEMENTS
background = py.Surface((WIDTH, HEIGHT))
background.fill(WHITE)


# GAME STATE
# 0 - menu: wybór ustawień
# 1 - wykonanie programu
# 2 - ekran końcowy: możliwość resetu
game_state = 0

# --- GAME STATE 0 START ---

# INPUTS

velocity_input_rect = py.Rect(250, 565, 60, 26)  # Position and size of the input field
velocity = ""  # Text the user types
velocity_active = False  # Track if the input is active ( naciśnięty )
velocity_input_color = INPUT_BLANK

angle_input_rect = py.Rect(250, 535, 60, 26) 
angle = ""  
angle_active = False  
angle_input_color = INPUT_BLANK

grid_density_rect = py.Rect(700, 565, 60, 26) 
grid_density_coefficient = '10'
grid_density_active = False
grid_density_color = INPUT_BLANK

meter_size_rect = py.Rect(700, 535, 60, 26) 
meter_size = '5'
meter_size_active = False
meter_size_color = INPUT_BLANK


start_button_rect = py.Rect(350, 550, 50, 26)
start_button_text = font.render("Rzuć", True, (0, 0, 0)) 

# --- GAME STATE 0 END ---

# --- GAME STATE 1 START ---

# BALL
ball = Ball(COORDINATE_START_X, COORDINATE_START_Y, GRAVITY)

# number of tick while throw
tick = 0

# --- GAME STATE 1 END ---

# --- GAME STATE 2 START ---

positions_array = []

x_filnal_pos = 0
y_filnal_pos = 0

time_total = 0
total_distance = 0

x_for_max_height = 0
max_height = 0

reset_button_rect = py.Rect(400, 570, 70, 26)
reset_button_text = font.render("RESET", True, (0, 0, 0)) 

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
                    velocity_active = velocity_input_rect.collidepoint(event.pos)    
                    angle_active = angle_input_rect.collidepoint(event.pos)  
                    grid_density_active = grid_density_rect.collidepoint(event.pos)  
                    meter_size_active = meter_size_rect.collidepoint(event.pos)  
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
                if event.type == py.KEYDOWN and grid_density_active:
                    if event.key == py.K_BACKSPACE:
                        grid_density_coefficient = grid_density_coefficient[:-1]
                    else:
                        grid_density_coefficient += event.unicode
                if event.type == py.KEYDOWN and meter_size_active:
                    if event.key == py.K_BACKSPACE:
                        meter_size = meter_size[:-1]
                    else:
                        meter_size += event.unicode
            case 1:
                """ print('angle: ', float(angle))
                print('velocity: ', float(velocity)) """

            case 2:
                if event.type == py.MOUSEBUTTONDOWN:
                    if reset_button_rect.collidepoint(event.pos):
                        velocity_active = False
                        angle_active = False
                        grid_density_active = False
                        meter_size_active = False
                        tick = 0
                        x_filnal_pos = 0
                        y_filnal_pos = 0
                        time_total = 0
                        total_distance = 0
                        x_for_max_height = 0
                        max_height = 0
                        positions_array = []
                        game_state = 0
       

    # BLIT UKŁAD WSPÓŁRZĘDNYCH
    screen.blit(background, (0, 0))
    
    # Potrzebne żeby się nie wywalało jak się wyczyści input dla szerokości siatki. Ustala default na 10m
    grid_density_coefficient_int = int(grid_density_coefficient) if not grid_density_coefficient=="" else 10
    meter_size_int = int(meter_size) if not meter_size=="" else 5

    for x in range(COORDINATE_START_X, WIDTH, meter_size_int* grid_density_coefficient_int):
        py.draw.line(screen, GRAY, (x, COORDINATE_START_Y), (x, 0), 1)  # Linie pionowe
    for y in range(COORDINATE_START_Y, 0, -meter_size_int* grid_density_coefficient_int):
        py.draw.line(screen, GRAY, (COORDINATE_START_X, y), (WIDTH, y), 1)  # Linie poziome
   
    py.draw.line(screen, BLACK, (COORDINATE_START_X, COORDINATE_START_Y), (COORDINATE_START_X, 0), width=2)
    py.draw.line(screen, BLACK, (COORDINATE_START_X, COORDINATE_START_Y), (2000, COORDINATE_START_Y), width=2)

    match game_state:
        case 0: 
            
            # UPDATE INPUT COLOR
            velocity_input_color = INPUT_BLANK if not velocity_active else  INPUT_SELECTED
            angle_input_color = INPUT_BLANK if not angle_active else  INPUT_SELECTED
            grid_density_color = INPUT_BLANK if not grid_density_active else  INPUT_SELECTED
            meter_size_color = INPUT_BLANK if not meter_size_active else INPUT_SELECTED

            # ANGLE INPUT
            angle_label = font.render("Kąt (w stopniach): ", True, (0, 0, 0))
            screen.blit(angle_label, (20, 540))

            py.draw.rect(screen, angle_input_color, angle_input_rect)  
            angle_text_surface = font.render(angle, True, (0, 0, 0))  
            screen.blit(angle_text_surface, (angle_input_rect.x + 5, angle_input_rect.y + 5))  

            # VELOCITY INPUT
            velocity_label = font.render("Prędkość początkowa (m/s): ", True, (0, 0, 0))
            screen.blit(velocity_label, (20, 570))
            
            py.draw.rect(screen, velocity_input_color, velocity_input_rect)  
            velocity_text_surface = font.render(velocity, True, (0, 0, 0))  
            screen.blit(velocity_text_surface, (velocity_input_rect.x + 5, velocity_input_rect.y + 5))  

            # THROW BUTTON
            py.draw.rect(screen, (150, 150, 150), start_button_rect)
            screen.blit(start_button_text, (start_button_rect.x+5, start_button_rect.y+5 ))
            
            # GRID DENSITY
            grid_density_label = font.render("Gęstość siatki (w metrach): ", True, (0, 0, 0))
            screen.blit(grid_density_label, (450, 570))

            py.draw.rect(screen, grid_density_color, grid_density_rect)
            grid_density_text_surface = font.render(grid_density_coefficient, True, (0, 0, 0)) 
            screen.blit(grid_density_text_surface, (grid_density_rect.x + 5, grid_density_rect.y + 5))  
           
            # ROZMIAR 1 METRA
            meter_size_label = font.render("Długość 1 metra (w px): ", True, (0, 0, 0))
            screen.blit( meter_size_label, (450, 535))

            py.draw.rect(screen, meter_size_color, meter_size_rect)
            meter_size_text_surface = font.render(meter_size, True, (0, 0, 0)) 
            screen.blit(meter_size_text_surface, (meter_size_rect.x + 5, meter_size_rect.y + 5))  

            # BALL 
            py.draw.circle(screen, (0, 0, 0), (COORDINATE_START_X, COORDINATE_START_Y), BALL_RADIUS)
            
        case 1: 
            # BALL
            x_pos, y_pos, has_landed, velocity_tuple = ball.update(float(velocity), float(angle), tick, meter_size)
            screen.blit(ball.image, ball.rect)

            positions_array.append((x_pos, y_pos))

            x_filnal_pos = x_pos
            y_filnal_pos = y_pos
            
            for tuple in  positions_array:
                py.draw.circle(screen, BLACK, tuple, 2)

            tick+=1

            if has_landed:
                velocity_x, velocity_y = velocity_tuple
                time_total = (2*velocity_y)/-GRAVITY
                total_distance = velocity_x * time_total
                
                x_for_max_height = (velocity_x * velocity_y)/(-GRAVITY)
                max_height = velocity_y * (x_for_max_height/velocity_x) - 0.5 * (-GRAVITY) * ((x_for_max_height**2)/(velocity_x**2))
                
                game_state = 2
        case 2: 
            py.draw.circle(screen, BLACK, (x_filnal_pos, y_filnal_pos), BALL_RADIUS)

            for tuple in  positions_array:
                py.draw.circle(screen, BLACK, tuple, 2)

            total_time_display = font.render(f"Całkowity czas lotu: {round(time_total, 4)} s", True, (0, 0, 0))
            screen.blit(total_time_display, (20, 535))
            
            total_distance_display = font.render(f"Odległość: {round(total_distance, 4)} m", True, (0, 0, 0))
            screen.blit(total_distance_display, (20, 575))
           
            total_height_display = font.render(f"Maksymalna wysokość: {round(max_height, 4)} m", True, (0, 0, 0))
            screen.blit(total_height_display, (400, 535))

            py.draw.rect(screen, GRAY, reset_button_rect )
            screen.blit(reset_button_text, (reset_button_rect.x+5, reset_button_rect.y+5 ))
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