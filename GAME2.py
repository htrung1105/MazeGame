import pygame
import sys
import cv2
from user_database import UserDatabase
import cv2

# màn hình di chuyển 
class Backgroud():
    def __inint__(self,x,y,speed):
        self.x = x
        self.y =y
        self.speed = speed
        self.img= BG
        self.width= self.img.get_width()
    def draw(self): 
        DIPLAYSURF.blit(self.img(self.x, self.y ))
        DIPLAYSURF.blit(self.img(self.x + self.width , self.y ))
     
    def update(self):
        self.x = self.spped
        if self.x < -self.width:
            self.x += self.width
        

class Button_Image():
    def __init__(self, x, y, image, scale):
        self.original_image = image
        self.scaled_image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.scaled_image.get_rect(topleft=(x, y))
        self.clicked = False

    def enhance_image(self, image_surface):
        # Chuyển đổi hình ảnh Pygame thành mảng NumPy
        image_np = pygame.surfarray.pixels3d(image_surface)

        # Áp dụng các phép biến đổi ảnh để tăng độ nét
        # Ví dụ: làm mờ Gaussian với kernel size nhỏ để tăng độ nét
        blurred_image = cv2.GaussianBlur(image_np, (3, 3), 0)

        # Chuyển đổi hình ảnh trở lại thành bề mặt Pygame
        enhanced_image_surface = pygame.surfarray.make_surface(blurred_image)

        return enhanced_image_surface

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
        self.default_color = (220,20,60)   # Màu xanh lam
        self.hover_color = (220,20,60) 
        self.click_color = (220,20,60) 
        self.color = self.default_color
        self.FONT = pygame.font.Font(None, 32)
        self.alpha = 255
        self.blink_count = 0
        self.blink_frequency = 20  # Cấu hình tần suất nhấp nháy
        self.blink_color = (220,20,60)   # Màu của hiệu ứng nhấp nháy
        
  

    def draw(self, surface):
       
     button_surface = pygame.Surface(self.size, pygame.SRCALPHA)
     gradient = pygame.Surface((self.size[0], self.size[1] // 2), pygame.SRCALPHA)
     pygame.draw.rect(gradient, (255, 255, 255, 50), (0, 0, self.size[0], self.size[1] // 2) )
     pygame.draw.rect(gradient, (255, 255, 255, 0), (0, self.size[1] // 2, self.size[0], self.size[1] // 2))
     button_surface.blit(gradient, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
     button_surface.blit(gradient, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
    
     outline_color = (0, 0, 0)
     pygame.draw.rect(button_surface, outline_color, (0, 0, self.size[0], self.size[1]), 3)

     surface.blit(button_surface, self.position)

     text_surface = self.FONT.render(self.text, True, (0, 100, 0))  # Yellow color
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
        self.font = pygame.font.Font(None, 32)
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
    def __init__(self):
        self.WIDTH, self.HEIGHT = 1300, 750
        self.WHITE = (255, 255, 255)
        self.FONT = pygame.font.Font(None, 32)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Game Menu")
        self.buttons = []
        self.text_boxes = []
        self.buttons_image = []
        self.username = ""
        self.password = ""
        self.current_page = "main_menu"
        self.db = UserDatabase('user_data.json')
        self.db.load_users()
        self.background = pygame.image.load("Sweet.png")
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))
        self.home_background = pygame.image.load("tom_-_jerry.jpg")
        self.home_background = pygame.transform.scale(self.home_background, (self.WIDTH, self.HEIGHT))
        
        self.img = pygame.image.load('2.png').convert_alpha()
        self.img1=pygame.image.load ('pngtree-account-avatar-user-abstract-circle-background-flat-color-icon-png-image_1650938.jpg').convert_alpha()
        # Fade transition parameters
        self.fade_alpha = 0
        self.fade_speed = 10
        self.fade_direction = 1
        self.transitioning = False
        self.next_page = ""

    def add_button(self, button):
        self.buttons.append(button)

    def draw_text(self, text, position):
        text_surface = self.FONT.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(topleft=position)
        self.screen.blit(text_surface, text_rect)

    def fade_screen(self):
        if self.fade_direction == 1:  # Fade in
            self.fade_alpha += self.fade_speed
            if self.fade_alpha >= 255:
                self.fade_alpha = 255
                self.transitioning = False
        else:  # Fade out
            self.fade_alpha -= self.fade_speed
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.current_page = self.next_page
                self.transitioning = False

        fade_surface = pygame.Surface((self.WIDTH, self.HEIGHT), pygame.SRCALPHA)
        fade_surface.fill((0, 0, 0, self.fade_alpha))
        self.screen.blit(fade_surface, (0, 0))

    def reset_page(self):
        
        self.buttons = []
        self.text_boxes = []
        self.buttons_image= []

    def add_button(self, button):
        self.buttons.append(button)

    def add_text_box(self, textbox):
        self.text_boxes.append(textbox)
        
    def add_button_img(self, button_image):
        self.buttons_image.append(button_image)

    def draw_text(self, text, position):
        text_surface = self.FONT.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(topleft=position)
        self.screen.blit(text_surface, text_rect)
    
    def gaussian_blur(self, image):
    # Chuyển đổi hình ảnh Pygame thành mảng NumPy
     image_np = pygame.surfarray.array3d(image)

    # Áp dụng hiệu ứng làm mờ Gaussian
     blurred_image = cv2.GaussianBlur(image_np, (5, 5), 0)

    # Chuyển đổi mảng NumPy trở lại thành bề mặt Pygame
     blurred_image_surface = pygame.surfarray.make_surface(blurred_image)

     return blurred_image_surface

    def draw_page(self, page_name):
     if page_name == 'Main Menu':
        background_image = self.background
     elif page_name == 'Login Page':
        background_image = pygame.image.load("you.png").convert_alpha()
     elif page_name == 'Register Page':
        background_image = pygame.image.load("you.png").convert_alpha()
     elif page_name == 'Home Page':
        background_image = pygame.image.load("CHEESE SWIPE (1300 x 750 px).png").convert_alpha()

     background_image = pygame.transform.scale(background_image, (self.WIDTH, self.HEIGHT))
     self.screen.blit(background_image, (0, 0))
     self.draw_text(page_name, (20, 20))

     for button in self.buttons:
        if isinstance(button, Button):
            button.draw(self.screen)
     for button_image in self.buttons_image:
        if isinstance(button_image, Button_Image):
            button_image.draw(self.screen)

     for textbox in self.text_boxes:
        textbox.draw(self.screen)

     pygame.display.flip()
     

    def draw_page_with_transition(self, page_name):
        if self.transitioning:
            self.fade_screen()
        else:
            self.draw_page(page_name)


    def handle_button_click(self, button):
        if self.current_page == "main_menu":
            if button.text == 'Settings':
                print("Start Game")
            elif button.text == 'Exit':
                pygame.quit()
                sys.exit()
            elif button.text == 'Person':
                print('person')
                self.current_page = "login_page"

        elif self.current_page == "login_page":
            if button.text == 'Exit':
                pygame.quit()
                sys.exit()
            elif button.text == 'Submit':
                self.username = self.text_boxes[0].text
                self.password = self.text_boxes[1].text
                print("Username:", self.username)
                print("Password:", self.password)

                if self.db.login_user(self.username, self.password):
                    print("Login successful!")
                    # Navigate to next page or perform further actions
                    self.current_page = "home_page"
                    self.run_home()
                else:
                    print("Login failed! Incorrect username or password.")

            elif button.text == 'Register':
                self.current_page = "register_page"
                self.run_register()

        elif self.current_page == "register_page":
            if button.text == 'Submit':
                username = self.text_boxes[0].text
                password = self.text_boxes[1].text
                if self.db.register_user(username, password):
                    print("Registration successful!")
                    self.current_page = "login_page"
                    self.run_login()
                else:
                    print("Registration failed! Username already exists.")

            elif button.text == 'Exit':
                pygame.quit()
                sys.exit()

    def run_login(self):
      self.reset_page()
      login_page_buttons = [
        Button('Submit', (150, 490), (350, 50)),
        Button('Register', (150, 570), (200, 50)),
        Button('Exit', (1000 , 550), (5,5))
    ]


      self.add_button(login_page_buttons[0])
      self.add_button(login_page_buttons[1])
      self.add_button(login_page_buttons[2])

      self.add_text_box(TextBox(290, 327, 300, 40))
      self.add_text_box(TextBox(290, 405, 300, 40))
      
    

      while self.current_page == "login_page":
        self.draw_page_with_transition('Login Page')

       

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(event.pos):
                        self.handle_button_click(button)
                for textbox in self.text_boxes:
                    textbox.handle_event(event)
                    if textbox.rect.collidepoint(pygame.mouse.get_pos()):
                        for other_textbox in self.text_boxes:
                            if other_textbox != textbox:
                                other_textbox.active = False
                        textbox.active = True
                    else:
                        textbox.active = False
                    textbox.color = (255, 255, 255) if textbox.active else (200, 200, 200)
            elif event.type == pygame.KEYDOWN:
                for textbox in self.text_boxes:
                    if textbox.active:
                        textbox.handle_event(event)

        pygame.display.flip()
        
    def run_register(self):
        self.reset_page()
        register_page_buttons = [
            Button('Submit', (150, 490), (350, 50)),
            Button('Back Page ', (150, 570), (200, 50)),
        
        ]
        
        self.add_button(register_page_buttons[0])
        self.add_button(register_page_buttons[1])

        self.add_text_box(TextBox(290, 327, 300, 40))
        self.add_text_box(TextBox(290, 405, 300, 40))
       

        name_textbox = TextBox(390, 327, 300, 40)
        password_textbox = TextBox(290, 405, 300, 40)

        self.add_text_box(name_textbox)
        self.add_text_box(password_textbox)

        while self.current_page == "register_page":
            self.draw_page_with_transition('Register Page')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.is_clicked(event.pos):
                            self.handle_button_click(button)
                    for textbox in self.text_boxes:
                        textbox.handle_event(event)
                        if textbox.rect.collidepoint(pygame.mouse.get_pos()):
                            for other_textbox in self.text_boxes:
                                if other_textbox != textbox:
                                    other_textbox.active = False
                            textbox.active = True
                        else:
                            textbox.active = False
                        textbox.color = (255, 255, 255) if textbox.active else (200, 200, 200)
                elif event.type == pygame.KEYDOWN:
                    for textbox in self.text_boxes:
                        if textbox.active:
                            textbox.handle_event(event)

            pygame.display.flip()
    
    def run_home(self):
     self.reset_page()
     """
     Home_buttons = [
        Button_Image(50, 150, self.img, 0.8),
        Button_Image(50, 250, self.img, 0.8),
        Button_Image(50, 350, self.img, 0.8),
        Button_Image(50, 450, self.img, 0.8),
        Button_Image(50, 550, self.img, 0.8)
    ]

     self.add_button_img(Home_buttons[0])
     self.add_button_img(Home_buttons[1])
     self.add_button_img(Home_buttons[2])
     self.add_button_img(Home_buttons[3])
     self.add_button_img(Home_buttons[4])
     """
     self.reset_page()
     home_page_buttons = [
        Button('Play', (175, 130), (170, 50)),
        Button('Load Game ', (175, 270), (170, 50)),
        Button('Load', (175 , 410), (170,50)),
        Button('Help', (175 , 550), (170,50)),
        
    ]


     self.add_button( home_page_buttons[0])
     self.add_button( home_page_buttons[1])
     self.add_button( home_page_buttons[2])
     self.add_button( home_page_buttons[3])
     
     while self.current_page == "home_page":
        self.draw_page('Home Page')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.is_clicked(event.pos):
                        self.handle_button_click(button)
        pygame.display.flip()

    def run(self):
        main_menu_buttons = [
            Button('Person', (535, 390), (300, 50)),
            Button('Settings', (535, 510), (300, 50)),
            Button('Exit', (535, 621), (300, 50))
        ]

        for button in main_menu_buttons:
            self.add_button(button)

        while True:
            if self.current_page == "main_menu":
                 self.draw_page_with_transition('Main Menu')
            elif self.current_page == "login_page":
                self.run_login()
            elif self.current_page == "register_page":
                self.run_register()
            elif self.current_page == "home_page":
                self.run_home()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.is_clicked(event.pos):
                            self.handle_button_click(button)

            pygame.display.flip()

if __name__ == "__main__":
    pygame.init()  # Khởi tạo pygame
    game = Game()  # Khởi tạo trò chơi
    game.run()     # Chạy trò chơi