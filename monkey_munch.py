import random
import sys
import pygame
from pygame.locals import *

# Konstanten
WINDOW_WIDTH = 500  # Breite des Spielfensters
WINDOW_HEIGHT = 500  # Höhe des Spielfensters
TEXT_COLOR = (0, 0, 0)  # Textfarbe (schwarz)
BACKGROUND_COLOR = (245, 245, 245)  # Hintergrundfarbe (weiß)
MOVE_SPEED = 15  # Initiale Geschwindigkeit der Schlange
SPEED_INCREMENT = 0.5  # Geschwindigkeitserhöhung pro gegessener Banane

# Pygame-Initialisierung
pygame.init()
main_clock = pygame.time.Clock()  # Hauptuhr für das Spiel
window_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Fenster erstellen
pygame.display.set_caption('Monkey Munch')  # Titel des Fensters
font = pygame.font.SysFont(None, 48)  # Schriftart für Titel und Game Over
score_font = pygame.font.SysFont(None, 36)  # Schriftart für Punkteanzeige

# Farben
WHITE = (245, 245, 245)  # Weiß für den Hintergrund

# Musik und Sounds
game_over_sound = pygame.mixer.Sound('gameover.wav')  # Game Over Sound
pick_up_sound = pygame.mixer.Sound('pickup.wav')  # Sound für das Aufsammeln von Bananen
music_playing = True  # Status der Musik

# Spielzustände
move_left = False
move_right = True  # Startbewegung nach rechts
move_up = False
move_down = False

# Spielfiguren
snake = [{'rect': pygame.Rect(300, 100, 20, 20), 'dir': 'right'}]  # Startposition der Schlange
head = 0  # Index des Schlangenkopfs
snake_image = pygame.image.load('monkey.png')  # Bild der Schlange laden
snake_image = pygame.transform.scale(snake_image, (20, 20))  # Bildgröße anpassen
food_image = pygame.image.load('banana.png')  # Bild der Banane laden
food = pygame.Rect(random.randint(0, WINDOW_WIDTH - 20), random.randint(0, WINDOW_HEIGHT - 20), 20,
                   20)  # Zufällige Startposition der Banane

# Punkte
score = 0  # Aktueller Punktestand
top_score = 0  # Höchster Punktestand


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
def draw_text(text, font, surface, x, y):
    text_obj = font.render(text, True, TEXT_COLOR)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


# Überprüfen, ob die Schlange die Banane erreicht hat
def check_collision_with_food():
    global food, score, MOVE_SPEED
    if snake[head]['rect'].colliderect(food):
        food = pygame.Rect(random.randint(0, WINDOW_WIDTH - 20), random.randint(0, WINDOW_HEIGHT - 20), 20, 20)
        pick_up_sound.play()
        score += 10
        MOVE_SPEED += SPEED_INCREMENT
    else:
        snake.pop()


# Überprüfen, ob die Schlange gegen die Wände gestoßen ist
def check_collision_with_walls():
    if (snake[head]['rect'].left < 0 or snake[head]['rect'].right > WINDOW_WIDTH or
            snake[head]['rect'].top < 0 or snake[head]['rect'].bottom > WINDOW_HEIGHT):
        game_over()


# Game Over-Prozedur
def game_over():
    global score, top_score, MOVE_SPEED
    if score > top_score:
        top_score = score
    game_over_sound.play()
    draw_text('Game Over', font, window_surface, WINDOW_WIDTH // 3, WINDOW_HEIGHT // 3)
    draw_text('Press a key to play again.', font, window_surface, WINDOW_WIDTH // 3 - 80, WINDOW_HEIGHT // 3 + 50)
    pygame.display.update()
    wait_for_key_press()
    reset_game()


# Spiel zurücksetzen
def reset_game():
    global snake, head, move_left, move_right, move_up, move_down, score, MOVE_SPEED
    snake = [{'rect': pygame.Rect(300, 100, 20, 20), 'dir': 'right'}]
    head = 0
    move_left = False
    move_right = True
    move_up = False
    move_down = False
    score = 0
    MOVE_SPEED = 15  # Geschwindigkeit zurücksetzen


# Bewegung der Schlange steuern
def move_snake():
    if move_down:
        snake[head]['dir'] = 'down'
    elif move_up:
        snake[head]['dir'] = 'up'
    elif move_left:
        snake[head]['dir'] = 'left'
    elif move_right:
        snake[head]['dir'] = 'right'

    if snake[head]['dir'] == 'up':
        new_head = {'rect': pygame.Rect(snake[head]['rect'].left, snake[head]['rect'].top - MOVE_SPEED, 20, 20),
                    'dir': 'up'}
    elif snake[head]['dir'] == 'down':
        new_head = {'rect': pygame.Rect(snake[head]['rect'].left, snake[head]['rect'].top + MOVE_SPEED, 20, 20),
                    'dir': 'down'}
    elif snake[head]['dir'] == 'left':
        new_head = {'rect': pygame.Rect(snake[head]['rect'].left - MOVE_SPEED, snake[head]['rect'].top, 20, 20),
                    'dir': 'left'}
    elif snake[head]['dir'] == 'right':
        new_head = {'rect': pygame.Rect(snake[head]['rect'].left + MOVE_SPEED, snake[head]['rect'].top, 20, 20),
                    'dir': 'right'}

    snake.insert(0, new_head)


# Ereignisse (Tastendrücke) verarbeiten
def handle_events():
    global move_left, move_right, move_up, move_down
    for event in pygame.event.get():
        if event.type == QUIT:
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_LEFT and snake[head]['dir'] != 'right':
                move_left, move_right, move_up, move_down = True, False, False, False
            elif event.key == K_RIGHT and snake[head]['dir'] != 'left':
                move_left, move_right, move_up, move_down = False, True, False, False
            elif event.key == K_UP and snake[head]['dir'] != 'down':
                move_left, move_right, move_up, move_down = False, False, True, False
            elif event.key == K_DOWN and snake[head]['dir'] != 'up':
                move_left, move_right, move_up, move_down = False, False, False, True


# Startbildschirm anzeigen
def start_screen():
    window_surface.fill(BACKGROUND_COLOR)
    draw_text('Monkey Munch', font, window_surface, (WINDOW_WIDTH // 3), (WINDOW_HEIGHT // 3))
    draw_text('Press a key to start.', font, window_surface, (WINDOW_WIDTH // 3) - 30, (WINDOW_HEIGHT // 3) + 50)
    pygame.display.update()
    wait_for_key_press()


# Hauptspiel
start_screen()
reset_game()
while True:
    handle_events()  # Ereignisse verarbeiten
    move_snake()  # Schlange bewegen
    check_collision_with_food()  # Kollision mit der Banane prüfen
    check_collision_with_walls()  # Kollision mit den Wänden prüfen

    window_surface.fill(WHITE)  # Hintergrund zeichnen
    for segment in snake:  # Schlange zeichnen
        window_surface.blit(snake_image, segment['rect'])
    window_surface.blit(food_image, food)  # Banane zeichnen

    # Punkte anzeigen
    draw_text(f'Score: {score}', score_font, window_surface, 10, 10)
    draw_text(f'Top Score: {top_score}', score_font, window_surface, 10, 40)

    pygame.display.update()  # Anzeige aktualisieren
    main_clock.tick(15)  # Bildwiederholrate einstellen
