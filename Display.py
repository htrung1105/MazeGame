import pygame
import sys
from pygame.locals import *

class Button:
    def __init__(self, text, position, size):
        self.text = text
        self.position = position
        self.size = size
        self.rect = pygame.Rect(position, size)
        self.default_color = (211,151,68)   
        self.hover_color = (220,20,60) 
        self.click_color = (220,20,60) 
        self.color = self.default_color
        self.FONT = pygame.font.Font(None, 60)
        self.alpha = 255
        self.blink_count = 0
        self.blink_frequency = 20  # Cấu hình tần suất nhấp nháy
        self.blink_color = (220,20,60)   # Màu của hiệu ứng nhấp nháy
        
  

    def draw(self, surface):
        
        button_surface = pygame.Surface(self.size, pygame.SRCALPHA)
        gradient = pygame.Surface((self.size[0], self.size[1] // 2), pygame.SRCALPHA)
        button_surface.blit(gradient, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        button_surface.blit(gradient, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)



        surface.blit(button_surface, self.position)

        text_surface = self.FONT.render(self.text, True, (211,151,68))  # Màu vàng
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
     
    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update_color(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.color = self.hover_color
            if pygame.mouse.get_pressed()[0]:
                self.color = self.click_color
        else:
            self.color = self.default_color
        
        # Hiệu ứng nhấp nháy khi nút được nhấn
        if self.color == self.click_color:
            self.blink_count += 1
            if self.blink_count % self.blink_frequency == 0:
                self.blink_color = (255 - self.blink_color[0], 0, 0)  # Thay đổi màu giữa đỏ và trắng
        else:
            self.blink_color = (220,20,60)  # Reset màu nhấp nháy khi không được nhấn

class Button_Image():
    def __init__(self, image_path, x, y , scale):
        BASE_PATH = 'assets/button/'
        self.original_image = pygame.image.load(BASE_PATH + image_path)
        self.scaled_image = pygame.transform.scale(self.original_image, scale) # Thay đổi kích thước tùy ý
        self.rect = self.scaled_image.get_rect(topleft=(x, y))
        self.clicked = False

    def draw(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.scaled_image, self.rect.topleft)

        return action

class Display():
    def __init__(self, screen):
        pygame.init()
        self.screen = screen
        self.clock = pygame.time.Clock()

        x, y = 275, 150
        self.Display= Button_Image('button1.png', x, y,(800,400))
        self.Button1= Button_Image('button2.png', x + 180, y + 190,(70,70))
        self.Button2= Button_Image('button3.png', x + 280, y + 190,(70,70))
        self.Button3=Button_Image('button4.png', x + 380, y + 190,(70,70))
        self.Button4=Button_Image('button5.png', x + 480, y + 190,(70,70))
        self.Button5=Button_Image('button6.png', x + 570, y + 120,(40,40))
        self.buttons = []
    
    def reset_page(self):
        self.buttons = []
    
    def add_button(self, button):
        self.buttons.append(button)
        
    def draw_page(self):
        for button in self.buttons:
            if isinstance(button, Button):
                button.draw(self.screen)

    def run(self):
        self.reset_page()
        running =  True
        home_page_buttons = []
        
        for button in home_page_buttons:
            self.add_button(button)
    
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_page()

            display=self.Display.draw(self.screen)
            Home= self.Button1.draw(self.screen)
            Reset = self.Button2.draw(self.screen)
            Zoom= self.Button3.draw(self.screen)
            Help= self.Button4.draw(self.screen)
            Stop= self.Button5.draw(self.screen)
            
            if Home:
                print("Home")
            if Reset:
                print("Reset")
            if Zoom:
                print("Zoom")
            if Help:
                print("Help")
            if Stop:
                running = False

            pygame.display.update()
            self.clock.tick(60)