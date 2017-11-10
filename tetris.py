# Barebones timer, mouse, and keyboard events

from tkinter import *
import random
import copy

####################################
# customize these functions
####################################


 # Seven "standard" pieces (tetrominoes)
iPiece = [
    [  True,  True,  True,  True ]
]

jPiece = [
    [  True, False, False ],
    [  True,  True,  True ]
]

lPiece = [
    [ False, False,  True ],
    [  True,  True,  True ]
]

oPiece = [
    [  True,  True ],
    [  True,  True ]
]

sPiece = [
    [ False,  True,  True ],
    [  True,  True, False ]
]

tPiece = [
    [ False,  True, False ],
    [  True,  True,  True ]
]

zPiece = [
    [  True,  True, False ],
    [ False,  True,  True ]
]
   
#make a list of piece and piecesColors
tetrisPieces = [ iPiece, jPiece, lPiece, oPiece, sPiece, tPiece, zPiece ]    
tetrisPiecesColors = [ "red", "yellow", "magenta", "pink", 
                                "cyan", "green", "orange" ]


def boardMaker(row, col, color):
    #make a base board
    board = []
    #make a nest loop of row and col
    for i in range(row):
        rowList = []
        for j in range(col):
            rowList.append(color)
        board.append(rowList)
    return board

     
def init(data):
    # load data.xyz as appropriate
    data.isGameOver = False
    data.rows, data.cols = 15, 10
    data.margin = 20
    data.cellSize = 20
    data.emptyColor = "blue"
    data.board = boardMaker(data.rows, data.cols, data.emptyColor)
    data.tetrisPieces = tetrisPieces
    data.tetrisPiecesColors = tetrisPiecesColors
    newFallingPiece(data)
    data.fallingPieceRow = 0
    data.fallingPieceCol = data.cols//2 - len(data.fallingPiece[0])//2 
    data.drow, data.dcol = 0, 0 
    data.score = 0
    

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    #define action for four arrow keys
    if moveFallingPiece(data, +1, 0):
        if (event.keysym == "Up"):
            listRotator(data)
        if (event.keysym == "Down"):
            moveFallingPiece(data, +1, 0)
        elif (event.keysym == "Left"):
            moveFallingPiece(data, 0, -1)
        elif(event.keysym == "Right"):
            moveFallingPiece(data, 0, +1)  
    #define reset
    if(event.keysym == "r"):
        init(data)
        pass


def timerFired(data):
    #fall pieces as the time passed
    moveFallingPiece(data, +1, 0)
    #make pieces sit bottom when they reach bottom
    placeFallingPiece(data)
    

def redrawAll(canvas, data):
    # draw in canvas
    drawBoard(canvas, data)
    drawFallingPiece(canvas, data)
    drawGameOver(canvas, data)
    drawScore(canvas, data)
    
def drawCell(canvas, data, row, col, color):
    #draw each cells
    x = data.margin + data.cellSize * col
    y = data.margin + data.cellSize * row
    canvas.create_rectangle(x, y, x + data.cellSize, y + data.cellSize, 
                            width = 3, fill = color)
                                    
def drawBoard(canvas, data):
    #draw background orange board
    canvas.create_rectangle(0, 0, data.width, data.height, fill = "orange")
    
    #draw board referring to each cell's color
    for row in range(data.rows):
        for col in range(data.cols):
            drawCell(canvas, data, row, col, data.board[row][col])
            
def newFallingPiece(data):
    #check if the game continues
    if data.isGameOver == False:
        #randomly choose the pieces
        randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
        data.fallingPiece = data.tetrisPieces[randomIndex]
        data.fallingPieceColor = data.tetrisPiecesColors[randomIndex]


def drawFallingPiece(canvas, data):
    #assign number of each rows and cols
    fallingPieceRows = len(data.fallingPiece)
    fallingPieceCols = len(data.fallingPiece[0])
    #make a nest loop using numbers of rows and cols
    for i in range(fallingPieceRows):
        for j in range(fallingPieceCols):
            #assign colors to cells of the pieces which are "True"
            if data.fallingPiece[i][j] == True:
                drawCell(canvas, data, i+data.fallingPieceRow,
                        j+data.fallingPieceCol, data.fallingPieceColor)
                        

def fallingPieceIsLegal(data):
    #assign number of each rows and cols
    fallingPieceRows = len(data.fallingPiece)
    fallingPieceCols = len(data.fallingPiece[0])
    #make a nest loop using numbers of rows and cols
    for i in range(fallingPieceRows):
        for j in range(fallingPieceCols):
            if data.fallingPiece[i][j] == True:
                #check if the falling piece is legal
                if i+data.fallingPieceRow < 0  \
                or i+data.fallingPieceRow >= data.rows \
                or j+data.fallingPieceCol < 0 or j+data.fallingPieceCol >=\
                 data.cols or not \
                 data.board[i+data.fallingPieceRow][j+data.fallingPieceCol]\
                 == data.emptyColor:
                    return False
    return True

    
