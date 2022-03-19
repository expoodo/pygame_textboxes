import pygame
import textsurfaces

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
running = True


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("not sure")
pygame.key.set_repeat(500, 50)

textbox = textsurfaces.TextLine("lol", "impact", 40, (255, 255, 255), True)

textbox.text_background = (255, 0, 0)

while running:
    events = pygame.event.get()

    screen.fill((0, 0, 0))
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_F1:
                textbox.italic = not textbox.italic
        elif event.type == pygame.QUIT:
            running = False

    textbox.update(events)
    screen.blit(textbox.surface, (10, 10))

    clock.tick()
    pygame.display.flip()
