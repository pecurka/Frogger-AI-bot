import pygame
import random
import time

pygame.init()
screen_width = 350
screen_height = 400
white = (255, 255, 255)

finish = False   # Check if application is running
fps = 20  # Simulation speed

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Frogger-AI-bot')
clock = pygame.time.Clock()

# The main game loop
while not finish:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finish = True

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()
