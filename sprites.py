import pygame
from pygame.locals import (K_a, K_w, K_d, K_s, KEYDOWN, K_ESCAPE, QUIT)
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("C:/Users/clw-h/OneDrive/Pictures/basket.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.HEIGHT = 570  # height to be positioned
        self.capture_area_width_sub = 50
        self.capture_area_rect = pygame.Rect((self.rect.left+self.capture_area_width_sub/2, self.rect.top + 35),
                                             (self.rect.width - self.capture_area_width_sub, 1))  # capture area

        self.rect.top = self.HEIGHT

    # move the rect
    def move(self, pressed_keys):
        if pressed_keys[K_a]:
            self.rect.move_ip(-4, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(4, 0)

        # move capture area with sprite
        self.capture_area_rect.topleft = (self.rect.left+self.capture_area_width_sub/2, self.rect.top + 35)


class Object(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("C:/Users/clw-h/OneDrive/Pictures/apple.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.creation_time = pygame.time.get_ticks()
        self.velocity = 0  # initial velocity
        self.can_fall = True
        self.splattered_start_time = None  # time when sprite has hit the ground
        self.splatter_height = SCREEN_HEIGHT - 150  # distance from the bottom of the screen for sprite to stop
        self.able_to_capture = True
        self.splattered_alive_time = 500  # how long for sprite to live after hitting the ground in ms
        self.alpha_value = 255  # transparency value 0-255

        self.rect.topleft = (  # spawn somewhere around the width of screen, 2 rect heights above the screen
            random.randint(0, SCREEN_WIDTH - self.rect.width),
            0 - self.rect.height*2
        )

    def update(self):
        if self.can_fall:
            final_velocity = self.velocity + 2 * (pygame.time.get_ticks() - self.creation_time)/100000

            self.velocity = final_velocity
            self.rect.move_ip(0, final_velocity)

        if self.rect.bottom >= self.splatter_height and self.can_fall:  # if the sprite has hit the ground...
            self.splattered_start_time = pygame.time.get_ticks()
            self.able_to_capture = False
            self.can_fall = False  # prevent sprite from falling
            self.image = pygame.image.load("C:/Users/clw-h/OneDrive/Pictures/squished_apple.png").convert_alpha()

        elif not self.can_fall:  # prevent *splattered_start_time from being updated

            # check if sprite has lived longer/equal than *splattered_alive_time
            if pygame.time.get_ticks() - self.splattered_start_time >= self.splattered_alive_time:

                if self.alpha_value > 0:  # reduce alpha until transparency is 0
                    self.alpha_value -= 255 / 60  # fade image over the span of 60 frames
                    self.image.set_alpha(self.alpha_value)
                else:  # if the image is fully transparent...
                    self.kill()


if __name__ == "__main__":
    # catch apples in basket
    #create racing game
    pass
