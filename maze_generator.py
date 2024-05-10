import random

# tạo class cho một ô
class Cell:
    def __init__(self, x: int, y: int):
        '''
        x, y: tọa độ của ô
        visited: ô đã được thăm hay chưa
        walls: các bức tường bao quanh ô
        '''
        self.x = x
        self.y = y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
    
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
    def __init__(self, size: int, startX: int, startY: int, endX: int, endY: int):
        '''
        size: kích thước của mê cung
        startX, startY: tọa độ ô bắt đầu
        endX, endY: tọa độ ô kết thúc
        grid: ma trận của mê cung
        trace: tọa độ của ô trước đó đã đi vào ô (x, y)
        '''
        self.size = size
        self.startX, self.startY = startX, startY
        self.endX, self.endY = endX, endY
        self.grid = [[Cell(x, y) for y in range(size)] for x in range(size)]
        self.trace = [[(0, 0)] * size for _ in range(size)]
    
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