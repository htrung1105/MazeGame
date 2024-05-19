import pygame
import math
import sys
from database import UserDatabase

WIDTH, HEIGHT = 1300, 750 
class Clock:
    def __init__(self, x, y):
        self.minutes = 0
        self.seconds = 0
        self.x = x
        self.y = y

    def update(self):
        self.seconds += 1
        if self.seconds == 60:
            self.minutes += 1
            self.seconds = 0
        if self.minutes == 60:
            self.minutes = 0

    def display_time(self):
        return f"{self.minutes:02d}:{self.seconds:02d}"



class Button_Image1():
    def __init__(self, image, pos, width, height, radius):
        self.img = pygame.image.load(image).convert_alpha()
        self.image = pygame.transform.smoothscale(self.img, (WIDTH, HEIGHT))
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.width = width
        self.height = height
        self.radius = radius
        
    def draw(self,screen):
        screen.blit(self.image, (0, 0))

    def check_collision(self, position):
        if self.radius is not None:  
            distance = math.sqrt((position[0] - self.x_pos) ** 2 + (position[1] - self.y_pos) ** 2)
            return distance <= self.radius
        else:
            return (self.x_pos <= position[0] <= self.x_pos + self.width) and (self.y_pos <= position[1] <= self.y_pos + self.height)


        

class Button_Image():
    def __init__(self, x, y, image, scale):
        self.original_image = image
        self.scaled_image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.scaled_image.get_rect(topleft=(x, y))
        self.clicked = False

    def draw(self, surface):
        action = False
        # Get mouse position
        pos = pygame.mouse.get_pos()

        # Check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Enhance the scaled image
        enhanced_image_surface = self.enhance_image(self.scaled_image)

        # Draw button on screen
        surface.blit(enhanced_image_surface, self.rect.topleft)

        return action


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



class TextBox:
    def __init__(self, x, y, width, height, text=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (200, 200, 200)
        self.font = pygame.font.Font(None, 60)
        self.text = text
        self.txt_surface = self.font.render(self.text, True, (0, 0, 0))
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = (255, 255, 255) if self.active else (200, 200, 200)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, (0, 0, 0))

    def update(self):
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))

