import heapq
from maze_generator import *

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
    
class mazeSolver:
    def __init__(self, maze: Maze):
        self.maze = maze
    
    # trả về list gồm thứ tự các đường đi tìm được bao gồm cả điểm bắt đầu và kết thúc
    def tracePath(self):
        # lấy các thông số của mê cung để dễ xử lý
        maze = self.maze
        startX = self.maze.startX
        startY = self.maze.startY
        x = self.maze.endX
        y = self.maze.endY

        # truy ngược đường đi
        path = []
        while (x, y) != (startX, startY):
            path.append((x, y))
            x, y = maze.trace[x][y]
        path.append((x, y))
        path.reverse()
        return path

    # chạy thuật toán A* và trả về thứ tự thăm các ô
    def AStarSearch(self) -> list[tuple]:
        # lấy các thông số của mê cung để dễ xử lý
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

        visited = []
        while pq:
            _, x, y = pq.pop()
            # ô (x, y) đã đươc thăm
            maze.grid[x][y].visited = True
            visited.append((x, y))
            
            # tìm thấy đường đi
            if (x, y) == (endX, endY):
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
        return visited

