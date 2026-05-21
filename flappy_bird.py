import pygame
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 500, 750
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

CLOCK, FPS = pygame.time.Clock(), 60

BIRD_X, BIRD_SIZE = 50, (38, 28)
GRAVITY, FLAP_STRENGTH = 3, -6
OBSTACLE_WIDTH, OBSTACLE_GAP, OBSTACLE_SPEED = 70, 160, -4

BG = pygame.transform.scale(pygame.image.load("background.jpg"), (SCREEN_WIDTH, SCREEN_HEIGHT))
BIRD = pygame.transform.scale(pygame.image.load("bird1.png"), BIRD_SIZE)

FONT_L, FONT_M, FONT_S, FONT_SCORE = (
    pygame.font.Font("freesansbold.ttf", 64),
    pygame.font.Font("freesansbold.ttf", 32),
    pygame.font.Font("freesansbold.ttf", 22),
    pygame.font.Font("freesansbold.ttf", 36),
)


def center(text, y):
    return SCREEN_WIDTH // 2 - text.get_width() // 2, y


def start_screen():
    SCREEN.blit(BG, (0, 0))

    t = FONT_L.render("FLAPPY BIRD", 1, (255, 220, 0))
    p = FONT_M.render("Press SPACE to Start", 1, (255, 255, 255))

    SCREEN.blit(t, center(t, 200))
    SCREEN.blit(p, center(p, 310))
    pygame.display.update()


def game_over(score):
    SCREEN.blit(pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA), (0, 0))

    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    SCREEN.blit(overlay, (0, 0))

    g = FONT_L.render("GAME OVER", 1, (220, 40, 40))
    s = FONT_M.render(f"Score: {score}", 1, (255, 255, 255))
    r = FONT_S.render("Press SPACE to Play Again", 1, (200, 200, 200))

    SCREEN.blit(g, center(g, 240))
    SCREEN.blit(s, center(s, 340))
    SCREEN.blit(r, center(r, 510))
    pygame.display.update()


def wait(start, score):
    (start_screen() if start else game_over(score))
    while True:
        CLOCK.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); raise SystemExit
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                return


def main():
    first, high = True, 0

    while True:
        wait(first, 0)
        first = False

        bird_y, bird_v = 300, 0
        obs_x, top = SCREEN_WIDTH, random.randint(120, 430)
        score, passed = 0, False

        running = True
        while running:
            CLOCK.tick(FPS)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); raise SystemExit
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                    bird_v = FLAP_STRENGTH
                if e.type == pygame.KEYUP and e.key == pygame.K_SPACE:
                    bird_v = GRAVITY

            bird_y += bird_v
            obs_x += OBSTACLE_SPEED

            if obs_x + OBSTACLE_WIDTH < BIRD_X and not passed:
                score += 1
                passed = True

            if obs_x < -OBSTACLE_WIDTH:
                obs_x, top, passed = SCREEN_WIDTH, random.randint(120, 430), False

            bottom = top + OBSTACLE_GAP

            bird = pygame.Rect(BIRD_X, bird_y, *BIRD_SIZE)
            top_r = pygame.Rect(obs_x, 0, OBSTACLE_WIDTH, top)
            bot_r = pygame.Rect(obs_x, bottom, OBSTACLE_WIDTH, SCREEN_HEIGHT - bottom)

            if bird.colliderect(top_r) or bird.colliderect(bot_r):
                running = False

            SCREEN.blit(BG, (0, 0))
            SCREEN.blit(BIRD, (BIRD_X, bird_y))
            pygame.draw.rect(SCREEN, (211, 253, 117), top_r)
            pygame.draw.rect(SCREEN, (211, 253, 117), bot_r)

            SCREEN.blit(FONT_SCORE.render(str(score), 1, (255, 255, 255)), (230, 20))
            pygame.display.update()

        high = max(high, score)


main()
pygame.quit()
