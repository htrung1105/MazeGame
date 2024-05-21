import pygame
from utils import import_folder

class Button:
    def __init__(self):
        button_path = 'assets/button/'
        self.buttons = {'help': [], 'again': [], 'change': [], 'hint': [], 'zoom': [], 'home': []}

        for button in self.buttons.keys():
            full_path = button_path + button
            self.buttons[button] = import_folder(full_path, 40)
