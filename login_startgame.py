import time
import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
from database import UserDatabase

from typing import Tuple, Optional
pygame.init()

# Constants and global variables
WINDOW_SIZE = (1300, 750)

# -------------------------------------------------------
# Hướng dẫn sử dụng
# Bắt đầu trò chơi:
#   g = LoginMenu()
#   g.start()
# Khi từ game -> main menu, khởi tạo 
#   g = MenuGame(username, password)
#   g.start()
# -------------------------------------------------------

class LoginMenu():
    def __init__(self):
        self.running_menu = True
        self.surface = create_example_window('Maze Game', WINDOW_SIZE)
        self.main_menu = pygame_menu.Menu(
            overflow=(False, False),
            height=WINDOW_SIZE[1],  # * 0.7,
            onclose=pygame_menu.events.EXIT,  # User press ESC button
            title='Main menu',
            width=WINDOW_SIZE[0]  # * 0.8
        )

    def check_login(self):
        data = self.login_menu.get_input_data()
        for k in data.keys():
            print(f'\t{k}\t=>\t{data[k]}')

        DB = UserDatabase()
        if not DB.login_user(username = data['username'], password = data['password']):
            self.login_noti.set_title('Wrong username or password')
            print('wrongggggg')
        else:
            self.login_noti.set_title('Login DONE!')
            self.login_menu.force_surface_update()
            print('login successful')
            pygame.time.delay(300)
            self.running_menu = False
            g = MenuGame(data['username'], data['password'])
            g.start()

    def check_register(self):
        data = self.register_menu.get_input_data()
        for k in data.keys():
            print(f'\t{k}\t=>\t{data[k]}')

        DB = UserDatabase()
        if DB.register_user(username = data['username'], password = data['password']):
            self.regis_noti.set_title('Register DONE!')
            print('register OK!')
            pygame.time.delay(1500)
        else:
            print('not register ok')
            self.regis_noti.set_title('Register AGAIN!')

    def reset_noti_regis(self, a):
        self.regis_noti.set_title('Register now')

    def reset_noti_login(self, a):
        self.login_noti.set_title('User Login')
            
    def init_theme(self):
        b_img = pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path='assets/background.png',
            image_id='background')
       
        login_img = pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path='assets/login.png',
            image_id='background')
            
        register_img = pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path='assets/register.png',
            image_id='background')

        my_theme = pygame_menu.themes.Theme(
            background_color = b_img, 
            border_color = (0, 255, 0),
            border_width = 15,
            #cursor_color = (15, 15, 15),
            #focus_background_color = None,                          

            title = True,                                                 # có hay không title
            title_background_color = (249,72,82),                         # màu nền của title
            title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE, # style title bar
            title_close_button = True,                                    # nút thoát // quay lại
            title_close_button_background_color = (10, 10, 10),           # màu nút thoát // quay lại
            title_font = pygame_menu.font.FONT_COMIC_NEUE,                # font title
            title_font_antialias = True,                                  # khử răng cưa title font
            title_font_color = (255, 255, 255),                           # màu title
            title_font_shadow = True,                                     # bóng chữ title
            title_font_shadow_color = (0, 0, 0),                          # màu bóng chữ title

            # effect khi chọn
            widget_selection_effect = pygame_menu.widgets.LeftArrowSelection(
                arrow_size=(10, 15), arrow_right_margin=10, arrow_vertical_offset=0, blink_ms=0),

            widget_font = pygame_menu.font.FONT_COMIC_NEUE,               # font widget
            widget_font_antialias = True,                                 # font widget, khử răng cưa
            widget_font_color = (0, 0, 0),                                # màu chữ chưa được chọn
            selection_color = (249,16,23),                                # màu chữ được chọn
            widget_background_color = (249,72,82, 0),                     # màu nền widget
            widget_font_size = 30,                                        # size font widget                              
            widget_offset = (0, 0),                                       # x-axis and y-axis (x, y) offset
            widget_margin = (0, 25),                                      # khoảng cách của các ô
            widget_alignment = pygame_menu.locals.ALIGN_CENTER,           # căn giữa
            
            widget_box_arrow_color = (34, 24, 142),                       # màu mũi tên chọn hộp
            widget_box_border_width = 2,                                  # độ dày viền hộp chọn
            widget_box_border_color = (0, 0, 0),                          # màu viền hộp chọn
            widget_box_margin = (10, 0),                                  # vị trí hộp chọn
            widget_box_background_color = (255, 255, 255)                 # màu hộp chọn
        )

        self.main_menu_theme = my_theme.copy()
        self.main_menu_theme.background_color = b_img
        self.main_menu_theme.widget_offset = (0.01, 0.505) # need for main menu
        self.main_menu_theme.title_close_button = False
        self.main_menu_theme.selection_color=(249,16,23)

        self.login_menu_theme = my_theme.copy()
        self.login_menu_theme.background_color = login_img
        self.login_menu_theme.widget_offset = (0.38, 0.22)  
        self.login_menu_theme.title_close_button = True
        self.login_menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT

        
        self.register_menu_theme = my_theme.copy()
        self.register_menu_theme.background_color = register_img
        self.register_menu_theme.widget_offset = (0.38, 0.22)  
        self.register_menu_theme.title_close_button = True
        self.register_menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT

    def init_login_menu(self):
        self.login_menu = pygame_menu.Menu(
            overflow=(False, False),
            height=WINDOW_SIZE[1],  # * 0.7,
            onclose=pygame_menu.events.EXIT,  # User press ESC button
            theme=self.login_menu_theme,
            title='Login',
            width=WINDOW_SIZE[0],  # * 0.8
        )

        self.login_noti = self.login_menu.add.label('User Login')
        usern_login = self.login_menu.add.text_input(
            title='                     ',
            maxchar=10,
            textinput_id='username',
            input_underline = '__',
            # input_underline_vmargin = 3,
            onchange = self.reset_noti_login)
        passw_login = self.login_menu.add.text_input(
            title='                     ',
            maxchar=10,
            textinput_id='password',
            input_underline = '__',
            # input_underline_vmargin = 1,
            password=False,
            onchange = self.reset_noti_login)
        self.login_menu.add.button('                            Login', self.check_login)
        self.login_menu.add.button('Return to main menu', pygame_menu.events.BACK)

    def init_register_menu(self):
        self.register_menu = pygame_menu.Menu(
            overflow=(False, False),
            height=WINDOW_SIZE[1],  # * 0.7,
            onclose=pygame_menu.events.EXIT,  # User press ESC button
            theme=self.register_menu_theme,
            title='Register',
            width=WINDOW_SIZE[0]  # * 0.8
        )

        self.regis_noti = self.register_menu.add.label('Register now')
        usern_regis = self.register_menu.add.text_input(
            title='                     ',
            maxchar=10,
            textinput_id='username',
            onchange = self.reset_noti_regis)
        passw_regis = self.register_menu.add.text_input(
            title='                     ',
            maxchar=10,
            textinput_id='password',
            password=False,
            onchange = self.reset_noti_regis)
        self.register_menu.add.button('                          Register', self.check_register)
        self.register_menu.add.button('Return to main menu', pygame_menu.events.BACK)

    def init_main_menu(self):
         self.main_menu = pygame_menu.Menu(
            overflow=(False, False),
            height=WINDOW_SIZE[1],  # * 0.7,
            onclose=pygame_menu.events.EXIT,  # User press ESC button
            theme=self.main_menu_theme,
            title='Main menu',
            width=WINDOW_SIZE[0]  # * 0.8
         )

         Login_button = self.main_menu.add.button('Login', self.login_menu)
        
         Register_button = self.main_menu.add.button('Register', self.register_menu)
        
         Quit_button = self.main_menu.add.button('Quit', pygame_menu.events.EXIT)

    def init_menu(self):
        self.init_login_menu()
        self.init_register_menu()
        self.init_main_menu()

    def start(self):
        self.init_theme()
        self.init_menu()

        self.running_menu = True
        while self.running_menu:

            # Main menu
            self.main_menu.mainloop(self.surface)

            # Flip surface
            pygame.display.flip()

