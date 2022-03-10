import pygame
from pygame.locals import (K_a, K_w, K_d, K_s, KEYDOWN, K_ESCAPE, QUIT)
import sprites

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
ADD_OBJ = pygame.USEREVENT + 1
running = True


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, pygame.SCALED)
background_img = pygame.image.load("C:/Users/clw-h/OneDrive/Pictures/background.png").convert()
all_obj = pygame.sprite.Group()

pygame.display.set_caption("Game")
pygame.time.set_timer(ADD_OBJ, 500)  # blit object onto screen every 500ms

player = sprites.Player()
score = pygame.font.Font(None, 30)
score_surface = score.render("TEST: 0", True, (255, 0, 0))

while running:
    events = pygame.event.get()

    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

        if event.type == ADD_OBJ:
            new_obj = sprites.Object()

            all_obj.add(new_obj)

    pressed_keys = pygame.key.get_pressed()

    screen.blit(background_img, background_img.get_rect())

    screen.blit(score_surface, score_surface.get_rect())

    all_obj.draw(screen)
    all_obj.update()

    player.move(pressed_keys)
    player.rect.clamp_ip(screen.get_rect())  # keep sprite in border
    screen.blit(player.image, player.rect)

    collided_sprites = pygame.sprite.spritecollide(player, all_obj, False, pygame.sprite.collide_mask)

    if collided_sprites:  # if objects have collided with the entire sprite
        for obj in collided_sprites:
            obj_rect = obj.rect

            # if the object is intersecting with the capture area...
            if player.capture_area_rect.colliderect(obj_rect) and obj.able_to_capture:
                obj.kill()

    clock.tick(120)
    pygame.display.flip()
    # print(clock.get_fps(), len(all_obj.sprites()))
