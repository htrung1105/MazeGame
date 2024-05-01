import pygame

WIDTH, HEIGHT = 1300, 750
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

if __name__ == '__main__':
    main()