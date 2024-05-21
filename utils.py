from os import walk
import pygame
from settings import setting

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            image_surf = pygame.transform.smoothscale(image_surf, (setting.tilesize, setting.tilesize))
            surface_list.append(image_surf)

    return surface_list