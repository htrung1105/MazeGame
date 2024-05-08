'''
file này gồm các class:
class Cell: Một ô của mê cung
class Maze: Mê cung
'''
import random
import pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# tạo class cho một ô
class Cell:
    '''
    các hàm của class:
    def neighbor(self): trả về tọa độ của các ô kể cạnh không bị ngăn cách bởi tường
    def render(self, screen, center_x, center_y): trả về
    '''
    def __init__(self, x: int, y: int, cell_size = 15, wall_thickness = 2, dir_thickness = 3, wall_color = BLACK, dir_color = GREEN):
        '''
        :param x, y: chỉ số của ô trong ma trận
        :param cell_size: kích thước của 1 ô Cell  (số lẻ)
        :param wall_thickness: độ dày của tường
        :param dir_thickness: độ dày line gợi ý    (số lẻ)
        :param wall_color: màu của tường
        :param dir_color: màu của line gợi ý

        vis_dir: hướng đi của gợi ý
        walls: các bức tường bao quanh ô
        image: ảnh tại ô Cell
        '''
        self.x, self.y = x, y
        self.cell_size = cell_size
        self.wall_thickness = wall_thickness
        self.dir_thickness = dir_thickness
        self.wall_color = wall_color
        self.dir_color = dir_color

        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.vis_dir = {'top': False, 'right': False, 'bottom': False, 'left': False}
        self.image = None

    # trả về tọa độ của các ô kề cạnh không bị ngăn cách bởi tường
    def neighbor(self):
        neibor = []
        walls = ['top', 'right', 'bottom', 'left']
        dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for wall, (dx, dy) in zip(walls, dir):
            if self.walls[wall] == False:
                neibor.append((self.x + dx, self.y + dy))
        return neibor

    def render(self, screen, top_left_x, top_left_y):
        '''
        screen: màn hình xuất ảnh
        top_left_x, top_left_y: tọa độ trái-trên của ô Cell
        '''
        center_x = top_left_x + self.cell_size // 2
        center_y = top_left_y + self.cell_size // 2

        bottom_right_x = top_left_x + self.cell_size - 1
        bottom_right_y = top_left_y + self.cell_size - 1

        if self.walls['top']:
            pygame.draw.rect(screen, self.wall_color, (top_left_x, top_left_y, self.cell_size, self.wall_thickness))
        if self.walls['bottom']:
            pygame.draw.rect(screen, self.wall_color, (top_left_x, bottom_right_y - self.wall_thickness + 1, self.cell_size, self.wall_thickness))
        if self.walls['left']:
            pygame.draw.rect(screen, self.wall_color, (top_left_x, top_left_y, self.wall_thickness, self.cell_size))
        if self.walls['right']:
            pygame.draw.rect(screen, self.wall_color, (bottom_right_x - self.wall_thickness + 1, top_left_y, self.wall_thickness, self.cell_size))

        if self.vis_dir['top']:
            pygame.draw.rect(screen, self.dir_color, (center_x - self.dir_thickness // 2, top_left_y, self.dir_thickness, self.cell_size // 2 + 1))
        if self.vis_dir['bottom']:
            pygame.draw.rect(screen, self.dir_color, (center_x - self.dir_thickness // 2, center_y, self.dir_thickness, self.cell_size // 2 + 1))
        if self.vis_dir['left']:
            pygame.draw.rect(screen, self.dir_color, (top_left_x, center_y - self.dir_thickness // 2, self.cell_size // 2 + 1, self.dir_thickness))
        if self.vis_dir['right']:
            pygame.draw.rect(screen, self.dir_color, (center_x, center_y - self.dir_thickness // 2, self.cell_size // 2 + 1, self.dir_thickness))

        if self.image != None:
            screen.blit(self.image, self.image.get_rect(center = (center_x, center_y)))

SIZE_BORDER = 2 # Viền cạnh ngoài của maze
# tạo class cho một mê cung
class Maze:
    '''
    class gồm các hàm:
    def breakWall(self, x: int , y: int, dx: int, dy: int): phá tường theo hướng (dx, dy)
    def mazeGenerate(self): Sinh một mê cung
    def update_pos_now(self, x, y): cập nhật vị trí hiện tại là (x, y)
    def render(self, screen, pos_x, pos_y, x, y, len): Sinh display (góc trái trên là pos_x, pos_y) là ma trận có chỉ số [x -> x + len][y -> y + len]
    '''
    def __init__(self, size: int, startX: int, startY: int, endX: int, endY: int, cell_size: int, image_character = None, image_goal = None, scale = 1,
                 wall_thickness = 3, dir_thickness = 3, wall_color = BLACK, dir_color = GREEN, maze_color = WHITE):
        '''
        :param size: kích thước của mê cung
        :param startX, startY: tọa độ ô bắt đầu
        :param endX, endY: tọa độ ô kết thúc
        :param cell_size: kích thước của 1 ô Cell  (recommend odd number)
        :param image_character: ảnh nhân vật di chuyển
        :param image_goal: ảnh đích mê cung
        :param scale: tỉ lệ thu nhỏ của hình ảnh
        :param wall_thickness: độ dày của tường
        :param dir_thickness: độ dày line gợi ý
        :param wall_color: màu của tường
        :param dir_color: màu của line gợi ý
        :param maze_color: màu của ma trận

        nowX, nowY: tọa độ hiện tại của mê cung
        width: kích thước của display
        grid: ma trận của mê cung
        trace: tọa độ của ô trước đó đã đi vào ô (x, y)
        image_character: ảnh nhân vật di chuyển
        display: màn hình xuất maze
        '''
        self.size = size
        self.startX, self.startY = startX, startY
        self.endX, self.endY = endX, endY
        self.cell_size = cell_size
        self.scale = scale
        self.wall_thickness, self.dir_thickness = wall_thickness, dir_thickness
        self.wall_color, self.dir_color, self.maze_color = wall_color, dir_color, maze_color

        self.nowX, self.nowY = startX, startY
        self.grid = [[Cell(x, y, self.cell_size, wall_thickness, dir_thickness, wall_color, dir_color) for y in range(size)] for x in range(size)]
        self.trace = [[(0, 0)] * size for _ in range(size)]

        # Update ảnh cho Cell bắt đầu và kết thúc
        if image_character != None:
            self.grid[startX][startY].image = pygame.transform.smoothscale(image_character, (self.cell_size * scale, self.cell_size * scale))
        if image_goal != None:
            self.grid[endX][endY].image = pygame.transform.smoothscale(image_goal, (self.cell_size * scale, self.cell_size * scale))
        self.image_character = image_character

        # Xây dựng display riêng cho maze
        width = cell_size * size - wall_thickness * (size - 1)
        self.display = pygame.Surface((width, width))
        self.display.fill(WHITE)

    # phá tường theo hướng (dx, dy)
    def breakWall(self, x: int , y: int, dx: int, dy: int):
        nx, ny = x + dx, y + dy
        if dx == 1:
            self.grid[x][y].walls['bottom'] = False
            self.grid[nx][ny].walls['top'] = False
        if dx == -1:
            self.grid[x][y].walls['top'] = False
            self.grid[nx][ny].walls['bottom'] = False
        if dy == 1:
            self.grid[x][y].walls['right'] = False
            self.grid[nx][ny].walls['left'] = False
        if dy == -1:
            self.grid[x][y].walls['left'] = False
            self.grid[nx][ny].walls['right'] = False

    # Sinh ra một mê cung
    def mazeGenerate(self):
        # randomized DFS generator
        # sử dụng DFS khử đệ quy
        visited = [[False] * self.size for _ in range(self.size)]
        visited[0][0] = True
        stack = [(0, 0)]

        while stack:
            x, y = stack[-1]
            dir = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(dir)
            deadEnd = 1

            for dx, dy in dir:
                nx, ny = x + dx, y + dy
                if 0 <= nx and nx < self.size and 0 <= ny and ny < self.size and visited[nx][ny] == False:
                    deadEnd = 0
                    visited[nx][ny]= True
                    self.breakWall(x, y, dx, dy)
                    stack.append((nx, ny))
                    break
            if deadEnd == 1:
                stack.pop()

    def update_pos_now(self, x: int, y: int):
        self.grid[self.nowX][self.nowY].image = None
        self.grid[x][y].image = self.image_character
        self.nowX, self.nowY = x, y

    def render(self, screen, pos_x: int, pos_y: int, x = 0, y = 0, len = None):
        '''
        :param screen: màn hình xuất maze
        :param pos_x, pos_y: tọa độ góc trái - trên của ma trận
        :param x, y: chỉ số Cell góc trái - trên của ma trận
        :param len: độ dài ma trận vuông hiển thị
        :return: None
        '''
        if(len == None):
            len = self.size

        # Vẽ maze[x -> x + len][y -> y + len]
        for j in range(len):
            for i in range(len):
                self.grid[x + i][y + j].render(self.display, (self.cell_size - self.wall_thickness) * j, (self.cell_size - self.wall_thickness) * i)
        screen.blit(self.display, (pos_x, pos_y))


