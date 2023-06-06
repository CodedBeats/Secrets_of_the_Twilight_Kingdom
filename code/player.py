import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # hitbox to be slightly smaller than sprite rect and therefore gives illusion of depth in overlapping
        self.hitbox = self.rect.inflate(0, -20)

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites


    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0


    def move(self, speed):
        # this is added to stop player being faster on angled directional movement
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        # x movement
        self.hitbox.x += self.direction.x * speed
        # check for collision
        self.collision("horizontal")

        # y movement
        self.hitbox.y += self.direction.y * speed
        # check for collision
        self.collision("vertical")

        # update rect to be exactly centered with hitbox
        self.rect.center = self.hitbox.center


    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                # if sprite overlaps/collides
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: # moving right
                        # stop right of moving sprite overlapping with left of static sprite
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: # moving left
                        # stop left of moving sprite overlapping with right of static sprite
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                # if sprite overlaps/collides
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # moving down
                        # stop bottom of moving sprite overlapping with top of static sprite
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # moving up
                        # stop top of moving sprite overlapping with bottom of static sprite
                        self.hitbox.top = sprite.hitbox.bottom


    def update(self):
        self.input()
        self.move(self.speed)
