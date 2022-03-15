import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 800
running = True


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE, pygame.SCALED)
pygame.display.set_caption("not sure")


while running:
    events = pygame.event.get()

    screen.fill((0, 0, 0))
    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        elif event.type == pygame.QUIT:
            running = False



    clock.tick(120)
    pygame.display.flip()
