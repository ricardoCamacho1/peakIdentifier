import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Constants for the game
WIDTH, HEIGHT = 800, 600
BALL_SPEED = [3, 3]  # Starting speed
PADDLE_SPEED = 5
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FONT_SIZE = 48
WINNING_SCORE = 5

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Atari Pong for DipoleDigital")

# Ball settings
ball = pygame.Rect(WIDTH // 2 - 15, HEIGHT // 2 - 15, 30, 30)

# Paddle settings
paddle1 = pygame.Rect(30, HEIGHT // 2 - 70, 10, 140)
paddle2 = pygame.Rect(WIDTH - 40, HEIGHT // 2 - 70, 10, 140)

# Clock to control game speed
clock = pygame.time.Clock()

# Font for displaying scores and countdown
font = pygame.font.Font(None, FONT_SIZE)

# Player names
player1_name = ""
player2_name = ""

# Scores
score1 = 0
score2 = 0

def draw_text_centered(message, height, font, color):
    text = font.render(message, True, color)
    rect = text.get_rect(center=(WIDTH // 2, height))
    screen.blit(text, rect)

def start_page():
    started = False
    while not started:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                started = True

        screen.fill(BLACK)
        draw_text_centered("Hello,", HEIGHT // 2 - 60, font, WHITE)
        draw_text_centered("This is the Atari Pong for DipoleDigital", HEIGHT // 2, font, WHITE)
        draw_text_centered("Press any key to start!", HEIGHT // 2 + 60, font, WHITE)
        pygame.display.flip()
        clock.tick(30)

def get_player_name(player_number):
    name = ""
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.fill(BLACK)
        prompt = f"Enter name of Player {player_number}: {name}"
        draw_text_centered(prompt, HEIGHT // 2, font, WHITE)
        pygame.display.flip()
        clock.tick(30)

def ready_screen(player1_name, player2_name):
    ready = False
    while not ready:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                ready = True

        screen.fill(BLACK)
        draw_text_centered(f"Are you ready {player1_name} and {player2_name}?", HEIGHT // 2 - 90, font, WHITE)
        draw_text_centered(f"{player1_name} use 'W' and 'S'.", HEIGHT // 2 - 30, font, WHITE)
        draw_text_centered(f"{player2_name} use 'UP' and 'DOWN' arrows.", HEIGHT // 2 + 30, font, WHITE)
        draw_text_centered("Press any key to start the match", HEIGHT // 2 + 90, font, WHITE)
        pygame.display.flip()
        clock.tick(30)


def game_loop(player1_name, player2_name):
    global score1, score2, BALL_SPEED
    running = True
    ball_speed_increment_interval = 10000  # Interval in milliseconds (10 seconds)
    pygame.time.set_timer(pygame.USEREVENT + 1, ball_speed_increment_interval)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.USEREVENT + 1:
                # Increase ball speed every 10 seconds
                BALL_SPEED[0] *= 1.2
                BALL_SPEED[1] *= 1.2

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1.y -= PADDLE_SPEED if paddle1.y - PADDLE_SPEED > 0 else 0
        if keys[pygame.K_s]:
            paddle1.y += PADDLE_SPEED if paddle1.y + paddle1.height + PADDLE_SPEED < HEIGHT else 0
        if keys[pygame.K_UP]:
            paddle2.y -= PADDLE_SPEED if paddle2.y - PADDLE_SPEED > 0 else 0
        if keys[pygame.K_DOWN]:
            paddle2.y += PADDLE_SPEED if paddle2.y + paddle2.height + PADDLE_SPEED < HEIGHT else 0

        ball.x += BALL_SPEED[0]
        ball.y += BALL_SPEED[1]

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            BALL_SPEED[1] = -BALL_SPEED[1]
        if ball.left <= 0:
            score2 += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            BALL_SPEED[0] = -3  # Reset to original direction with a base speed
        elif ball.right >= WIDTH:
            score1 += 1
            ball.center = (WIDTH // 2, HEIGHT // 2)
            BALL_SPEED[0] = 3  # Reset to original direction with a base speed
        if ball.colliderect(paddle1) or ball.colliderect(paddle2):
            BALL_SPEED[0] = -BALL_SPEED[0]

        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, paddle1)
        pygame.draw.rect(screen, WHITE, paddle2)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

        draw_text_centered(f"{player1_name}: {score1}", FONT_SIZE, font, WHITE)
        draw_text_centered(f"{player2_name}: {score2}", HEIGHT - FONT_SIZE, font, WHITE)

        pygame.display.flip()
        clock.tick(60)

        if score1 >= WINNING_SCORE or score2 >= WINNING_SCORE:
            display_winner(player1_name, player2_name)
            running = False


def display_winner(player1_name, player2_name):
    if score1 >= WINNING_SCORE:
        winner_text = f"{player1_name} Wins!"
    else:
        winner_text = f"{player2_name} Wins!"
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

        screen.fill(BLACK)
        draw_text_centered(winner_text, HEIGHT // 2, font, WHITE)
        draw_text_centered("Press Enter to exit", HEIGHT // 2 + 60, font, WHITE)
        pygame.display.flip()
        clock.tick(30)

# Main program flow
start_page()
player1_name = get_player_name(1)
player2_name = get_player_name(2)
ready_screen(player1_name, player2_name)
game_loop(player1_name, player2_name)
