import pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

esc = True
while esc:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            esc = False
    



    pygame.display.update()
    clock.tick(FPS)

pygame.quit()