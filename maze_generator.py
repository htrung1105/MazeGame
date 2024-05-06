'''
file này gồm các class:
class Cell: Một ô của mê cung
class Maze: Mê cung
'''
import random
from queue import Queue

# tạo class cho một ô
class Cell:
    '''
    các hàm của class:
    def neighbor(self): trả về tọa độ của các ô kể cạnh không bị ngăn cách bởi tường
    '''
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
    '''
    class gồm các hàm:
    def breakWall(self, x: int , y: int, dx: int, dy: int): phá tường theo hướng (dx, dy)
    def mazeGenerate(self): Sinh một mê cung
    def makeHint(self): tạo gợi ý đường đi bằng BFS cho toàn bộ ô trong mê cung
    def hint(self, x: int, y: int) -> list[tuple]: trả về đường đi gợi ý cho người chơi hướng đến điểm kết thúc đến khi gặp ngã ba
    '''
    def __init__(self, size: int, startX: int, startY: int, endX: int, endY: int):
        '''
        size: kích thước của mê cung
        startX, startY: tọa độ ô bắt đầu
        endX, endY: tọa độ ô kết thúc
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

    # trả về đường đi gợi ý cho người chơi hướng đến điểm kết thúc đến khi gặp ngã 3
    def hint(self, x: int, y: int) -> list[tuple]:
        startNode = (self.startX, self.startY)
        
        hintPath = []
        while True:
            if (x, y) == startNode:
                break
            x, y = self.hint[x][y]
            hintPath.append(x, y)
            if list(self.grid[x][y].walls.values()).count(False) != 1:
                break
        return hintPath

    # tạo gợi ý đường đi bằng BFS cho toàn bộ ô trong mê cung
    def makeHint(self):
        # lấy các thông số của mê cung
        maze = self.maze
        endX = self.maze.endX
        endY = self.maze.endY

        # khởi tạo các biến
        visited = [[False] * maze.size for _ in range(maze.size)]
        q = Queue()

        visited[endX][endY] = True
        q.put((endX, endY))

        # BFS
        while q:
            x, y = q.get()
            for nx, ny in maze.grid[x][y].neighbors():
                if visited[nx][ny] == False:
                    visited[nx][ny] = True
                    maze.hint[nx][ny] = (x, y)
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
                    visited[nx][ny]= True
                    self.breakWall(x, y, dx, dy)
                    stack.append((nx, ny))
                    break
            if deadEnd == 1:
                stack.pop()
        
        # Sau khi sinh xong mê cung thì tạo gợi ý
        self.makeHint()