def moveFallingPiece(data, drow, dcol):
    #store previous falling piece's information
    prevFallingPieceRow = copy.copy(data.fallingPieceRow)
    prevFallingPieceCol = copy.copy(data.fallingPieceCol)
    data.fallingPieceRow += drow
    data.fallingPieceCol += dcol
    #if the move is illegal, undo the above action
    if fallingPieceIsLegal(data) == False:
        data.fallingPieceRow = prevFallingPieceRow
        data.fallingPieceCol = prevFallingPieceCol
        return  False
    else:
        return True
        
        
def placeFallingPiece(data):
    #check if the move has occurred
    if moveFallingPiece(data, +1, 0) == False:
        #if the move hasn't occured, set the piece to the place
        fallingPieceRows = len(data.fallingPiece)
        fallingPieceCols = len(data.fallingPiece[0])
        for i in range(fallingPieceRows):
            for j in range(fallingPieceCols):
                if data.fallingPiece[i][j] == True:
                    #assign the piece's color to the place
                    data.board[i+data.fallingPieceRow][j+data.fallingPieceCol]\
                     = data.fallingPieceColor
        #remove full rows
        removeFullRows(data)
        #reset the start place of the falling piece
        data.fallingPieceRow = 0
        data.fallingPieceCol = data.cols//2 - len(data.fallingPiece[0])//2 
        #call new falling piece
        newFallingPiece(data)
        #if the falling piece placed illegally, turn isGameOver to True
        if fallingPieceIsLegal(data) == False:
            data.isGameOver = True
            
            
def drawGameOver(canvas,data):
    #draw the sign of game over
    if data.isGameOver == True:
        canvas.create_rectangle(data.margin, 
                                data.margin+data.cellSize*2, 
                                data.width-data.margin, 
                                data.margin+data.cellSize * 4,
                                fill = "black")
        canvas.create_text(data.width/2, 
                            (data.margin+data.cellSize*2 +\
                             data.margin+data.cellSize * 4)/2,
                            text= "Game Over!", fill = "Yellow",\
                            font="Helvetica 22 bold")
                            
def drawScore(canvas, data):
    #draw the score
    canvas.create_text(data.width//2, data.margin//2,
                    text = "Score: "+str(data.score), 
                    fill = "dark blue", font="Helvetica 15 bold")

def removeFullRows(data):
    #remove full rows
    newBoard = []
    fullRow = 0
    for row in range(data.rows):
        counter = 0
        for col in range(data.cols):
            if not data.board[row][col] == data.emptyColor:
                counter +=  1
                #check if the row is full
                if counter == data.cols:
                    #count full rows
                    fullRow += 1
                    continue
        #make a new list that contains rows which are not full
        if counter < data.cols:
            newBoard.append(data.board[row])
    #add new empty rows on the top of newBoard, referring to the number 
    #of full rows
    newBoard = [[data.emptyColor]* data.cols] * fullRow + newBoard
    #count scores
    data.score += fullRow**2
    #assign to data.board
    data.board = newBoard
    
    
def make2dList(rows, cols):
    #function to make a list with zero
    newList = []
    rowList = []
    #make a nest loop
    for row in range(rows):
        for col in range(cols):
            rowList.append(0)
        newList.append(rowList)
        rowList = []
    return newList
    
    
def listRotator(data):
    #store previous piece information
    oldPiece = data.fallingPiece
    prevCol = data.fallingPieceCol
    oldPieceRows = len(data.fallingPiece)
    oldPieceCols = len(data.fallingPiece[0])
    
    #make new(rotated) 2dList of the piece using make2dList function
    newPiece = make2dList(oldPieceCols, oldPieceRows)
    
    #make a nest loop of oldRow and oldCol
    for oldRow in range(oldPieceRows):
        for oldCol in range(oldPieceCols):
            #change row and col
            newCol = oldRow
            newRow = (oldPieceCols-1) - oldCol
            newPiece[newRow][newCol] = oldPiece[oldRow][oldCol]
            
    #assing as rotated piece
    data.fallingPiece = newPiece
    
    #if the rotation illegal, undo the above action
    if not fallingPieceIsLegal(data):
       data.fallingPieceCol = prevCol
       data.fallingPiece = oldPiece
   
   
####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 400 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

def playTetris():
    rows, cols, cellSize, margin = 15, 10, 20, 20
    run(width = cols*cellSize + margin*2, height = rows*cellSize + margin*2)

# run(400, 200)
playTetris()