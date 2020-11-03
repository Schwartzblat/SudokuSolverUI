import pygame
import threading
import time

pygame.font.init()


class Grid:

    def __init__(self, rows, cols, width, height, boardNums):
        self.board = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                self.board[i][j] = int(boardNums[i * 9 + j])
        self.rows = rows
        self.cols = cols
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.selected = None

    def draw(self, win):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

    def updateBoard(self, rows, cols, width, height):
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]


class Cube:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.green = False
        if self.value > 0:
            self.green = True

    def draw(self, win):
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))
        if self.green:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)


def redraw_window(win, board):
    win.fill((255, 255, 255))
    fnt = pygame.font.SysFont("comicsans", 40)
    # Draw grid and board
    board.draw(win)


def solveSlow():
    global counter
    counter = counter + 1
    if counter % 5 == 0:
        time.sleep(0.00000000000000000001)
    global board
    find = find_empty(board.board)
    if not find:
        return True
    else:
        row, col = find
    for i in range(1, 10):
        if valid(board.board, i, (row, col)):
            board.board[row][col] = i

            if solveSlow():
                return True

            board.board[row][col] = 0

    return False


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return i, j
    return None


def print_board(board):
    for i in range(len(board)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(board[i][j])
            else:
                print(str(board[i][j]) + " ", end="")

def valid(board, num, pos):
    # check_row
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True


counter = 0
clock = pygame.time.Clock()
# 800000000003600000070090200050007000000045700000100030001000068008500010090000400
print("enter the numbers for the board in this way for example: \n ")
print("530070000600195000098000060800060003400803001700020006060000280000419005000080079 \n")
print("for this board:")
print("5 3 0  | 0 7 0  | 0 0 0")
print("6 0 0  | 1 9 5  | 0 0 0")
print("0 9 8  | 0 0 0  | 0 6 0")
print("- - - - - - - - - - - - - ")
print("8 0 0  | 0 6 0  | 0 0 3")
print("4 0 0  | 8 0 3  | 0 0 1")
print("7 0 0  | 0 2 0  | 0 0 6")
print("- - - - - - - - - - - - - ")
print("0 6 0  | 0 0 0  | 2 8 0")
print("0 0 0  | 4 1 9  | 0 0 5")
print("0 0 0  | 0 8 0  | 0 7 9")
print("-----------------------------")
boardNums = input("enter your board nums: \n")
win = pygame.display.set_mode((540, 600))
pygame.display.set_caption("Sudoku")
board = Grid(9, 9, 540, 540, boardNums)
run = True
board1 = board.board
value = True
time.sleep(3)
while run:
    clock.tick(300)
    thread = threading.Thread(target=solveSlow)
    thread.start()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    board.updateBoard(9, 9, 540, 540)
    redraw_window(win, board)
    pygame.display.update()
print(counter)
pygame.quit()
