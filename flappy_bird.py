import pygame
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 500, 750
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

CLOCK = pygame.time.Clock()
FPS = 60

BIRD_X = 50
BIRD_SIZE = (38, 28)

GRAVITY = 3
FLAP_STRENGTH = -6

OBSTACLE_WIDTH = 70
OBSTACLE_GAP = 160
OBSTACLE_SPEED = -4

COUNTDOWN_SECONDS = 3

BACKGROUND_IMAGE = pygame.transform.scale(
    pygame.image.load("background.jpg"),
    (SCREEN_WIDTH, SCREEN_HEIGHT)
)

BIRD_IMAGE = pygame.transform.scale(
    pygame.image.load("bird1.png"),
    BIRD_SIZE
)

FONT_LARGE = pygame.font.Font("freesansbold.ttf", 64)
FONT_MEDIUM = pygame.font.Font("freesansbold.ttf", 32)
FONT_SMALL = pygame.font.Font("freesansbold.ttf", 22)
FONT_SCORE = pygame.font.Font("freesansbold.ttf", 36)
FONT_COUNTDOWN = pygame.font.Font("freesansbold.ttf", 80)


def center_x(text):
    return SCREEN_WIDTH // 2 - text.get_width() // 2


def draw_background():
    SCREEN.blit(BACKGROUND_IMAGE, (0, 0))


def draw_bird(y):
    SCREEN.blit(BIRD_IMAGE, (BIRD_X, y))


def draw_score(score):

    text = FONT_SCORE.render(str(score), True, (255, 255, 255))

    padding = 12
    box_w = text.get_width() + padding * 2
    box_h = text.get_height() + padding * 2

    box_x = SCREEN_WIDTH // 2 - box_w // 2
    box_y = 18

    shadow = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    shadow.fill((0, 0, 0, 100))
    SCREEN.blit(shadow, (box_x + 3, box_y + 3))

    bg = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    bg.fill((0, 0, 0, 160))
    SCREEN.blit(bg, (box_x, box_y))

    pygame.draw.rect(
        SCREEN,
        (255, 255, 255),
        (box_x, box_y, box_w, box_h),
        2,
        border_radius=6
    )

    SCREEN.blit(text, (box_x + padding, box_y + padding))


def run_countdown():

    for count in range(COUNTDOWN_SECONDS, 0, -1):

        draw_background()
        draw_bird(300)

        number = FONT_COUNTDOWN.render(str(count), True, (255, 255, 255))
        shadow = FONT_COUNTDOWN.render(str(count), True, (0, 0, 0))

        x = center_x(number)
        y = SCREEN_HEIGHT // 2 - number.get_height() // 2

        SCREEN.blit(shadow, (x + 3, y + 3))
        SCREEN.blit(number, (x, y))

        pygame.display.update()
        pygame.time.wait(1000)


def draw_start_screen():

    draw_background()

    title = FONT_LARGE.render("FLAPPY BIRD", True, (255, 220, 0))
    prompt = FONT_MEDIUM.render("Press SPACE to Start", True, (255, 255, 255))

    SCREEN.blit(title, (center_x(title), 200))
    SCREEN.blit(prompt, (center_x(prompt), 310))

    pygame.display.update()


def draw_game_over(score):

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    SCREEN.blit(overlay, (0, 0))

    game_over = FONT_LARGE.render("GAME OVER", True, (220, 40, 40))
    score_text = FONT_MEDIUM.render(f"Score: {score}", True, (255, 255, 255))
    restart = FONT_SMALL.render("Press SPACE to Play Again", True, (200, 200, 200))

    SCREEN.blit(game_over, (center_x(game_over), 240))
    SCREEN.blit(score_text, (center_x(score_text), 340))
    SCREEN.blit(restart, (center_x(restart), 510))

    pygame.display.update()


def wait_for_input(game_over=False, score=0):

    if game_over:
        draw_game_over(score)
    else:
        draw_start_screen()

    waiting = True

    while waiting:

        CLOCK.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


first_run = True
last_score = 0

while True:

    wait_for_input(not first_run, last_score)
    first_run = False

    run_countdown()

    bird_y = 300
    bird_y_change = 0

    obstacle_x = SCREEN_WIDTH
    top_height = random.randint(120, 430)

    score = 0
    scored = False

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
        obstacle_x += OBSTACLE_SPEED

        if obstacle_x + OBSTACLE_WIDTH < BIRD_X and not scored:
            score += 1
            scored = True

        if obstacle_x < -OBSTACLE_WIDTH:
            obstacle_x = SCREEN_WIDTH
            top_height = random.randint(120, 430)
            scored = False

        bottom_y = top_height + OBSTACLE_GAP

        bird_rect = pygame.Rect(BIRD_X, bird_y, *BIRD_SIZE)

        top_rect = pygame.Rect(
            obstacle_x,
            0,
            OBSTACLE_WIDTH,
            top_height
        )

        bottom_rect = pygame.Rect(
            obstacle_x,
            bottom_y,
            OBSTACLE_WIDTH,
            SCREEN_HEIGHT - bottom_y
        )

        if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
            running = False

        draw_background()

        pygame.draw.rect(SCREEN, (211, 253, 117), top_rect)
        pygame.draw.rect(SCREEN, (211, 253, 117), bottom_rect)

        draw_bird(bird_y)
        draw_score(score)

        pygame.display.update()

    last_score = score

pygame.quit()
