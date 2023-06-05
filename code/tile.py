import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/test/rock.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # hitbox to be slightly smaller than sprite rect and therefore gives illusion of depth in overlapping
        self.hitbox = self.rect.inflate(0, -10)
