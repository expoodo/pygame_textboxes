import pygame
import text_test_classes
from pygame.locals import (K_a, K_w, K_d, K_s, KEYDOWN, K_ESCAPE, QUIT)

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
running = True

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, pygame.SCALED)

pygame.display.set_caption("Text")
pygame.key.set_repeat(500, 50)  # fire keydown every 50ms after 500ms of being called

label = text_test_classes.TextSurface(screen, "hey", font_file="OpenSans-Bold.ttf")

while running:
    events = pygame.event.get()
    screen.fill((0, 0, 0))

    for event in events:
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    label.update(events)
    label.rect.topleft = (0, 0)
    screen.blit(label.surface, label.rect)

    clock.tick(120)
    pygame.display.flip()
