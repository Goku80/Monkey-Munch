import random
import sys
import pygame
from pygame.locals import *


# Konstanten
WINDOW_WIDTH = 500                                                                                              # Breite des Spielfensters
WINDOW_HEIGHT = 500                                                                                             # Höhe des Spielfensters
TEXT_COLOR = (255, 255, 255)                                                                                    # Textfarbe (weiß)
BACKGROUND_COLOR = (34, 139, 34)                                                                                # Hintergrundfarbe (waldgrün)
MOVE_SPEED = 15                                                                                                 # Initiale Geschwindigkeit der Schlange
SPEED_INCREMENT = 0.5                                                                                           # Geschwindigkeitserhöhung pro gegessener Banane

# Pygame-Initialisierung
pygame.init()                                                                                                   # Pygame-Initialisierung
main_clock = pygame.time.Clock()                                                                                # Hauptuhr für das Spiel
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))                                         # Fenster erstellen
pygame.display.set_caption('Monkey Munch')                                                                      # Titel des Fensters
font = pygame.font.SysFont('comicsansms', 32)                                                                   # Schriftart für Titel und Game Over - KLEINER
score_font = pygame.font.SysFont('comicsansms', 24)                                                             # Schriftart für Punkteanzeige - KLEINER

# Farben
JUNGLE_GREEN = (34, 139, 34)                                                                                    # Waldgrün für den Hintergrund
BANANA_YELLOW = (255, 225, 53)                                                                                  # Gelb für die Punkteanzeige
SCORE_BG = (0, 0, 0, 128)                                                                                       # Halbdurchsichtiger Hintergrund für Punkteanzeige
SCORE_COLOR = (200, 200, 255)                                                                                   # Hellblaue Farbe für die Punkteanzeige

# Bilder laden
try:
    background_image = pygame.image.load('jungle_bg.jpg')                                                       # Hintergrundbild laden
    background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
except:
    background_image = None                                                                                     # Falls das Bild nicht gefunden wird

# Musik und Sounds
game_over_sound = pygame.mixer.Sound('gameover.wav')                                                            # Game Over Sound
pick_up_sound = pygame.mixer.Sound('pickup.wav')                                                                # Sound für das Aufsammeln von Bananen
music_playing = True                                                                                            # Status der Musik

# Zufällige Startrichtung wählen
directions = ['left', 'right', 'up', 'down']
start_direction = random.choice(directions)

# Spielzustände basierend auf zufälliger Startrichtung
move_left = start_direction == 'left'
move_right = start_direction == 'right'
move_up = start_direction == 'up'
move_down = start_direction == 'down'

# Spielfiguren
monkey = [{'rect': pygame.Rect(300, 100, 20, 20), 'dir': start_direction}]                                      # Startposition der Schlange
head = 0  # Index des Schlangenkopfs
monkey_image = pygame.image.load('monkey.png')                                                                  # Bild der Schlange laden
monkey_image = pygame.transform.scale(monkey_image, (20, 20))                                                   # Bildgröße anpassen
food_image = pygame.image.load('banana.png')                                                                    # Bild der Banane laden
food_image = pygame.transform.scale(food_image, (20, 20))                                                       # Bananengröße anpassen
food = pygame.Rect(random.randint(0, WINDOW_WIDTH - 20), random.randint(0, WINDOW_HEIGHT - 20), 20, 20)         # Zufällige Startposition der Banane

# Punkte
score = 0                                                                                                       # Aktueller Punktestand
top_score = 0                                                                                                   # Höchster Punktestand


# Spiel beenden und Programm schließen
def terminate():
    pygame.quit()
    sys.exit()


# Auf eine Tasteneingabe warten
def wait_for_key_press():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                terminate()
            if event.type == KEYDOWN:
                return


