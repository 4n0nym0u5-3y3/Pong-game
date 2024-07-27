import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up game elements
BALL_RADIUS = 20
PAD_WIDTH = 10
PAD_HEIGHT = 80
LEFT = False
RIGHT = True

ball_pos = [WIDTH // 2, HEIGHT // 2]
ball_vel = [0, 0]

paddle1_pos = HEIGHT // 2 - PAD_HEIGHT // 2
paddle2_pos = HEIGHT // 2 - PAD_HEIGHT // 2

paddle1_vel = 0
paddle2_vel = 0

score1 = 0
score2 = 0

font = pygame.font.SysFont("comicsans", 50)

# Helper function to initialize ball position and velocity
def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_pos = [WIDTH // 2, HEIGHT // 2]
    vx = random.randrange(120, 240) / 60
    vy = -random.randrange(60, 180) / 60
    if direction == LEFT:
        vx = -vx
    ball_vel = [vx, vy]

# Function to start a new game
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, score1, score2
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT // 2 - PAD_HEIGHT // 2
    paddle2_pos = HEIGHT // 2 - PAD_HEIGHT // 2
    paddle1_vel = 0
    paddle2_vel = 0
    spawn_ball(random.choice([LEFT, RIGHT]))

# Function to draw game elements
def draw(win):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel

    win.fill(BLACK)

    # Draw mid line and gutters
    pygame.draw.line(win, WHITE, [WIDTH // 2, 0], [WIDTH // 2, HEIGHT], 3)
    pygame.draw.line(win, WHITE, [PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(win, WHITE, [WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1)

    # Update ball position
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Collision with top or bottom wall
    if ball_pos[1] - BALL_RADIUS <= 0 or ball_pos[1] + BALL_RADIUS >= HEIGHT:
        ball_vel[1] = -ball_vel[1]

    # Draw ball
    pygame.draw.circle(win, WHITE, ball_pos, BALL_RADIUS)

    # Update paddles' positions
    if 0 <= paddle1_pos + paddle1_vel <= HEIGHT - PAD_HEIGHT:
        paddle1_pos += paddle1_vel
    if 0 <= paddle2_pos + paddle2_vel <= HEIGHT - PAD_HEIGHT:
        paddle2_pos += paddle2_vel

    # Draw paddles
    pygame.draw.rect(win, WHITE, (PAD_WIDTH, paddle1_pos, PAD_WIDTH, PAD_HEIGHT))
    pygame.draw.rect(win, WHITE, (WIDTH - 2 * PAD_WIDTH, paddle2_pos, PAD_WIDTH, PAD_HEIGHT))

    # Ball collision with paddles
    if ball_pos[0] - BALL_RADIUS <= PAD_WIDTH and paddle1_pos <= ball_pos[1] <= paddle1_pos + PAD_HEIGHT:
        ball_vel[0] = -ball_vel[0] * 1.1
        ball_vel[1] = ball_vel[1] * 1.1
    elif ball_pos[0] - BALL_RADIUS <= PAD_WIDTH:
        score2 += 1
        spawn_ball(RIGHT)

    if ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH and paddle2_pos <= ball_pos[1] <= paddle2_pos + PAD_HEIGHT:
        ball_vel[0] = -ball_vel[0] * 1.1
        ball_vel[1] = ball_vel[1] * 1.1
    elif ball_pos[0] + BALL_RADIUS >= WIDTH - PAD_WIDTH:
        score1 += 1
        spawn_ball(LEFT)

    # Draw scores
    score1_text = font.render(str(score1), 1, WHITE)
    score2_text = font.render(str(score2), 1, WHITE)
    win.blit(score1_text, (WIDTH // 4, 20))
    win.blit(score2_text, (3 * WIDTH // 4, 20))

    pygame.display.update()

# Main game loop
def main():
    global paddle1_vel, paddle2_vel
    run = True
    clock = pygame.time.Clock()
    new_game()

    while run:
        clock.tick(60)  # Frame rate: 60 FPS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    paddle1_vel = -4
                elif event.key == pygame.K_s:
                    paddle1_vel = 4
                elif event.key == pygame.K_UP:
                    paddle2_vel = -4
                elif event.key == pygame.K_DOWN:
                    paddle2_vel = 4
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    paddle1_vel = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    paddle2_vel = 0

        draw(win)

    pygame.quit()

if __name__ == "__main__":
    main()
