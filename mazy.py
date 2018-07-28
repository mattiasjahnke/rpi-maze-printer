#!/usr/bin/python

# import modules used here -- sys is a very standard one
import sys
from PIL import Image, ImageDraw
import math
import random

class Cell:
    walls = int('1111', 2)
    visited = False

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, draw):
        global start, end, margin

        if self.walls & 1 == 1:
            draw.line([(margin + cellSize * self.x, margin + cellSize * self.y + cellSize), (margin + cellSize * self.x + cellSize, margin + cellSize * self.y + cellSize)], fill="black", width=3)
        if (self.walls >> 1 & 1) == 1:
            draw.line([(margin + cellSize * self.x + cellSize, margin + cellSize * self.y), (margin + cellSize * self.x + cellSize, margin + cellSize * self.y + cellSize)], fill="black", width=3)
        if (self.walls >> 2 & 1) == 1:
            draw.line([(margin + cellSize * self.x, margin + cellSize * self.y), (margin + cellSize * self.x + cellSize, margin + cellSize * self.y)], fill="black", width=3)
        if (self.walls >> 3 & 1) == 1:
            draw.line([(margin + cellSize * self.x, margin + cellSize * self.y), (margin + cellSize * self.x, margin + cellSize * self.y + cellSize)], fill="black", width=3)

        if self.x == start[0] and self.y == start[1]:
            draw.ellipse([margin + cellSize * self.x + cellSize / 4, margin + cellSize * self.y + cellSize / 4, margin + cellSize * self.x + cellSize / 4 + cellSize / 2, margin + cellSize * self.y + cellSize / 4 + cellSize / 2], fill="blue")
        elif self.x == end[0] and self.y == end[1]:
            draw.ellipse([margin + cellSize * self.x + cellSize / 4, margin + cellSize * self.y + cellSize / 4, margin + cellSize * self.x + cellSize / 4 + cellSize / 2, margin + cellSize * self.y + cellSize / 4 + cellSize / 2], fill="green")

rows = 0
cols = 0
image = Image.new('RGB', (380, 400 * 2), (0, 0, 0))
draw = ImageDraw.Draw(image)
cellSize = 20
margin = 10

matrix = []
stack = []
currentCell = None
biggestStack = 0
start = (0, 0)
end = (0, 0)

# Gather our code in a main() function
def main():
    global matrix, stack, currentCell, start, rows, cols, cellSize, margin
    # Setup
    if len(sys.argv) > 1:
        cellSize = int(sys.argv[1])

    drawingWidth = image.width - margin * 2
    drawingHeight = image.height - margin * 2

    draw.rectangle([margin, margin, margin + drawingWidth, margin + drawingHeight], fill="white")

    rows = int(math.floor(drawingHeight / cellSize))
    cols = int(math.floor(drawingWidth / cellSize))

    print(cellSize)

    for y in xrange(rows):
        for x in xrange(cols):
            matrix.append(Cell(x, y))

    currentCell = matrix[0]
    start = (currentCell.x, currentCell.y)

    while nrOfUnvisitedCells() > 0:
        runMazeStep()

    # Draw
    for cell in matrix:
        cell.draw(draw)

    image.save("maze.png")

def runMazeStep():
    global currentCell, stack, end, biggestStack

    currentCell.visited = True

    nei = []

    if currentCell.x > 0:
        cell = matrix[index(currentCell.x - 1, currentCell.y)]
        if not cell.visited:
            nei.append(cell)
    if currentCell.y > 0:
        cell = matrix[index(currentCell.x, currentCell.y - 1)]
        if not cell.visited:
            nei.append(cell)
    if currentCell.x < cols - 1:
        cell = matrix[index(currentCell.x + 1, currentCell.y)]
        if not cell.visited:
            nei.append(cell)
    if currentCell.y < rows - 1:
        cell = matrix[index(currentCell.x, currentCell.y + 1)]
        if not cell.visited:
            nei.append(cell)

    if len(nei) > 0:
        chosen = random.choice(nei)
        stack.append(currentCell)
        if len(stack) > biggestStack:
            biggestStack = len(stack)
            end = (chosen.x, chosen.y)

        if chosen.x < currentCell.x:
            chosen.walls &= ~(1 << 1)
            currentCell.walls &= ~(1 << 3)
        elif chosen.x > currentCell.x:
            chosen.walls &= ~(1 << 3)
            currentCell.walls &= ~(1 << 1)
        elif chosen.y > currentCell.y:
            chosen.walls &= ~(1 << 2)
            currentCell.walls &= ~(1 << 0)
        elif chosen.y < currentCell.y:
            chosen.walls &= ~(1 << 0)
            currentCell.walls &= ~(1 << 2)

        currentCell = chosen
    else:
        currentCell = stack.pop()


def nrOfUnvisitedCells():
    global matrix
    res = len([cell for cell in matrix if not cell.visited])
    return res

def index(x, y):
    global cols
    return y * cols + x

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