class Game:
    def __init__(self, play_mode, name_game, difficult, play_mode_game):
        self.WIDTH, self.HEIGHT = 1300, 750
        self.WHITE = (255, 255, 255)
        self.FONT = pygame.font.Font(None, 60)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Game Menu")
        self.buttons = []
        self.text_boxes = []
        self.buttons_image = []
        self.buttons_image1 = []
        self.playmode=play_mode 
        self.name=name_game
        self.Difficult=difficult
        self.current_page = play_mode_game
        self.db = UserDatabase('user_data.json')
        self.home_background1 = pygame.image.load("assets/start_game.png")
        self.home_background2 = pygame.image.load("assets/Auto_mode.png")
        self.clock = Clock(50, 50)
    


    def add_button(self, button):
        self.buttons.append(button)

    def draw_text(self, text, position):
        text_surface = self.FONT.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(topleft=position)
        self.screen.blit(text_surface, text_rect)

    
    def reset_page(self):
        
        self.buttons = []
        self.text_boxes = []
        self.buttons_image= []
        self.buttons_image1 = []

    def add_button(self, button):
        self.buttons.append(button)

    def add_text_box(self, textbox):
        self.text_boxes.append(textbox)
        
    def add_button_img(self, button_image):
        self.buttons_image.append(button_image)
        
    def add_button_img1(self, button_image1):
        self.buttons_image1.append(button_image1)

    def draw_text(self, text, position):
        text_surface = self.FONT.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(topleft=position)
        self.screen.blit(text_surface, text_rect)
    

    def draw_page(self, page_name):
     if page_name == 'Playauto':
       background_image = self.home_background2
       self.screen.blit(background_image, (0, 0))
     if page_name == 'Playyourself':
        background_image = self.home_background1
        self.screen.blit(background_image, (0, 0))
        
     for button in self.buttons:
        if isinstance(button, Button):
            button.draw(self.screen)
     for button_image in self.buttons_image:
        if isinstance(button_image, Button_Image):
            button_image.draw(self.screen)
     for button_image1 in self.buttons_image1:
        if isinstance(button_image1, Button_Image1):
            button_image1.draw(self.screen)
     for textbox in self.text_boxes:
        textbox.draw(self.screen)

     pygame.display.flip()
     
    def handle_button_click(self, button):
        if self.current_page == "Playauto":
            if button.text == '':
                pygame.quit()
                sys.exit()
        if self.current_page == "Playyourself":
            if button.text == '':
                pygame.quit()
                sys.exit()
 ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##                
    ## Hướng dẫn xây dựng button_imge
        #button1.png : la nut dung cho playyourself
        #button2.png: la nut dung cho quay phim =))
        #button3.png: goi y
        #button4.png: cau hoi
        #button5.png:settings
        #button6.png:vô địch
        #button8.png: nut tiep tuc
        #button9.png: quay lại
        #button10.png:nut dung cho auto_mode
 ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##      
    def run_button0():
        pass
        
        
        
        

    def run_home_playauto(self):
        self.reset_page()
        home_page_buttons = [
            Button('', (0, 0), (170, 50)),
            Button(self.name, (945, 286), (250, 50)),
            Button(self.playmode, (945, 350), (250, 50)),
            Button(self.Difficult, (945, 410),(250, 50)),
        ]
            
        

        self.add_button(home_page_buttons[0])
        self.add_button(home_page_buttons[1])
        self.add_button(home_page_buttons[2])
        self.add_button(home_page_buttons[3])
      

        home_page_buttons_img1 = [
            Button_Image1('assets/button10.png', (self.WIDTH//2 , self.HEIGHT//2 ), None, None, 85),
            Button_Image1('assets/button9.png', (self.WIDTH//2 , self.HEIGHT//2 ), None, None, 85),
            Button_Image1('assets/button4.png', (self.WIDTH//2 , self.HEIGHT//2 ), None, None, 85),
            Button_Image1('assets/button5.png', (self.WIDTH//2 , self.HEIGHT//2 ), None, None, 85),
            Button_Image1('assets/button6.png', (self.WIDTH//2 , self.HEIGHT//2 ), None, None, 85),
            Button_Image1('assets/button7.png', (self.WIDTH//2 , self.HEIGHT//2 ), None, None, 85)
            
     ]

        self.add_button_img1(home_page_buttons_img1[0])
        self.add_button_img1(home_page_buttons_img1[1])
        self.add_button_img1(home_page_buttons_img1[2])
        self.add_button_img1(home_page_buttons_img1[3])
        self.add_button_img1(home_page_buttons_img1[4])
        self.add_button_img1(home_page_buttons_img1[5])
     

        while self.current_page == "Playauto":
            self.draw_page('Playauto')
            time_text = self.FONT.render(self.clock.display_time(), True, ((211,151,68)))
            self.screen.blit(time_text, (990, 500))
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Lặp qua tất cả các nút hình ảnh để kiểm tra va chạm
                    for button_image1 in self.buttons_image1:
                        if button_image1[0].check_collision(pygame.mouse.get_pos()):
                            self.run_button0()
                        if button_image1[1].check_collision(pygame.mouse.get_pos()):
                            self.run_buttonreset()
                        if button_image1[2].check_collision(pygame.mouse.get_pos()):
                            self.run_button2()
                        if button_image1[3].check_collision(pygame.mouse.get_pos()):
                            self.run_button3()
                        if button_image1[4].check_collision(pygame.mouse.get_pos()):
                            self.run_button4()
                        if button_image1[5].check_collision(pygame.mouse.get_pos()):
                            self.run_button5()
            self.clock.update()
            pygame.display.flip()
            pygame.time.wait(1000) 
            
    def run_home_playyourself(self):
        self.reset_page()
        home_page_buttons = [
            Button('', (0, 0), (170, 50)),
            Button(self.name, (945, 286), (250, 50)),
            Button(self.playmode, (945, 350), (250, 50)),
            Button(self.Difficult, (945, 410),(250, 50)),
        ]
            
        

        self.add_button(home_page_buttons[0])
        self.add_button(home_page_buttons[1])
        self.add_button(home_page_buttons[2])
        self.add_button(home_page_buttons[3])
      

        home_page_buttons_img1 = [
            Button_Image1('assets/button1.png', (self.WIDTH//2 , self.HEIGHT//2 ), None, None, 85),
            Button_Image1('assets/button2.png', (self.WIDTH//2 , self.HEIGHT//2 ), None, None, 85),
            Button_Image1('assets/button3.png', (self.WIDTH//2 , self.HEIGHT//2 ), None, None, 85),
            Button_Image1('assets/button4.png', (self.WIDTH//2 , self.HEIGHT//2 ), None, None, 85),
            Button_Image1('assets/button5.png', (self.WIDTH//2 , self.HEIGHT//2 ), None, None, 85),
            Button_Image1('assets/button6.png', (self.WIDTH//2 , self.HEIGHT//2 ), None, None, 85),
            Button_Image1('assets/button7.png', (self.WIDTH//2 , self.HEIGHT//2 ), None, None, 85)
            
     ]

        self.add_button_img1(home_page_buttons_img1[0])
        self.add_button_img1(home_page_buttons_img1[1])
        self.add_button_img1(home_page_buttons_img1[2])
        self.add_button_img1(home_page_buttons_img1[3])
        self.add_button_img1(home_page_buttons_img1[4])
        self.add_button_img1(home_page_buttons_img1[5])
        self.add_button_img1(home_page_buttons_img1[6])
     

        while self.current_page == "Playyourself":
            self.draw_page('Playyourself')
            time_text = self.FONT.render(self.clock.display_time(), True, ((211,151,68)))
            self.screen.blit(time_text, (990, 470))
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Lặp qua tất cả các nút hình ảnh để kiểm tra va chạm
                    for button_image1 in self.buttons_image1:
                        if button_image1.check_collision(pygame.mouse.get_pos()):
                            self.run_button()
                             
            self.clock.update()
            pygame.display.flip()
            pygame.time.wait(1000) 
 
    def run(self):
        running = True
        
        while running:
       
         if self.current_page == "Playauto":
            self.run_home_playauto()
            
            
         elif self.current_page == "Playyourself":
            self.run_home_playyourself()
         
       
         for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running= False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(event.pos):
                        self.handle_button_click(button)
        
         pygame.display.flip()
       
        

if __name__ == "__main__":
    play_mode_game = ["Playauto" ,"Playyourself"]
    # Thay đổi chế độ chơi ở đây
    play_mode, name_game, difficult= "Auto", "Sheet1" , "Hard"
    pygame.init()  # Khởi tạo pygame
    game = Game(play_mode, name_game, difficult,play_mode_game[1])  # Khởi tạo trò chơi
    game.run()     # Chạy trò chơi