import pygame
from game import Game

SIZE = (1600, 900)

if (__name__ == "__main__"):
    pygame.init()
    pygame.display.set_caption('60 seconds') # TODO change
    screen = pygame.display.set_mode((SIZE[0], SIZE[1]))
    Game(screen, 0)