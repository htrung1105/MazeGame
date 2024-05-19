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

    def __init__(self, x: int, y: int):
        '''
        :param x, y: chỉ số của ô trong ma trận

        vis_dir: hướng đi của gợi ý
        walls: các bức tường bao quanh ô
        '''
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.vis_dir = {'top': False, 'right': False, 'bottom': False, 'left': False}

    # trả về tọa độ của các ô kề cạnh không bị ngăn cách bởi tường
    def neighbor(self):
        neibor = []
        walls = ['top', 'right', 'bottom', 'left']
        dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        for wall, (dx, dy) in zip(walls, dir):
            if self.walls[wall] == False:
                neibor.append((self.x + dx, self.y + dy))
        return neibor

# tạo class cho một mê cung
class Maze:
    '''
    class gồm các hàm:
    def breakWall(self, x: int , y: int, dx: int, dy: int): phá tường theo hướng (dx, dy)
    def mazeGenerate(self): Sinh một mê cung
    def makeHint(self): tạo gợi ý đường đi bằng BFS cho toàn bộ ô trong mê cung
    def hint(self, x: int, y: int) -> list[tuple]: trả về đường đi gợi ý cho người chơi hướng đến điểm kết thúc đến khi gặp ngã ba
    '''

    def __init__(self, size: int, startX: int, startY: int, endX: int, endY: int):
        '''
        :param size: kích thước của mê cung
        :param startX, startY: tọa độ ô bắt đầu
        :param endX, endY: tọa độ ô kết thúc

        grid: ma trận của mê cung
        trace: tọa độ của ô trước đó đã đi vào ô (x, y)
        hint: gợi ý ô tiếp theo hướng đến điểm kết thúc
        '''
        self.size = size
        self.startX, self.startY = startX, startY
        self.endX, self.endY = endX, endY

        self.grid = [[Cell(x, y) for y in range(size)] for x in range(size)]

        self.trace = [[(0, 0)] * size for _ in range(size)]
        self.hint = [[(0, 0)] * size for _ in range(size)]

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

    def convert(self) -> list[list[str]]:
        grid = [['x'] * (self.size * 2 + 1) for _ in range(self.size * 2 + 1)]

        for i in range(0, self.size):
            for j in range(0, self.size):
                x = 1 + i * 2
                y = 1 + j * 2
                grid[x][y] = ' '
                walls = ['top', 'right', 'bottom', 'left']
                dir = [(-1, 0), (0, 1), (1, 0), (0, -1)]
                for wall, (dx, dy) in zip(walls, dir):
                    if self.grid[i][j].walls[wall] == True:
                        grid[x + dx][y + dy] = 'x'
                    else:
                        grid[x + dx][y + dy] = ' '
        grid[1 + self.startX * 2][1 + self.startY * 2] = 'p'
        grid[1 + self.endX * 2][1 + self.endY * 2] = 'e'

        return grid