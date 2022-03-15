import pygame
import textsurfaces

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
running = True


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("not sure")
pygame.key.set_repeat(500, 50)

textbox = textsurfaces.TextLine("lol", None, 40, (255, 255, 255))

while running:
    events = pygame.event.get()

    screen.fill((0, 0, 0))
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            running = False

    textbox.update(events)
    screen.blit(textbox.surface, (10, 10))

    clock.tick(120)
    pygame.display.flip()
