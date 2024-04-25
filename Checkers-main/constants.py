import pygame

WIDTH, HEIGHT = 670,670 
ROWS, COLS = 8,8
SQUARE_SIZE = WIDTH//COLS

# rgb
red='RED IS WINNER'
white='WHITE IS WINNER'
RED = (200, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
GREY = (128,128,128)
        #for scaling tha crown on the piece we use inbuilt function of pygame
CROWN = pygame.transform.scale(pygame.image.load('crown.png'), (35, 25))