# Text auf dem Bildschirm zeichnen
def draw_text(text, font, surface, x, y, color=TEXT_COLOR, has_bg=False):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    
    # Hintergrund für den Text zeichnen, falls gewünscht
    if has_bg:
        bg_rect = text_rect.copy()                                                                              # Hintergrund etwas größer als Text
        bg_rect.inflate_ip(20, 10)                                                                              # Hintergrund etwas größer als Text
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, 160))                                                                         # Halbtransparenter schwarzer Hintergrund
        surface.blit(bg_surface, bg_rect)                                                                       # Hintergrund zeichnen
    
    surface.blit(text_obj, text_rect)


# Überprüfen, ob die Schlange die Banane erreicht hat
def check_collision_with_food():
    global food, score, MOVE_SPEED
    if monkey[head]['rect'].colliderect(food):
        food = pygame.Rect(random.randint(0, WINDOW_WIDTH - 20), 
                           random.randint(0, WINDOW_HEIGHT - 20), 20, 20)
        pick_up_sound.play()
        score += 10
        MOVE_SPEED += SPEED_INCREMENT
    else:
        monkey.pop()


# Überprüfen, ob die Schlange gegen die Wände gestoßen ist
def check_collision_with_walls():
    if (monkey[head]['rect'].left < 0 or 
        monkey[head]['rect'].right > WINDOW_WIDTH or
        monkey[head]['rect'].top < 0 or monkey[head]['rect'].bottom > WINDOW_HEIGHT):
        game_over()


# Punkteanzeige zeichnen
def draw_score():
    # Zeichnen des Punktestands links oben ohne Hintergrund, mit sehr kleinem Font
    kleiner_font = pygame.font.SysFont('comicsansms', 18)                                                      # Noch kleinere Schrift
    # Hintergrund für besseren Kontrast
    score_bg = pygame.Surface((100, 40), pygame.SRCALPHA)                                                      # Transparente Oberfläche
    score_bg.fill((0, 0, 0, 80))                                                                               # Sehr leicht transparent
    window_surface.blit(score_bg, (5, 5))                                                                      # Oberer linker Bildschirmrand
    # Text
    draw_text(f'Punkte: {score}', kleiner_font, window_surface, 10, 8, SCORE_COLOR)                            # Neue Farbe und Position
    draw_text(f'Highscore: {top_score}', kleiner_font, window_surface, 10, 26, SCORE_COLOR)                    # Neue Farbe und Position


# Startbildschirm anzeigen
def start_screen():
    # Hintergrund zeichnen
    if background_image:
        window_surface.blit(background_image, (0, 0))
    else:
        window_surface.fill(JUNGLE_GREEN)
    
    # Halbtransparenter Overlay für Text
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 120))  # Halbdurchsichtiges Schwarz
    window_surface.blit(overlay, (0, 0))
    
    # Text zentrieren
    title_text = 'Monkey Munch'
    title_obj = font.render(title_text, True, BANANA_YELLOW)
    title_rect = title_obj.get_rect()
    title_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)
    window_surface.blit(title_obj, title_rect)
    
    # Starttext zentrieren - kleinerer Text
    start_font = pygame.font.SysFont('comicsansms', 28)
    start_text = 'Drücke eine Taste zum Starten'
    start_obj = start_font.render(start_text, True, BANANA_YELLOW)
    start_rect = start_obj.get_rect()
    start_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 50)
    window_surface.blit(start_obj, start_rect)
    
    pygame.display.update()
    wait_for_key_press()


# Game Over-Prozedur
def game_over():
    global score, top_score, MOVE_SPEED
    if score > top_score:
        top_score = score
    game_over_sound.play()
    
    # Halbdurchsichtiger Hintergrund für Game Over-Text
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))  # Halbdurchsichtiges Schwarz
    window_surface.blit(overlay, (0, 0))
    
    # Game Over Text zentrieren
    gameover_text = 'Game Over'
    gameover_obj = font.render(gameover_text, True, TEXT_COLOR)
    gameover_rect = gameover_obj.get_rect()
    gameover_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3)
    window_surface.blit(gameover_obj, gameover_rect)
    
    # Neustart Text zentrieren - kleinerer Text
    restart_font = pygame.font.SysFont('comicsansms', 28)
    restart_text = 'Drücke eine Taste zum Neustarten'
    restart_obj = restart_font.render(restart_text, True, TEXT_COLOR)
    restart_rect = restart_obj.get_rect()
    restart_rect.center = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 50)
    window_surface.blit(restart_obj, restart_rect)
    
    pygame.display.update()
    wait_for_key_press()
    reset_game()


