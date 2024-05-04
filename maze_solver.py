import heapq
from maze_generator import *

# tạo class hàng đợi ưu tiên
class priority_queue:
    def __init__(self):
        self.heap = []

    def push(self, item):
        heapq.heappush(self.heap, item)

    def pop(self):
        return heapq.heappop(self.heap)

    def peek(self):
        return self.heap[0]

    def __len__(self):
        return len(self.heap)

# tạo class giải mê cung
class mazeSolver:
    def __init__(self, maze: Maze):
        '''
        vì self.maze là một view nên khi chạy thuật toán không được tác động lên 
        các thông số của maze ngoại trừ maze.trace
        '''
        self.maze = maze
    
    def AStarSearch(self):
        # lấy các thông số của mê cung để xử lý cho dễ
        maze = self.maze
        startX = self.maze.startX
        startY = self.maze.startY
        endX = self.maze.endX
        endY = self.maze.endY

        # hàm heuristic
        heuristic = lambda x, y: (x - endX) ** 2 + (y - endY) ** 2
        
        # khởi tạo các biến
        oo = float('inf')
        pq = priority_queue()
        g = [[oo] * maze.size for _ in range(maze.size)]
        f = [[oo] * maze.size for _ in range(maze.size)]
        
        g[startX][startY] = 0
        f[startX][startY] = heuristic(startX, startY)
        pq.push((f[startX][startY], startX, startY))

        # chạy thuật toán A*
        while pq:
            _, x, y = pq.pop()
            # ô (x, y) đã đươc thăm
            maze.grid[x][y].visited = True

            if (x, y) == (endX, endY):
                # tìm thấy đường đi
                break
            
            # duyệt qua các ô xung quanh
            for nx, ny in maze.grid[x][y].neighbor():
                # thêm một ô vào hàng đợi
                new_g = g[x][y] + 1
                new_f = new_g + heuristic(nx, ny)
                if new_f < f[nx][ny]:
                    maze.trace[nx][ny] = (x, y)
                    g[nx][ny] = new_g
                    f[nx][ny] = new_f
                    pq.push((new_f, nx, ny))
