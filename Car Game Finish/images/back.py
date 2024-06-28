import pygame
from pygame.locals import *
import random

pygame.init()

# Create the window
width = 700
height = 700
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

# Colors
gray = (100, 100, 100)
sand = (237, 215, 201)
red = (200, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
yellow = (255, 182, 1)

# Game settings
gameover = False
speed = 2
score = 0

# marker size
marker_width = 10
marker_height = 50

# Road and edge markers
road = (100, 0, 100, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0, marker_width, height)


#game loop
clock = pygame.time.Clock()
fps = 120
running = True
while running :

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Draw the grass
    screen.fill(sand)

    #draw the road
    pygame.draw.rect(screen, gray, road)

    pygame.display.update()

    pygame.quit()