# Spiel zurücksetzen
def reset_game():
    global monkey, head, move_left, move_right, move_up, move_down, score, MOVE_SPEED, start_direction
    
    # Neue zufällige Startrichtung wählen
    start_direction = random.choice(directions)
    move_left = start_direction == 'left'
    move_right = start_direction == 'right'
    move_up = start_direction == 'up'
    move_down = start_direction == 'down'
    
    monkey = [{'rect': pygame.Rect(300, 100, 20, 20), 'dir': start_direction}]
    head = 0
    score = 0
    MOVE_SPEED = 15  # Geschwindigkeit zurücksetzen


# Bewegung der Schlange steuern
def move_monkey():
    if move_down:
        monkey[head]['dir'] = 'down'
    elif move_up:
        monkey[head]['dir'] = 'up'
    elif move_left:
        monkey[head]['dir'] = 'left'
    elif move_right:
        monkey[head]['dir'] = 'right'

    if monkey[head]['dir'] == 'up':
        new_head = {'rect': pygame.Rect(monkey[head]['rect'].left, monkey[head]['rect'].top - MOVE_SPEED, 20, 20),
                    'dir': 'up'}
    elif monkey[head]['dir'] == 'down':
        new_head = {'rect': pygame.Rect(monkey[head]['rect'].left, monkey[head]['rect'].top + MOVE_SPEED, 20, 20),
                    'dir': 'down'}
    elif monkey[head]['dir'] == 'left':
        new_head = {'rect': pygame.Rect(monkey[head]['rect'].left - MOVE_SPEED, monkey[head]['rect'].top, 20, 20),
                    'dir': 'left'}
    elif monkey[head]['dir'] == 'right':
        new_head = {'rect': pygame.Rect(monkey[head]['rect'].left + MOVE_SPEED, monkey[head]['rect'].top, 20, 20),
                    'dir': 'right'}

    monkey.insert(0, new_head)


# Ereignisse (Tastendrücke) verarbeiten
def handle_events():
    global move_left, move_right, move_up, move_down
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT and monkey[head]['dir'] != 'right':
                move_left, move_right, move_up, move_down = True, False, False, False
            elif event.key == K_RIGHT and monkey[head]['dir'] != 'left':
                move_left, move_right, move_up, move_down = False, True, False, False
            elif event.key == K_UP and monkey[head]['dir'] != 'down':
                move_left, move_right, move_up, move_down = False, False, True, False
            elif event.key == K_DOWN and monkey[head]['dir'] != 'up':
                move_left, move_right, move_up, move_down = False, False, False, True


# Hauptspiel
start_screen()
reset_game()
while True:
    handle_events()                 # Ereignisse verarbeiten
    move_monkey()                   # Schlange bewegen
    check_collision_with_food()     # Kollision mit der Banane prüfen
    check_collision_with_walls()    # Kollision mit den Wänden prüfen

    # Hintergrund zeichnen
    if background_image:
        window_surface.blit(background_image, (0, 0))
    else:
        window_surface.fill(JUNGLE_GREEN)
        
    for segment in monkey:                                  # Schlange zeichnen
        window_surface.blit(monkey_image, segment['rect'])
    window_surface.blit(food_image, food)                   # Banane zeichnen

    # Punkte anzeigen
    draw_score()

    pygame.display.update()                                 # Anzeige aktualisieren
    main_clock.tick(15)                                     # Bildwiederholrate einstellen
