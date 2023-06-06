import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load("./graphics/test/player.png").convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        # hitbox to be slightly smaller than sprite rect and therefore gives illusion of depth in overlapping
        self.hitbox = self.rect.inflate(0, -20)

        # graphics setup
        self.import_player_assets()
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.15

        # movement
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        self.obstacle_sprites = obstacle_sprites

    
    def import_player_assets(self):
        character_path = "./graphics/player/"
        # player dictionary
        self.animations = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "right-idle": [],
            "left-idle": [],
            "up-idle": [],
            "down-idle": [],
            "right_attack": [],
            "left-attack": [],
            "up-attack": [],
            "down-attack": [],
        }

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)


    def input(self):
        # stop movement while attacking
        if not self.attacking:
            keys = pygame.key.get_pressed()
            mouse_pressed = pygame.mouse.get_pressed()

            # movement input
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = "up"
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[pygame.K_d]:
                self.direction.x = 1
                self.status = "right"
            elif keys[pygame.K_a]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0

            # attack input
            if mouse_pressed[0]:
                # left click
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print("left click - attack")

            # magic input
            if mouse_pressed[2]:
                # right click
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
                print("right click - magic")


    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not "idle" in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"

        # attack status
        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not "attack" in self.status:
                if "idle" in self.status:
                    # overwrite idle
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")


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


    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        
        # timer to allow players to only attack on cooldown
        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False


    def animate(self):
        animation = self.animations[self.status]

        # loop pver the frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        # set the image
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)


    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
