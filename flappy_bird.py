import pygame
import random

pygame.init()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 750
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
OBSTACLE_MIN_TOP = 120
OBSTACLE_MAX_TOP = 430
OBSTACLE_COLOR = (211, 253, 117)

COUNTDOWN_SECONDS = 3

BACKGROUND_IMAGE = pygame.transform.scale(
    pygame.image.load("background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT)
)
BIRD_IMAGE = pygame.transform.scale(pygame.image.load("bird1.png"), BIRD_SIZE)

FONT_LARGE = pygame.font.Font("freesansbold.ttf", 64)
FONT_MEDIUM = pygame.font.Font("freesansbold.ttf", 32)
FONT_SMALL = pygame.font.Font("freesansbold.ttf", 22)
FONT_SCORE = pygame.font.Font("freesansbold.ttf", 36)
FONT_COUNTDOWN = pygame.font.Font("freesansbold.ttf", 80)


def draw_background():
    SCREEN.blit(BACKGROUND_IMAGE, (0, 0))


def draw_bird(y):
    SCREEN.blit(BIRD_IMAGE, (BIRD_X, y))


def draw_obstacle(x, top_height):
    bottom_y = top_height + OBSTACLE_GAP
    bottom_height = SCREEN_HEIGHT - bottom_y
    pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (x, 0, OBSTACLE_WIDTH, top_height))
    pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (x, bottom_y, OBSTACLE_WIDTH, bottom_height))


def check_collision(obstacle_x, top_height, bird_y):
    bird_right = BIRD_X + BIRD_SIZE[0]
    bird_bottom = bird_y + BIRD_SIZE[1]
    obstacle_right = obstacle_x + OBSTACLE_WIDTH
    bottom_y = top_height + OBSTACLE_GAP

    horizontally_aligned = obstacle_x < bird_right and obstacle_right > BIRD_X
    if horizontally_aligned:
        if bird_y < top_height or bird_bottom > bottom_y:
            return True
    return False


def draw_score(score):
    padding_x = 14
    padding_y = 8
    text_surface = FONT_SCORE.render(str(score), True, (255, 255, 255))
    text_w, text_h = text_surface.get_size()
    box_w = text_w + padding_x * 2
    box_h = text_h + padding_y * 2
    box_x = (SCREEN_WIDTH - box_w) // 2
    box_y = 18

    shadow_surface = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    shadow_surface.fill((0, 0, 0, 100))
    SCREEN.blit(shadow_surface, (box_x + 3, box_y + 3))

    bg_surface = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    bg_surface.fill((0, 0, 0, 160))
    SCREEN.blit(bg_surface, (box_x, box_y))

    pygame.draw.rect(SCREEN, (255, 255, 255), (box_x, box_y, box_w, box_h), 2, border_radius=6)
    SCREEN.blit(text_surface, (box_x + padding_x, box_y + padding_y))


def draw_start_screen():
    draw_background()
    title = FONT_LARGE.render("FLAPPY BIRD", True, (255, 220, 0))
    SCREEN.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
    prompt = FONT_MEDIUM.render("Press SPACE to Start", True, (255, 255, 255))
    SCREEN.blit(prompt, (SCREEN_WIDTH // 2 - prompt.get_width() // 2, 310))
    pygame.display.update()


def draw_game_over_screen(score, high_score):
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    SCREEN.blit(overlay, (0, 0))

    go_text = FONT_LARGE.render("GAME OVER", True, (220, 40, 40))
    SCREEN.blit(go_text, (SCREEN_WIDTH // 2 - go_text.get_width() // 2, 240))

    score_text = FONT_MEDIUM.render(f"Score: {score}", True, (255, 255, 255))
    SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 340))

    best_text = FONT_MEDIUM.render(f"Best:  {high_score}", True, (255, 220, 0))
    SCREEN.blit(best_text, (SCREEN_WIDTH // 2 - best_text.get_width() // 2, 390))

    if score >= high_score and score > 0:
        new_best = FONT_SMALL.render("NEW HIGH SCORE!", True, (255, 100, 100))
        SCREEN.blit(new_best, (SCREEN_WIDTH // 2 - new_best.get_width() // 2, 450))

    restart_text = FONT_SMALL.render("Press SPACE to Play Again", True, (200, 200, 200))
    SCREEN.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 510))

    pygame.display.update()


def run_countdown():
    for count in range(COUNTDOWN_SECONDS, 0, -1):
        draw_background()
        draw_bird(300)
        number = FONT_COUNTDOWN.render(str(count), True, (255, 255, 255))
        shadow = FONT_COUNTDOWN.render(str(count), True, (0, 0, 0))
        cx = SCREEN_WIDTH // 2 - number.get_width() // 2
        cy = SCREEN_HEIGHT // 2 - number.get_height() // 2
        SCREEN.blit(shadow, (cx + 3, cy + 3))
        SCREEN.blit(number, (cx, cy))
        pygame.display.update()
        pygame.time.wait(1000)


def wait_for_input(first_run, score, high_score):
    if first_run:
        draw_start_screen()
    else:
        draw_game_over_screen(score, high_score)

    waiting = True
    while waiting:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False


def main():
    high_score = 0
    first_run = True
    score = 0

    while True:
        wait_for_input(first_run, score, high_score)
        first_run = False

        run_countdown()

        bird_y = 300
        bird_y_change = 0
        obstacle_x = SCREEN_WIDTH
        top_height = random.randint(OBSTACLE_MIN_TOP, OBSTACLE_MAX_TOP)
        score = 0
        scored_this_obstacle = False

        running = True
        while running:
            CLOCK.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
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

            if check_collision(obstacle_x, top_height, bird_y):
                running = False

            draw_background()
            draw_obstacle(obstacle_x, top_height)
            draw_bird(bird_y)
            draw_score(score)
            pygame.display.update()


main()