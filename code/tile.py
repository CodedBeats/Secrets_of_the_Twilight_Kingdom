import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        # handle sprites larger than default 64 x 64
        if sprite_type == "object":
            self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - TILESIZE))
        else:
            self.rect = self.image.get_rect(topleft = pos)

        # hitbox to be slightly smaller than sprite rect and therefore gives illusion of depth in overlapping
        self.hitbox = self.rect.inflate(0, -10)
