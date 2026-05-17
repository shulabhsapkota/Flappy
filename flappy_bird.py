import pygame
import random

pygame.init()
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 750
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

CLOCK = pygame.time.Clock()
FPS = 60


BACKGROUND_IMAGE = pygame.transform.scale(
    pygame.image.load("background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
BIRD_SIZE = (38, 28)
BIRD_IMAGE = pygame.transform.scale(
    pygame.image.load("bird1.png"), BIRD_SIZE
)


BIRD_X = 50
bird_y = SCREEN_HEIGHT // 2
bird_y_change = 0
GRAVITY = 3
FLAP_STRENGTH = -6


OBSTACLE_WIDTH = 70
OBSTACLE_GAP = 160
OBSTACLE_SPEED = -4
OBSTACLE_MIN_TOP = 120
OBSTACLE_MAX_TOP = 430
OBSTACLE_COLOR = (211, 253, 117)

obstacle_x = SCREEN_WIDTH
top_height = random.randint(OBSTACLE_MIN_TOP, OBSTACLE_MAX_TOP)


score = 0
high_score = 0
scored_this_obstacle = False
FONT_SCORE = pygame.font.Font("freesansbold.ttf", 36)  # Score font

running = True
while running:
    CLOCK.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_y_change = FLAP_STRENGTH
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            bird_y_change = GRAVITY


    bird_y += bird_y_change
    bird_y = max(0, min(bird_y, SCREEN_HEIGHT - BIRD_SIZE[1]))
    obstacle_x += OBSTACLE_SPEED

    if obstacle_x + OBSTACLE_WIDTH < BIRD_X and not scored_this_obstacle:
        score += 1
        if score > high_score:
            high_score = score
        scored_this_obstacle = True

    if obstacle_x < -OBSTACLE_WIDTH:
        obstacle_x = SCREEN_WIDTH
        top_height = random.randint(OBSTACLE_MIN_TOP, OBSTACLE_MAX_TOP)
        scored_this_obstacle = False
    bottom_y = top_height + OBSTACLE_GAP

    bird_right = BIRD_X + BIRD_SIZE[0]
    bird_bottom = bird_y + BIRD_SIZE[1]
    if obstacle_x < bird_right and (obstacle_x + OBSTACLE_WIDTH) > BIRD_X:
        if bird_y < top_height or bird_bottom > bottom_y:
            running = False


    SCREEN.blit(BACKGROUND_IMAGE, (0, 0))
    pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (obstacle_x, 0, OBSTACLE_WIDTH, top_height))
    pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (obstacle_x, bottom_y, OBSTACLE_WIDTH, SCREEN_HEIGHT - bottom_y))
    SCREEN.blit(BIRD_IMAGE, (BIRD_X, bird_y))

    score_text = FONT_SCORE.render(str(score), True, (255, 255, 255))
    text_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, 20))
    SCREEN.blit(score_text, text_rect)

    pygame.display.update()

pygame.quit()
