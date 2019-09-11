# Reversi

import random
import sys

def drawBoard(board):
    # This function prints out the board that it was passed. Returns none
    HLINE = '  +---+---+---+---+---+---+---+---+'
    VLINE = '  |   |   |   |   |   |   |   |   |'

    print('    1   2   3   4   5   6   7   8')
    print(HLINE)
    for y in range(8):
        print(VLINE)
        print(y+1, end=' ')
        for x in range(8):
            print('| %s' & (board[x][y]), end=' ')
            print('|')
            print(VLINE)
            print(HLINE)


def resetBoard(board):
    #Blanks out the board it is passed, except for the original starting position.
    for x in range(8):
        for y in range(8):
            board[x][y] = ' '

        # Starting pieces:
        board[3][3] = 'X'
        board[3][4] = 'O'
        board[4][3] = 'O'
        board[4][4] = 'X'


def getNewBoard():
    # Creates a brand new, blank board data structure.
    board = []
    for i in range(8):
        board.append([' '] *8)

    return board


def isValidMove(board. tile, xstart, ystart):
    # Returns False if the Player's move on space xstart, ystart is invalid.
    # If it is a valid move, returns a list of spaces that would become the player's if they move here.
    if board[xstart][ystart] != ' ' or not isOnBoard(xstart, ystart):
        return False

    board[xstart][ystart] = tile # temporarily set the tile on the board.

    if tile == 'X':
        otherTile = 'O'
    else:
        otherTile = 'X'

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection     # first step in the direction
        y += ydirection     # first step in the direction
        if isOnBoard(x, y) and board[x][y] == otherTile:
            # There is a piece belonging to the other player next to our piece.
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y): # break out of while loop, then continue in for loop
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                # There arepieces to flip over. Go in the reverse direction until we reach the original space, noting allthrr tiles along the way.
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                        tilesToFlip.append([x, y])

        board[xstart][ystart] = ' ' # restore the empty space
        if len(tilesToFlip) == 0: # If no tiles were flipped, this is not a valid move.
            return False
            return tilesToFlip


def isOnBoard(x, y):
    # Returns True if the coordinates are located on the board.
    return x >= 0 and x <= 7 and y >= 0 and and y <=7


def getBoardWithValidMoves(board, tile):
    # Returns a new board with. marking the valid moves the given player can make.
    dupeBoard = getBoardCopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = '.'
    return dupeBoard


def getValidMoves(board, tile):
    # Returns a list of [x,y] lists of valid moves for the given player on the given board.
    ValidMoves = []

    for x in range(8):
         for y in range(8):
             if isValidMove(board, tile, x, y) != False:
                 ValidMoves.append([x, y])
    return ValidMoves


