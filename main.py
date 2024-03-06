import sys

import pygame
from queue import PriorityQueue
import time

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('A* Pathfinder')

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.color = WHITE
        self.neighbour = []
        self.width = width
        self.total_rows = total_rows
        self.f = 0
        self.g = 0
        self.h = 0

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == PURPLE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbour(self, grid):
        self.neighbour.clear()
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbour.append(grid[self.row - 1][self.col])
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbour.append(grid[self.row + 1][self.col])
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbour.append(grid[self.row][self.col - 1])
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbour.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(WIN)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


def h_cost(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(current, came_from):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    path.append(current)
    return path


def algorithm(draw, grid, start, end):
    count = 0
    open_list = PriorityQueue()
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h_cost(start.get_pos(), end.get_pos())
    came_from = {}

    open_list.put((0, count, start))
    open_list_hash = {start}

    while not open_list.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_list.get()[2]
        open_list_hash.remove(current)

        if current == end:
            path = reconstruct_path(current, came_from)
            for node in path:
                node.make_path()
            end.make_end()
            start.make_start()
            draw()
            print(f'Path: {path}')
            break

        for neighbour in current.neighbour:
            print(current.neighbour)
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbour]:
                print('gut')
                came_from[neighbour] = current
                g_score[neighbour] = temp_g
                f_score[neighbour] = temp_g + h_cost(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_list_hash:
                    count += 1
                    open_list.put((f_score[neighbour], count, neighbour))
                    open_list_hash.add(neighbour)
                    neighbour.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def main():
    ROWS = 25
    grid = make_grid(ROWS, WIDTH)
    start = None
    end = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                print(row, col)
                node = grid[col][row]
                if not start and node != end:
                    start = node
                    print(start)
                    start.make_start()
                elif not end and node != start:
                    end = node
                    print(end)
                    end.make_end()
                elif node != end and node != start:
                    node.make_barrier()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for node in row:
                            node.update_neighbour(grid)
                    algorithm(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, end)

        draw(WIN, grid, ROWS, WIDTH)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted by the user')
