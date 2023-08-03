import pygame
from random import randint

m, n = 70, 70
start_r, start_c = randint(0, m - 1), randint(0, n - 1)
end_r, end_c = randint(0, m - 1), randint(0, n - 1)

WIDTH, HEIGHT = 950, 950
win = pygame.display.set_mode((WIDTH, HEIGHT)) 

grid = [[0] * n for _ in range(m)]

class Node:

    def __init__(self, r, c):
        self.f = float("inf")
        self.g = float("inf")
        self.h = abs(end_r - r) + abs(end_c - c)
        self.r = r
        self.c = c
        self.prev = None
        self.neighbours = []
        self.obstacle = False

    def add_neighbours(self, r, c):

        if r > 0 and grid[r-1][c].obstacle == False:
            self.neighbours.append(grid[r-1][c])
        if r < m - 1 and grid[r+1][c].obstacle == False:
            self.neighbours.append(grid[r+1][c])
        if c > 0 and grid[r][c-1].obstacle == False:
            self.neighbours.append(grid[r][c-1])
        if c < n - 1 and grid[r][c+1].obstacle == False:
            self.neighbours.append(grid[r][c+1])

for i in range(len(grid)):
    for j in range(len(grid[i])):
        grid[i][j] = Node(i, j)

start = grid[start_r][start_c]
end = grid[end_r][end_c]

for i in range(len(grid)):
    for j in range(len(grid[i])):
        if randint(1, 3) == 1 and grid[i][j] != start and grid[i][j] != end: 
            grid[i][j].obstacle = True
            grid[i][j].f = "X"

for i in range(len(grid)):
    for j in range(len(grid[i])):
        grid[i][j].add_neighbours(i, j)

def display_grid(grid):

    for row in range(len(grid)):
        pygame.draw.line(win, (255, 255, 255), (0, row * (HEIGHT/m) - 1), (WIDTH, row * (WIDTH/n) - 1))
    
        for col in range(len(grid[row])):
            pygame.draw.line(win, (255, 255, 255), (col * (WIDTH/n) - 1, 0), (col * (WIDTH/n) - 1, HEIGHT))

            cur_node = grid[row][col]

            color = (125, 125, 125)
            # if cur_node.f != float("inf"):
               # color = (0, 50, 250)
            if cur_node.f == "X":
                color = (0, 0, 0)
            elif cur_node == start:
                color = (0, 255, 0)
            elif cur_node == end:
                color = (255, 0, 0)

            pygame.draw.rect(win, (color), (row * (HEIGHT/m), col * (WIDTH/n), WIDTH/n - 1, HEIGHT/m - 1))

def main():

    display_grid(grid)


    start.g = 0
    start.f = start.h

    open_list = [start]


    clock = pygame.time.Clock()
    FPS = 50

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        clock.tick(FPS)

        def show_shortest_path(cur, prev):
            total_path = []
            while cur.prev and cur.prev != start:
                cur = cur.prev
                total_path.append(cur)
            # print(total_path)
            for i in range(len(grid)):
                for j in range(len(grid[i])):
                    if grid[i][j] in total_path:
                        pygame.draw.rect(win, (75, 75, 200), (i * (HEIGHT/m), j * (WIDTH/n), WIDTH/n - 1, HEIGHT/m - 1))
                        pygame.display.update()


        # check several times if open_list is empty to avoid errors
        lowest = 0
        for i in range(len(open_list)):
            if open_list[i].f < open_list[lowest].f:
                lowest = i
        if len(open_list) > 0 and open_list[lowest] == end:
            print("FOUND A PATH")
            show_shortest_path(open_list[lowest], open_list[lowest].prev)
            continue
        if len(open_list) > 0:
            for neighbour in open_list[lowest].neighbours:
                g_score = open_list[lowest].g + 1
                if g_score < neighbour.g:
                    # find index of neighbour and draw it
                    for i in range(len(grid)):
                        for j in range(len(grid[i])):
                            if grid[i][j] == neighbour and grid[i][j] != end:
                                pygame.draw.rect(win, (25, 120, 200), (i * (HEIGHT/m), j * (WIDTH/n), WIDTH/n - 1, HEIGHT/m - 1))


                    neighbour.prev = open_list[lowest]
                    neighbour.g = g_score
                    neighbour.f = g_score + neighbour.h
                    if neighbour not in open_list:
                        open_list.append(neighbour)
        
        if len(open_list) > 0: open_list.pop(lowest)  



        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
