# Place your creative task here!
"""Bonus Features: 
   Created new pieces
   Added a list of the top 3 high scores
   Added dual rotation (uses keys 'a' and 'd' to rotate pieces)
   Added instructions
   Made more attractive pieces
   Allows user to choose change difficulty (uses number keys to change speed of falling piece and user gets higher score per piece cleared at higher speeds)"""

# Be clever, be creative, have fun!
from cmu_graphics import *
import math
import random


def onAppStart(app):
    app.highScore = [0, 0, 0]
    onGameStart(app)
    
    
def onGameStart(app):    
    app.rows = 15
    app.cols = 10
    app.width = 400
    app.height = 505
    app.boardLeft = 75
    app.boardTop = 120
    app.boardWidth = 250
    app.boardHeight = 365
    app.cellBorderWidth = 2
    app.borderColor = rgb(75, 75, 75)
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.pieceIndex = 0
    app.nextPieceIndex = 0
    app.difficulty = 1
    app.stepsPerSecond = 2
    app.paused = False
    app.score = 0
    app.gameOver = False
    loadTetrisPieces(app)
    loadNextPiece(app)


def redrawAll(app):
    if app.gameOver:
        drawLabel(f'Game Over :(', app.width/2, app.height/2-50, size=30, fill='red')
        drawLabel(f'Your Score: {app.score}', app.width/2, app.height/2-20, size=19)
        drawLabel(f'press r to play again', app.width/2, app.height/2+140, size=16)
        drawLabel(f'High Scores:', app.width/2, app.height/2+25, size=19)
        drawLabel(str(app.highScore[0]), app.width/2, app.height/2+40, size=16)
        drawLabel(str(app.highScore[1]), app.width/2, app.height/2+55, size=16)
        drawLabel(str(app.highScore[2]), app.width/2, app.height/2+70, size=16)
    else:    
        drawLabel('Tetris', app.width/2, 15, size=25, bold=True, font='montserrat', fill=gradient('red', 'green', 'dodgerBlue',  start='left-top'))
        drawLabel('left, right and down arrow keys move pieces', 200, 40, size=11)
        drawLabel("space bar hard drops pieces", 200, 50, size=11)
        drawLabel("up arrow key rotates pieces 180°", 200, 60, size=11)
        drawLabel("'a' and 'd' rotate pieces 90° clockwise and counterclockwise" , 200, 70, size=11)
        drawLabel("'1' to '9' number keys select the difficulty of the game" , 200, 80, size=11)
        drawLabel('press p to pause/unpause the game', 200, 90, size=11)
        drawLabel(f"Score: {app.score}", 10, 105, size=14, align='left')
        drawBoard(app)
        drawPiece(app)
        drawBoardBorder(app)
        
        if app.paused:
            drawLabel('PAUSED', app.width/2, 105, size=13, fill="darkOrange", bold=True)


def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            drawCell(app, row, col, app.board[row][col])


def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border=app.borderColor,
           borderWidth=2*app.cellBorderWidth)


def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border=app.borderColor,
             borderWidth=app.cellBorderWidth)


def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)


def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)
    
    
def loadTetrisPieces(app):
    # Seven "standard" pieces (tetrominoes)
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]] 
    uMyPiece = [[  True,  False, True ],
                [ True,  True,  True ]]
    rMyPiece = [[  True,  True ],
                [ True,  False ]]
    TMyPiece = [[  True,  True, True ],
                [ False,  True, False ],
                [  False, True, False]]
    LMyPiece = [[  True,  False, False ],
                [ True,  False, False ],
                [  True, True, True]]
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece, uMyPiece, rMyPiece, TMyPiece, LMyPiece ]
    app.tetrisPieceColors = [ gradient('red', 'orange', 'yellow', start='top'), 
                              gradient('royalBlue', 'green', 'yellow', start='top'), 
                              gradient('purple', 'pink', 'magenta', start='top'), 
                              gradient('lightGreen', 'darkGreen', 'cyan', 'lime', start='top'),
                              gradient('paleTurquoise', 'lightCyan', 'cornFlowerBlue', start='top'), 
                              gradient('cyan', 'blue', 'indigo', 'lightBlue', start='top'), 
                              gradient('yellow', 'goldenrod', 'chocolate', start='top'), 
                              gradient('lightSalmon', 'darkRed', 'coral', start='top'), 
                              gradient('fireBrick', 'red', 'tomato', start='top'), 
                              gradient('slateGray', 'darkSeaGreen', 'darkOliveGreen', start='top'),
                              gradient('crimson', 'teal', 'honeydew', start='top')]
               
                              
