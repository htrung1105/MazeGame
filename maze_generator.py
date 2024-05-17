'''
file này gồm các class:
class Cell: Một ô của mê cung
class Maze: Mê cung
'''
import random
from queue import Queue
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

    def __init__(self, x: int, y: int, top_left_x: int, top_left_y: int, cell_size=15, wall_thickness=2, dir_thickness=3, wall_color=BLACK, dir_color=GREEN):
        '''
        :param x, y: chỉ số của ô trong ma trận
        :param cell_size: kích thước của 1 ô Cell  (số lẻ)
        :param wall_thickness: độ dày của tường
        :param dir_thickness: độ dày line gợi ý    (số lẻ)
        :param wall_color: màu của tường
        :param dir_color: màu của line gợi ý

        vis_dir: hướng đi của gợi ý
        walls: các bức tường bao quanh ô
        '''
        self.x, self.y = x, y
        self.cell_size = cell_size
        self.wall_thickness = wall_thickness
        self.dir_thickness = dir_thickness
        self.wall_color = wall_color
        self.dir_color = dir_color

        self.top_left_x = top_left_x
        self.top_left_y = top_left_y
        self.topleft = (self.top_left_x, self.top_left_y)

        self.center_x = top_left_x + cell_size / 2
        self.center_y = top_left_y + cell_size / 2
        self.center = (self.center_x, self.center_y)

        self.bottom_right_x = top_left_x + cell_size - 1
        self.bottom_right_y = top_left_y + cell_size - 1
        self.bottomright = (self.bottom_right_x, self.bottom_right_y)

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

    def render(self, screen):
        '''
        screen: màn hình xuất ảnh
        maze: thông tin mê cung
        '''
        if self.walls['top']:
            pygame.draw.rect(screen, self.wall_color, (self.top_left_x, self.top_left_y, self.cell_size, self.wall_thickness))
        if self.walls['bottom']:
            pygame.draw.rect(screen, self.wall_color, (self.top_left_x, self.bottom_right_y - self.wall_thickness + 1, self.cell_size, self.wall_thickness))
        if self.walls['left']:
            pygame.draw.rect(screen, self.wall_color, (self.top_left_x, self.top_left_y, self.wall_thickness, self.cell_size))
        if self.walls['right']:
            pygame.draw.rect(screen, self.wall_color, (self.bottom_right_x - self.wall_thickness + 1, self.top_left_y, self.wall_thickness, self.cell_size))

        if self.vis_dir['top']:
            pygame.draw.rect(screen, self.dir_color,
                             (self.center_x - self.dir_thickness / 2, self.top_left_y, self.dir_thickness, self.cell_size / 2))
        if self.vis_dir['bottom']:
            pygame.draw.rect(screen, self.dir_color,
                             (self.center_x - self.dir_thickness / 2, self.center_y, self.dir_thickness, self.cell_size / 2))
        if self.vis_dir['left']:
            pygame.draw.rect(screen, self.dir_color,
                             (self.top_left_x, self.center_y - self.dir_thickness / 2, self.cell_size / 2, self.dir_thickness))
        if self.vis_dir['right']:
            pygame.draw.rect(screen, self.dir_color,
                             (self.center_x, self.center_y - self.dir_thickness / 2, self.cell_size / 2, self.dir_thickness))

