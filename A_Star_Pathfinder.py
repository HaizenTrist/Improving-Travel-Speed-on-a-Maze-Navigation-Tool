# Controls
## Left Click: Place block
## Middle Click: Place Origin/Goal
## Right Click: Erase tile
## Enter: Start pathing
## Right Shift: Clear board

import math
from queue import PriorityQueue
import pygame

windowWidth = 1000
windowRows = 50
tileWidth = windowWidth // windowRows
colorBorder = (117, 117, 117)
stateEmpty = (238, 238, 238)
stateBlocked = (33, 33, 33)
stateOrigin = (76, 175 ,80)
stateGoal = (255, 238, 28)
stateChecked = (2, 136, 209)
stateSelected = (229, 57, 53)
statePath = (132, 255, 255)

window = pygame.display.set_mode((windowWidth, windowWidth))
pygame.display.set_caption("A* Pathfinder")


class Tile:
    def __init__(self, row, col, width, rowTotal):
        self.row = row
        self.col = col
        self.state = stateEmpty
        self.adjacent = []
        self.x = row * width
        self.y = col * width
        self.width = width
        self.rowTotal = rowTotal

    def Place(self):
        pygame.draw.rect(window, self.state, (self.x, self.y, self.width, self.width))

    def FindEmpty(self, board):
        self.adjacent = []
        
        if self.row > 0 and board[self.row-1][self.col].state != stateBlocked:
            self.adjacent.append(board[self.row-1][self.col])
        
        if self.row < self.rowTotal-1 and board[self.row+1][self.col].state != stateBlocked:
            self.adjacent.append(board[self.row + 1][self.col])

        if self.col > 0 and board[self.row][self.col-1].state != stateBlocked:
            self.adjacent.append(board[self.row][self.col-1])

        if self.col < self.rowTotal-1 and board[self.row][self.col+1].state != stateBlocked:
            self.adjacent.append(board[self.row][self.col+1])


def ReconstructPath(cameFrom, current, draw, origin):
    while current in cameFrom:
        current = cameFrom[current]
        if current != origin:
            current.state = statePath
        draw()


def AStar(origin, goal, board, draw):
    order = 0
    cameFrom = {}
    openSet = PriorityQueue()
    openSet.put((0, order, origin))
    openSetHash = {origin}

    gScore = {tile: float("inf") for row in board for tile in row}
    fScore = {tile: float("inf") for row in board for tile in row}
    gScore[origin] = 0
    fScore[origin] = abs(origin.row - goal.row) + abs(origin.col - goal.col)

    while not openSet.empty():
        current = openSet.get()[2]
        openSetHash.remove(current)

        if current == goal:
            ReconstructPath(cameFrom, goal, draw, origin)
            goal.state = stateGoal
            return True

        for adjacent in current.adjacent:
            gBuffer = gScore[current] + 1

            if gBuffer < gScore[adjacent]:
                cameFrom[adjacent] = current
                gScore[adjacent] = gBuffer
                fScore[adjacent] = gBuffer + (abs(adjacent.row - goal.row) + abs(adjacent.col - goal.col))
                
                if adjacent not in openSetHash:
                    order = order + 1
                    openSet.put((fScore[adjacent], order, adjacent))
                    openSetHash.add(adjacent)
                    adjacent.state = stateSelected

        if current != origin:
            current.state = stateChecked

        draw()
        
    return False


def DefineBoard():
	board = []
	for i in range(windowRows):
		board.append([])
		for j in range(windowRows):
			tile = Tile(i, j, tileWidth, windowRows)
			board[i].append(tile)
	return board


def DrawBoard(board):
    window.fill(stateEmpty)

    for row in board:
        for tile in row:
            tile.Place()

    for i in range(windowRows):
        pygame.draw.line(window, colorBorder, (0, i * tileWidth), (windowWidth, i * tileWidth))
        for j in range(windowRows):
            pygame.draw.line(window, colorBorder, (j * tileWidth, 0), (j * tileWidth, windowWidth))

    pygame.display.update()


def main():
    board = DefineBoard()
    running = True
    origin = None
    goal = None

    while running:
        DrawBoard(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if pygame.mouse.get_pressed():
                pos = pygame.mouse.get_pos()
                row, col = pos[0]//tileWidth, pos[1]//tileWidth
                tile = board[row][col]
                
                if pygame.mouse.get_pressed()[1]:
                    if not origin and tile != goal:
                        origin = tile
                        origin.state = stateOrigin  
                    elif not goal and tile != origin:
                        goal = tile
                        goal.state = stateGoal
                
                if pygame.mouse.get_pressed()[0]:
                    if tile != goal and tile != origin:
                        tile.state = stateBlocked

                elif pygame.mouse.get_pressed()[2]:
                    tile.state = stateEmpty
                    if tile == origin:
                        origin = None
                    elif tile == goal:
                        goal = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and origin and goal:
                    for row in board:
                        for tile in row:
                            tile.FindEmpty(board)

                    AStar(origin, goal, board, lambda: DrawBoard(board))

                if event.key == pygame.K_RSHIFT:
                    board = DefineBoard()
                    origin = None
                    goal = None


main()