def loadPiece(app, pieceIndex):
    app.piece = app.tetrisPieces[pieceIndex]
    app.pieceColor = app.tetrisPieceColors[pieceIndex]
    app.pieceTopRow = 0
    app.pieceCols = 0
    for i in app.piece:
        app.pieceCols = max(app.pieceCols, len(i))
    app.centerColIndex = app.cols // 2
    app.pieceLeftCol = (app.cols - app.pieceCols) // 2
    if not pieceIsLegal(app):
         app.highScore.append(app.score)
         app.highScore.sort(reverse = True)
         app.highScore.pop()
         app.gameOver = True
    
    
def onKeyPress(app, key):
    # if '0' <= key <= '6':
    #     app.pieceIndex = int(key)
    #     loadPiece(app, app.pieceIndex)
    if not app.gameOver:
        if key == 'p':
            app.paused = not app.paused
        elif '1' <= key <= '9':
            app.difficulty = int(key)
        if app.paused == False:
            if key == 'left':
                movePiece(app, 0, -1)
            elif key == 'right':
                movePiece(app, 0, 1)
            elif key == 'down':
                movePiece(app, 1, 0)
            elif key == 'space':
                hardDropPiece(app)
            elif key == 'd':
                rotatePieceClockwise(app)
            elif key == 'a':
                rotatePieceAntiClockwise(app)
            elif key == 'up':
                rotatePieceClockwise(app)
                rotatePieceClockwise(app)
            elif '1' <= key <= '9':
                app.difficulty = int(key)
        
            
    if app.gameOver:
        if key == 'r':
            app.gameOver = False
            onGameStart(app)
            
    
def drawPiece(app):
    if not app.gameOver: 
        if app.piece != None:
            for row in range(app.rows):
                for col in range(app.cols):
                    if row == app.pieceTopRow and col == app.pieceLeftCol:
                        for i in range(len(app.piece)):
                            for j in range(len(app.piece[i])):
                                if app.piece[i][j]:
                                    drawCell(app, i+row, j+col, app.pieceColor)
            
        
def movePiece(app, drow, dcol):
    if not app.gameOver:
        if app.paused == False:
            app.pieceTopRow += drow
            app.pieceLeftCol += dcol
            if pieceIsLegal(app) == False:
                app.pieceTopRow -= drow
                app.pieceLeftCol -= dcol
                return False
            return True
    
    
def pieceIsLegal(app):
    for i in range(len(app.piece)):
        for j in range(len(app.piece[i])):
            #check if cell is within bounds
            if ((i+app.pieceTopRow < 0) or (j+app.pieceLeftCol < 0) or
            (i+app.pieceTopRow >= app.rows) or (j+app.pieceLeftCol >= app.cols)):
                return False
            else:
                # check if cell is empty
                currentCell = app.board[i+app.pieceTopRow][j+app.pieceLeftCol]
                if app.piece[i][j] == True and currentCell != None:
                    return False
    return True
    

def hardDropPiece(app):
    if not app.gameOver:
        if app.paused == False:
            while movePiece(app, +1, 0):
                pass
    
    
def rotate2dListClockwise(L):
    newRows = len(L[0])
    newCols = len(L)
    M = []
    for i in range(newRows):
        M.append([None] * newCols)
    
    for oldRow in range(len(L)):
        for oldCol in range(len(L[oldRow])):
            M[oldCol][oldRow] = L[oldRow][oldCol]
    for newRow in M:
        newRow.reverse()
    return M
    

def rotate2dListAntiClockwise(L):
    newRows = len(L[0])
    newCols = len(L)
    M = []
    for i in range(newRows):
        M.append([None] * newCols)
    
    for oldRow in range(len(L)):
        for oldCol in range(len(L[oldRow])):
            M[oldCol][oldRow] = L[oldRow][oldCol]
    M.reverse()
    return M
    
    
def rotatePieceClockwise(app):
    if not app.gameOver:
        if app.paused == False:
            oldPiece = app.piece
            oldTopRow = app.pieceTopRow
            oldLeftCol = app.pieceLeftCol
            oldRows = len(oldPiece)
            oldCols = len(oldPiece[0])
            newRows = len(oldPiece[0])
            newCols = len(oldPiece)
            
            app.piece = rotate2dListClockwise(app.piece)
            centerRow = oldTopRow + oldRows//2
            app.pieceTopRow = centerRow - newRows//2
            centerCol = oldLeftCol + oldCols//2
            app.pieceLeftCol = centerCol - newCols//2
            
            if pieceIsLegal(app) == False:
                app.piece = oldPiece
                app.pieceTopRow = oldTopRow
                app.pieceLeftCol = oldLeftCol
                return False
            return True
    
    