# tạo class cho một mê cung
class Maze:
    '''
    class gồm các hàm:
    def breakWall(self, x: int , y: int, dx: int, dy: int): phá tường theo hướng (dx, dy)
    def mazeGenerate(self): Sinh một mê cung
    def update_pos_now(self, x, y): cập nhật vị trí hiện tại là (x, y)
    def render(self, screen, pos_x, pos_y, x, y, len): Sinh display (góc trái trên là pos_x, pos_y) là ma trận có chỉ số [x -> x + len][y -> y + len]
    def makeHint(self): tạo gợi ý đường đi bằng BFS cho toàn bộ ô trong mê cung
    def hint(self, x: int, y: int) -> list[tuple]: trả về đường đi gợi ý cho người chơi hướng đến điểm kết thúc đến khi gặp ngã ba
    '''

    def __init__(self, size: int, startX: int, startY: int, endX: int, endY: int, cell_size: int,
                 wall_thickness=3, dir_thickness=3, wall_color=BLACK, dir_color=GREEN, maze_color=WHITE):
        '''
        :param size: kích thước của mê cung
        :param startX, startY: tọa độ ô bắt đầu
        :param endX, endY: tọa độ ô kết thúc
        :param cell_size: kích thước của 1 ô Cell  (recommend odd number)
        :param wall_thickness: độ dày của tường
        :param dir_thickness: độ dày line gợi ý
        :param wall_color: màu của tường
        :param dir_color: màu của line gợi ý
        :param maze_color: màu của ma trận

        width: kích thước của display
        grid: ma trận của mê cung
        trace: tọa độ của ô trước đó đã đi vào ô (x, y)
        image_character: ảnh nhân vật di chuyển
        display: màn hình xuất maze
        hint: gợi ý ô tiếp theo hướng đến điểm kết thúc
        '''
        self.size = size
        self.startX, self.startY = startX, startY
        self.endX, self.endY = endX, endY
        self.cell_size = cell_size
        self.wall_thickness, self.dir_thickness = wall_thickness, dir_thickness
        self.wall_color, self.dir_color, self.maze_color = wall_color, dir_color, maze_color

        self.grid = [[Cell(x, y,(cell_size - wall_thickness) * y, (cell_size - wall_thickness) * x, cell_size, wall_thickness, dir_thickness, wall_color, dir_color)
                      for y in range(size)] for x in range(size)]

        self.trace = [[(0, 0)] * size for _ in range(size)]
        self.hint = [[(0, 0)] * size for _ in range(size)]

        # Xây dựng display riêng cho maze
        width = cell_size * size - wall_thickness * (size - 1)
        self.display = pygame.Surface((width, width))
        self.display.fill(WHITE)

    # phá tường theo hướng (dx, dy)
    def breakWall(self, x: int, y: int, dx: int, dy: int):
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

    # trả về đường đi gợi ý cho người chơi hướng đến điểm kết thúc đến khi gặp ngã 3
    def hint(self, x: int, y: int) -> list[tuple]:
        startNode = (self.startX, self.startY)

        hintPath = []
        while True:
            if (x, y) == startNode:
                break
            x, y = self.hint[x][y]
            hintPath.append((x, y))
            if list(self.grid[x][y].walls.values()).count(False) != 1:
                break
        return hintPath

    # tạo gợi ý đường đi bằng BFS cho toàn bộ ô trong mê cung
    def makeHint(self):
        # khởi tạo các biến
        visited = [[False] * self.size for _ in range(self.size)]
        q = Queue()

        visited[self.endX][self.endY] = True
        q.put((self.endX, self.endY))

        # BFS
        while q:
            x, y = q.get()
            print(x, y)
            for nx, ny in self.grid[x][y].neighbor():
                if visited[nx][ny] is False:
                    visited[nx][ny] = True
                    self.hint[nx][ny] = (x, y)
                    q.put((nx, ny))

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
                    visited[nx][ny] = True
                    self.breakWall(x, y, dx, dy)
                    stack.append((nx, ny))
                    break
            if deadEnd == 1:
                stack.pop()
        # Sau khi sinh xong mê cung thì tạo gợi ý
        # self.makeHint()

    def get_pos(self, x: int, y: int):
        pos_x = self.cell_size / 2 + self.cell_size * x
        pos_y = self.cell_size / 2 + self.cell_size * y
        return (pos_x, pos_y)

    def render(self, screen, pos):
        '''
        :param pos_x: tọa độ x góc trái trên ma trận
        :param pos_y: tọa độ y góc trái trên của ma trận
        :param screen: màn hình xuất maze
        :return: None
        '''
        # Vẽ maze[x -> x + len][y -> y + len]
        for j in range(self.size):
            for i in range(self.size):
                self.grid[i][j].render(self.display)
        screen.blit(self.display, pos)
