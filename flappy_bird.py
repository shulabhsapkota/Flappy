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
    if obstacle_x < -OBSTACLE_WIDTH:
        obstacle_x = SCREEN_WIDTH
        top_height = random.randint(OBSTACLE_MIN_TOP, OBSTACLE_MAX_TOP)
    bottom_y = top_height + OBSTACLE_GAP


    bird_right = BIRD_X + BIRD_SIZE[0]
    bird_bottom = bird_y + BIRD_SIZE[1]
    if obstacle_x < bird_right and (obstacle_x + OBSTACLE_WIDTH) > BIRD_X:
        
        if bird_y < top_height or bird_bottom > bottom_y:
            running = False  

    SCREEN.fill((135, 206, 250)) 
    pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (obstacle_x, 0, OBSTACLE_WIDTH, top_height))
    pygame.draw.rect(SCREEN, OBSTACLE_COLOR, (obstacle_x, bottom_y, OBSTACLE_WIDTH, SCREEN_HEIGHT - bottom_y))
    
    pygame.draw.rect(SCREEN, (255, 255, 0), (BIRD_X, bird_y, BIRD_SIZE[0], BIRD_SIZE[1]))

    pygame.display.update()  

pygame.quit()