def rotatePieceAntiClockwise(app):
    if not app.gameOver:
        if app.paused == False:
            oldPiece = app.piece
            oldTopRow = app.pieceTopRow
            oldLeftCol = app.pieceLeftCol
            oldRows = len(oldPiece)
            oldCols = len(oldPiece[0])
            newRows = len(oldPiece[0])
            newCols = len(oldPiece)
            
            app.piece = rotate2dListAntiClockwise(app.piece)
            centerRow = oldTopRow + oldRows//2
            app.pieceTopRow = centerRow - newRows//2
            centerCol = oldLeftCol + oldCols//2
            app.pieceLeftCol = centerCol - newCols//2
            
            if pieceIsLegal(app) == False:
                app.piece = oldPiece
                app.pieceTopRow = oldTopRow
                app.pieceLeftCol = oldLeftCol
                return False
            return True
            
            
def loadNextPiece(app):
    if not app.gameOver:
        if app.paused == False:
            loadPiece(app, app.nextPieceIndex)
            # if app.nextPieceIndex == len(app.tetrisPieces) - 1:
            #     app.nextPieceIndex = 0
            # else:
            #     app.nextPieceIndex += 1
            app.nextPieceIndex = random.randrange(len(app.tetrisPieces))


def takeStep(app):
    if not app.gameOver:
        if app.paused == False:
            if not movePiece(app, +1, 0):
                # We could not move the piece, so place it on the board:
                placePieceOnBoard(app)
                removeFullRows(app)
                loadNextPiece(app)
        
        
def placePieceOnBoard(app):
    if not app.gameOver:
        if app.paused == False:
            for i in range(len(app.piece)):
                for j in range(len(app.piece[i])):
                    if app.piece[i][j] == True:
                        app.board[i+app.pieceTopRow][j+app.pieceLeftCol] = app.pieceColor


def onStep(app):
    if not app.gameOver:
        app.stepsPerSecond = 2 * (app.difficulty ** 0.4)
        if app.paused == False:
            takeStep(app)
    

def removeFullRows(app):
    if not app.gameOver:
        if app.paused == False:
            row = 0
            rowsPopped = 0
            while row < len(app.board):
                if None not in app.board[row]:
                    app.board.pop(row)
                    rowsPopped += 1
                else:
                    row += 1
            app.score += (rowsPopped ** 2) * app.difficulty
            for i in range(rowsPopped):
                app.board.insert(0, [None]*app.cols)

                
# def loadTestBoard(app, key):
#     # DO NOT EDIT THIS FUNCTION
#     # We are providing you with this function to set up the board
#     # with some test cases for clearing the rows.
#     # To use this: press 'a', 'b', through 'h' to select a test board.
#     # Then press 'space' for a hard drop of the red I,
#     # and then press 's' to step, which in most cases will result
#     # in some full rows being cleared.

#     # 1. Clear the board and load the red I piece 
#     app.board = [([None] * app.cols) for row in range(app.rows)]
#     app.nextPieceIndex = 0
#     loadNextPiece(app)
#     # 2. Move and rotate the I piece so it is vertical, in the
#     #    top-left corner
#     for keyName in ['down', 'down', 'up', 'left', 'left', 'left']:
#         onKeyPress(app, keyName)
#     # 3. Add a column of alternating plum and lavender cells down
#     #    the rightmost column
#     for row in range(app.rows):
#         app.board[row][-1] = 'plum' if (row % 2 == 0) else 'lavender'
#     # 4. Now almost fill some of the bottom rows, leaving just the
#     #    leftmost column empty
#     indexesFromBottom = [ [ ], [0], [0,1], [0,1,2], [0,2],
#                           [1,2,3], [1,2,4], [0,2,3,5] ]
#     colors = ['moccasin', 'aqua', 'khaki', 'aquamarine',
#               'darkKhaki', 'peachPuff']
#     for indexFromBottom in indexesFromBottom[ord(key) - ord('a')]:
#         row = app.rows - 1 - indexFromBottom
#         color = colors[indexFromBottom]
#         for col in range(1, app.cols):
#             app.board[row][col] = color
            
            
def main():
    runApp()

main()