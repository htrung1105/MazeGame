import pygame

BASE_IMG_PATH = 'assets/Display/'

def load_image(path, scale = 1, width = None, height = None):
    img = pygame.image.load(BASE_IMG_PATH + path).convert_alpha()
    if width is None:
        width = img.get_width()
    if height is None:
        height = img.get_height()

    img = pygame.transform.scale(img, (width * scale, height * scale))
    return img