class MenuGame():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.running_menu = True

        self.sound = pygame_menu.sound.Sound()
        self.sound.load_example_sounds()
        self.sound.set_sound(pygame_menu.sound.SOUND_TYPE_ERROR, None)

        self.surface = create_example_window('Main Menu', WINDOW_SIZE)
        self.main_menu = pygame_menu.Menu(
            overflow = (False, False),
            height=WINDOW_SIZE[1] ,#* 0.7,
            onclose=pygame_menu.events.EXIT,  # User press ESC button
            title='Main menu',
            width=WINDOW_SIZE[0] #* 0.8
        )

    def update_menu_sound(self, value: Tuple, enabled: bool) -> None:
        """
        Update menu sound.

        :param value: Value of the selector (Label and index)
        :param enabled: Parameter of the selector, (True/False)
        """
        assert isinstance(value, tuple)
        if enabled:
            main_menu.set_sound(sound, recursive=True)
            print('Menu sounds were enabled')
        else:
            main_menu.set_sound(None, recursive=True)
            print('Menu sounds were disabled')

    def return_to_login(self):
        self.running_menu = False
        g = LoginMenu()
        g.start()

    def get_data_leaderboard(self, level_to_return):
        DB = UserDatabase()
        data = DB.leaderboard()
        level_easy = []
        level_medium = []
        level_hard = []
        for level in data:
            for player in level:
                if player['level'] == 'easy':
                    level_easy.append(player['username'])
                    level_easy.append(player['time'])
                elif player['level'] == 'medium':
                    level_medium.append(player['username'])
                    level_medium.append(player['time'])
                elif player['level'] == 'hard':
                    level_hard.append(player['username'])
                    level_hard.append(player['time'])
        print(level_easy, level_medium, level_hard)
        if level_to_return == 'easy':
            return level_easy
        elif level_to_return == 'medium':
            return level_medium
        elif level_to_return == 'hard':
            return level_hard
        else:
            return None

    def start_a_saved_game(self):
        game = self.saved_games.get_index()
        data = self.saved_games.get_widgets()
        data = data[game].get_title()
        print(data)
        game_name = ''
        for i in range(len(data) - 1):
            if data[i:i + 2] == ': ':
                game_name = data[i + 2:]
                break
        print(game_name)
        return (self.username, self.password, game_name) ## START A SAVED GAME

    def init_theme(self):
        background_img = pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path = 'assets/nbackground.png',
            image_id = 'background')
        nbackground_img = pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path = 'assets/Home.png',
            image_id = 'nbackground')
        startgame_img = pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path = 'assets/start.png',
            image_id = 'nbackground')
        Setting_img = pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path = 'assets/Setting.png',
            image_id = 'nbackground')
        Leaderboard_img=pygame_menu.baseimage.BaseImage(
            drawing_mode=101,
            image_path = 'assets/leaderboard.png',
            image_id = 'nbackground')
              
        my_theme = pygame_menu.themes.Theme(
            background_color = background_img, 
            border_color = (0, 255, 0),
            border_width = 15,
            #cursor_color = (15, 15, 15),
            #focus_background_color = None,                          

            title = True,                                                 # có hay không title
            title_background_color = (249,72,82),                         # màu nền của title
            title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE, # style title bar
            title_close_button = True,                                    # nút thoát // quay lại
            title_close_button_background_color = (10, 10, 10),           # màu nút thoát // quay lại
            title_font = pygame_menu.font.FONT_COMIC_NEUE,                # font title
            title_font_antialias = True,                                  # khử răng cưa title font
            title_font_color = (255, 255, 255),                           # màu title
            title_font_shadow = True,                                     # bóng chữ title
            title_font_shadow_color = (0, 0, 0),                          # màu bóng chữ title

            # effect khi chọn
            widget_selection_effect = pygame_menu.widgets.LeftArrowSelection(
                arrow_size=(10, 15), arrow_right_margin=10, arrow_vertical_offset=0, blink_ms=0),

            widget_font = pygame_menu.font.FONT_COMIC_NEUE,               # font widget
            widget_font_antialias = True,                                 # font widget, khử răng cưa
            widget_font_color = (0, 0, 0),                                # màu chữ chưa được chọn
            selection_color = (255, 255, 255),                            # màu chữ được chọn
            widget_background_color = (249,72,82, 0),                     # màu nền widget
            widget_font_size = 30,                                        # size font widget                              
            widget_offset = (0, 0),                                       # x-axis and y-axis (x, y) offset
            widget_margin = (0, 25),                                      # khoảng cách của các ô
            widget_alignment = pygame_menu.locals.ALIGN_CENTER,           # căn giữa
            
            widget_box_arrow_color = (34, 24, 142),                       # màu mũi tên chọn hộp
            widget_box_border_width = 2,                                  # độ dày viền hộp chọn
            widget_box_border_color = (0, 0, 0),                          # màu viền hộp chọn
            widget_box_margin = (10, 0),                                  # vị trí hộp chọn
            widget_box_background_color = (255, 255, 255)                 # màu hộp chọn
            )

        self.my_main_menu_theme = my_theme.copy()
        self.my_main_menu_theme.background_color = nbackground_img
        #self.my_main_menu_theme # need for main menu
        self.my_main_menu_theme.title_close_button = False
        self.my_main_menu_theme.widget_margin = (-380, 10)
        self.my_main_menu_theme.widget_offset = (0, 50)
        self.my_main_menu_theme.selection_color=(249,16,23)

        self.my_start_game_theme = my_theme.copy()
        self.my_start_game_theme.background_color= startgame_img
        self.my_start_game_theme.widget_font_size = 25
        self.my_start_game_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT
        self.my_start_game_theme.widget_offset = (70, 210)
        self.my_start_game_theme.widget_margin = (-60, 25)
        self.my_start_game_theme.widget_font_color = (0, 0, 0),                        # màu chữ chưa được chọn
        self.my_start_game_theme.selection_color = (247, 12, 12),                            # màu chữ được chọn
        self.my_start_game_theme.widget_box_background_color = (0, 0, 0, 0) 
        #my_start_game_theme.widget_margin = (0, 0)
        
        self.my_load_game_theme = my_theme.copy()
        self.my_load_game_theme.widget_font_size = 25
        self.my_load_game_theme.widget_font_color = (0, 0, 0),
        self.my_load_game_theme.selection_color = (247, 12, 12),

        self.leaderboard_theme = my_theme.copy()
        self.leaderboard_theme.background_color=Leaderboard_img
        self.leaderboard_theme.widget_font_size = 25
        self.leaderboard_theme.widget_font_color = (0, 0, 0),
        self.leaderboard_theme.selection_color = (247, 12, 12),

        self.my_settings_menu_theme = my_theme.copy()
        self.my_settings_menu_theme.background_color=Setting_img 
        self.my_settings_menu_theme.widget_font_size = 20
        self.my_settings_menu_theme.widget_font_color = (0, 0, 0),
        self.my_settings_menu_theme.selection_color = (247, 12, 12),                            # màu chữ được chọn
        self.my_settings_menu_theme.selection_color = (247, 12, 12),
        self.my_settings_menu_theme.widget_box_background_color = (0, 0, 0)
        self.my_settings_menu_theme.widget_offset = (125, 0)
        self.my_settings_menu_theme.widget_margin = (-180, 25)
        self.my_settings_menu_theme.widget_alignment = pygame_menu.locals.ALIGN_LEFT

    def init_start_game(self):
        self.start_game_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1], #* 0.85,
        theme=self.my_start_game_theme,
        title='Start Game',
        width=WINDOW_SIZE[0], #* 0.6
        overflow = (False, False),
        #columns= 2,
        #rows = [5, 6],
        )
        items_levels = [('Easy (20x20)', '20'),
             ('Medium (40x40)', '40'),
             ('Hard (100x100)', '100')]

        def data_fun_sgm() -> None:
            """
            Print data of the menu.
            """
            print('Start game data:')
            data = self.start_game_menu.get_input_data()
            for k in data.keys():
                print(f'\t{k}\t=>\t{data[k]}')
            level = int(data['level'][0][1])
            locations = [data['start_x'], data['start_y'], data['end_x'], data['end_y']]
            next_step = True
            for location in locations:
                if location < 0 or location > level:
                    #randomm_noti.show()
                    #randomm.hide()
                    randomm.set_title('Choose again!')
                    print('unvalid')
                    next_step = False
                    break
            if next_step:
                print('valid !! playgame now')
                self.running_menu = False

        # Add some buttons
        self.start_game_menu.add.selector(
            'Play mode',
            items=[('Play by yourself', 0),
                ('Auto play (A*)  ', 1),
                ('Auto play (BFS)', 2)],
            selector_id='mode_play',
            default=0,
            style='fancy'
        )
        size_map = self.start_game_menu.add.selector(
            'Level',
            items_levels,
            selector_id='level',
            default=1,
            style='fancy'
        )

        def show_location(a, b):
            if a[0][1]:
                randomm.set_title('Choose location!')
                randomm.show()
                tam_row.show()
                tam_col.show()
                giahuy_row.show()
                giahuy_col.show()
            else:
                randomm.hide() 
                tam_row.hide()
                tam_col.hide()
                giahuy_row.hide()
                giahuy_col.hide()

        location = self.start_game_menu.add.selector(
            title = 'Location',
            onchange = show_location,
            items=[('Random', 0),
                ('Selectable ', 1),],
            selector_id='location_mode',
            default=0,
            style='fancy'
        )

        # Add final buttons
        #start_game_menu.add.button('Reset game setting', start_game_menu.reset_value)
        self.start_game_menu.add.button('Start game', data_fun_sgm, button_id='store')  # Call function
        self.start_game_menu.add.button('Return to main menu', pygame_menu.events.BACK,) #align=pygame_menu.locals.ALIGN_CENTER)

        # Add choose location input
        randomm = self.start_game_menu.add.label('Choose location').hide()
        randomm.set_font(
            font = pygame_menu.font.FONT_COMIC_NEUE,
            font_size = 20,
            color = (247, 12, 12),
            readonly_color = (247, 12, 12),
            selected_color = (247, 12, 12),
            readonly_selected_color = (247, 12, 12),
            background_color = (0, 0, 0, 0))
        tam_row = self.start_game_menu.add.text_input(
            'Tam location (row): ',
            default=0,
            maxchar=3,
            maxwidth=3,
            textinput_id='start_x',
            input_type=pygame_menu.locals.INPUT_INT,
            cursor_selection_enable=False
        ).hide()
        tam_col = self.start_game_menu.add.text_input(
            'Tam location (col): ',
            default=0,
            maxchar=3,
            maxwidth=3,
            textinput_id='start_y',
            input_type=pygame_menu.locals.INPUT_INT,
            cursor_selection_enable=False
        ).hide()
        giahuy_row = self.start_game_menu.add.text_input(
            'Gia Huy location (row): ',
            default=40,
            maxchar=3,
            maxwidth=3,
            textinput_id='end_x',
            input_type=pygame_menu.locals.INPUT_INT,
            cursor_selection_enable=False
        ).hide()
        giahuy_col = self.start_game_menu.add.text_input(
            'Gia Huy location (col): ',
            default=40,
            maxchar=3,
            maxwidth=3,
            textinput_id='end_y',
            input_type=pygame_menu.locals.INPUT_INT,
            cursor_selection_enable=False
        ).hide()

        location_input = self.start_game_menu.add.frame_v(
            background_color=(0, 0, 0, 0),
            border_color=(0, 0, 0, 0),
            border_width=1,
            float=True,
            height=600,
            max_height=600,
            width=500
        )

        for j in [randomm, tam_row, tam_col, giahuy_row, giahuy_col]:
            location_input.pack(j)
        location_input.translate(400, -180)

    def init_load_game(self):
        DB = UserDatabase()
        data = DB.load_users(self.username, self.password)
        games = []
        for game in data:
            if game != 'password':
                games.append(game)

        self.saved_games = pygame_menu.Menu(
            columns=1,
            height=WINDOW_SIZE[1], #* 0.45,
            theme=self.my_load_game_theme,
            column_max_width = 500,
            title='Load Game',
            width=WINDOW_SIZE[0], #* 0.9
        )
        f = self.saved_games.add.frame_v(
            background_color='#d2d3f7',
            border_color='#36372f',
            border_width=1,
            float=True,
            height=max(len(games) * 40, 250),
            max_height=250,
            width=400
        )
        labels = [self.saved_games.add.button(f'Game {i + 1}: {games[i]}', self.start_a_saved_game,) for i in range(len(games))]
        for j in labels:
            f.pack(j)
        f.translate(130, -45)
        '''
        for i in range(len(games)):
            self.saved_games.add.button(
                f'Game {i + 1}: {games[i]}',
                self.start_a_saved_game,
            )   ## START A SAVED GAME
        '''
        button = self.saved_games.add.button('Return to main menu', pygame_menu.events.BACK,).background_inflate_to_selection_effect()
        button.translate(130, 220)

    def init_leaderboard(self):
        easy_list = self.get_data_leaderboard('easy')
        medium_list = self.get_data_leaderboard('medium')
        hard_list = self.get_data_leaderboard('hard')

        self.leaderboard = pygame_menu.Menu(
            height=WINDOW_SIZE[1], #* 0.45,
            theme=self.leaderboard_theme,
            title='Leaderboard',
            columns = 3,
            rows = [len(easy_list)//2 + 1, len(medium_list)//2 + 1, len(hard_list)//2 + 2],
            width=WINDOW_SIZE[0], #* 0.9
            )

        easy_labels = [self.leaderboard.add.label(easy_list[i] + ' : ' + str(easy_list[i + 1]) + 's') for i in range(0, len(easy_list), 2)]
        medium_labels = [self.leaderboard.add.label(medium_list[i] + ' : ' + str(medium_list[i + 1]) + 's') for i in range(0, len(medium_list), 2)]
        hard_labels = [self.leaderboard.add.label(hard_list[i] + ' : ' + str(hard_list[i + 1]) + 's') for i in range(0, len(hard_list), 2)]

        easy = self.leaderboard.add.frame_v(
            background_color=(0, 0, 0, 0),   #'#d2d3f7',
            border_color=(0, 0, 0, 0),  #'#36372f',
            border_width=1,
            float=True,
            height=max(len(easy_labels) * 40 , 320),
            max_height=320,
            width=270
        )

        medium = self.leaderboard.add.frame_v(
            background_color=(0, 0, 0, 0),
            border_color=(0, 0, 0, 0),
            border_width=1,
            float=True,
            height=max(len(medium_labels) * 40 , 320),
            max_height=320,
            width=270
        )

        hard = self.leaderboard.add.frame_v(
            background_color=(0, 0, 0, 0),
            border_color=(0, 0, 0, 0),
            border_width=1,
            float=True,
            height=max(len(hard_labels) * 40 , 320),
            max_height=320,
            width=270
        )

        for j in easy_labels:
            easy.pack(j)
        easy.translate(-250, 0)

        for j in medium_labels:
            medium.pack(j)
        medium.translate(110, 0)

        for j in hard_labels:
            hard.pack(j)
        hard.translate(465, 0)
        
        button = self.leaderboard.add.button('Return to main menu', pygame_menu.events.BACK)
        button.translate(150, 435)

    def init_setting(self):
        self.settings_menu = pygame_menu.Menu(
        height=WINDOW_SIZE[1], #* 0.85,
        theme=self.my_settings_menu_theme,
        title='Settings',
        width=WINDOW_SIZE[0], #* 0.6
        columns = 2,
        rows = [6, 6]
        )

        # Selectable items
        items = [('Easy', 'EASY'),
                 ('Medium', 'MEDIUM'),
                 ('Hard', 'HARD')]

        self.settings_menu.add.selector(
            'Select difficulty fancy',
            items,
            selector_id='difficulty_fancy',
            default=1,
            style='fancy'
        )

        # Create switch
        self.settings_menu.add.toggle_switch('First Switch', False,
                                        toggleswitch_id='first_switch')
        self.settings_menu.add.toggle_switch('Other Switch', True,
                                        toggleswitch_id='second_switch',
                                        state_text=('Apagado', 'Encendido'))

        # Single value from range
        rslider = self.settings_menu.add.range_slider('Volume', 50, (0, 100), 1,
                                                 rangeslider_id='volume',
                                                 value_format=lambda x: str(int(x)))
        rslider = self.settings_menu.add.range_slider('Sound effect', 50, (0, 100), 1,
                                                 rangeslider_id='soundeffect',
                                                 value_format=lambda x: str(int(x)))

        # Add a progress bar
        progress = self.settings_menu.add.progress_bar('Progress', default=rslider.get_value(), progressbar_id='progress')

        def on_change_slider(val: int) -> None:
            """
            Updates the progress bar.

            :param val: Value of the progress from 0 to 100
            """
            progress.set_value(val)

        rslider.set_onchange(on_change_slider)

        # Add a block
        self.settings_menu.add.clock(clock_format='%Y/%m/%d %H:%M', title_format='Clock: {0}')

        def data_fun() -> None:
            """
            Print data of the menu.
            """
            print('Settings data:')
            data = settings_menu.get_input_data()
            for k in data.keys():
                print(f'\t{k}\t=>\t{data[k]}')

        # Add final buttons
        self.settings_menu.add.selector(
            'Menu sounds ',
            [('Off', False), ('On', True)],
            onchange=self.update_menu_sound,
            style='fancy'
                               )
        self.settings_menu.add.button('Store data', data_fun, button_id='store')  # Call function
        self.settings_menu.add.button('Restore original values', self.settings_menu.reset_value)
        self.settings_menu.add.button('Return to main menu', pygame_menu.events.BACK,
                                 align=pygame_menu.locals.ALIGN_CENTER)

    def init_main_menu(self):
        self.main_menu = pygame_menu.Menu(
        overflow = (False, False),
        height=WINDOW_SIZE[1] ,#* 0.7,
        onclose=pygame_menu.events.EXIT,  # User press ESC button
        theme=self.my_main_menu_theme,
        title='Main menu',
        position = (20, 20),
        width=WINDOW_SIZE[0] #* 0.8
        )

        self.main_menu.add.button('Start game', self.start_game_menu)
        self.main_menu.add.vertical_margin(85)
        self.main_menu.add.button('Load game', self.saved_games)
        self.main_menu.add.vertical_margin(85)
        self.main_menu.add.button('Leaderboard', self.leaderboard)
        self.main_menu.add.vertical_margin(75)
        self.main_menu.add.button('Settings', self.settings_menu)
        self.main_menu.add.vertical_margin(75)
        self.main_menu.add.button('Log out', self.return_to_login)  
    
    def init_menu(self):
        self.init_start_game()
        self.init_load_game()
        self.init_leaderboard()
        self.init_setting()
        self.init_main_menu()

    def start(self):
        self.init_theme()
        self.init_menu()

        self.running_menu = True
        while self.running_menu:
            
            # Main menu
            self.main_menu.mainloop(self.surface)
            
            # Flip surface
            pygame.display.flip()


if __name__ == '__main__':
    g = LoginMenu()
    g.start()
