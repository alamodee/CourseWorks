from tkinter import *
import string
import math
import copy

#function to load data
def init(data):
    data.rows = 9
    data.cols = 9
    data.cell = [0, 0]
    data.counter = 0
    data.margin = 20
    data.num = ""
    data.drawNum = False
    data.changedList = []
    data.delete = False
    data.gameOver = False

#function to define key controling 
def keyPressed(event, data):
    #check if the game is still continued
    if data.gameOver == False:
        #key of direction
        if (event.keysym == "Up"):
            data.cell[0] -= 1
            data.drawNum = False
        elif (event.keysym == "Down"):
            data.cell[0] += 1
            data.drawNum = False
        elif (event.keysym == "Left"):
            data.cell[1] -= 1
            data.drawNum = False
        elif(event.keysym == "Right"):
            data.cell[1] += 1
            data.drawNum = False
        #key of digit
        elif(event.keysym in [str(i) for i in range(1,10)]):
            data.num = event.keysym
            data.drawNum = True
        #key of backspase
        elif(event.keysym == "BackSpace"):
            data.num = 0
            data.delete = True
    
            
#function that returns the number of block with given number of row and col
def blockCounter(row, col, data):
    blockList = []
    lenBlock = int((len(data.board[0]))**.5)
    #make a loop using the number of block
    for block in range(len(data.board[0])):
        rowStart = (block // lenBlock) * lenBlock
        colStart = (block % lenBlock) * lenBlock
        #make a loop using row and col, and register those two values
        for bRow in range(rowStart, rowStart + lenBlock):
            for bCol in range(colStart, colStart + lenBlock):
                blockList.append([bRow,bCol])
                #return the number of block with the given number of row and col
                if (row, col) == (bRow, bCol):
                    return block
                    

#function to draw board
def drawBoard(canvas, data):
    squareSize = (data.width - data.margin) / len(data.board[0])
    
    #deal with cases that the current point is off the board
    if data.cell[0] >= data.cols:
        data.cell[0] = 0
    elif data.cell[0] < 0:
        data.cell[0] = data.cols-1
    elif data.cell[1] >= data.rows:
        data.cell[1] = 0
    elif data.cell[1] < 0:
        data.cell[1] = data.cols-1
    
    #define current cell
    (currRow, currCol) = data.cell
     
    #make a for loop to make a grid
    for row in range(len(data.board)):
        for col in range(len(data.board[0])):
            left = data.margin/2 + squareSize * col
            top = data.margin/2 + squareSize * row
            right = data.margin/2 + squareSize * (col+1)
            bottom = data.margin/2 +squareSize * (row+1)
            block = blockCounter(row, col, data)
            #check the current row and column
            if (row, col) == (currRow, currCol):
                color = "MistyRose2"
            else:
                color = "white"
            
            canvas.create_rectangle(left, top, right, bottom, width = 1, 
                                    fill=color, outline="PeachPuff4")
            num = data.board[row][col]

            #define the case to delete the digit
            if (row, col) == (currRow, currCol) and\
               data.delete == True and [row, col] in data.changedList:
                   data.board[row][col] = 0
                   num = data.board[row][col]
                   data.delete = False
            
            #define the case to draw the digit that the player type
            if (row, col) == (currRow, currCol) and\
               data.drawNum == True and num == 0 and data.delete == False:
                   data.board[row][col] = int(data.num)
                   #check if the number makes legal row, col, and block
                   if isLegalCol(data.board,col) and \
                            isLegalRow(data.board,row)and\
                            isLegalBlock(data.board, block) and data.num != 0:
                          numColor = "gray33"
                          canvas.create_text((left+right)/2, (top+bottom)/2, 
                          text=data.num, fill=numColor, 
                          font="Helvetica 18 bold")
                          data.changedList.append([row, col])
                   else: 
                        data.board[row][col] = 0
                        
            #define the case to draw the initial digit
            if not num == 0:
                if [row, col] in data.changedList:
                    numColor = "gray33"
                else:
                    numColor = "indian red"
                canvas.create_text((left+right)/2, (top+bottom)/2, text=num, 
                                    fill=numColor, font="Helvetica 18 bold")
                                    
#function to draw blocks(bold lines)
def drawBlocks(canvas, data):
    blockNum  = int(len(data.board[0])**.5)
    blockSize = blockNum * (data.width - data.margin) / len(data.board[0])
    
    #make a loop using row and col
    for row in range(blockNum):
        for col in range(blockNum):
            left = data.margin/2 + blockSize * col
            top = data.margin/2 + blockSize * row
            right = data.margin/2 + blockSize * (col+1)
            bottom = data.margin/2 + blockSize * (row+1)
            canvas.create_rectangle(left, top, right, bottom, width = 7,\
                                    outline="#7A1E2A")
                                        
#function to draw the message which pops up after the user won                  
def drawWin(canvas, data):
    #make a loop using row and col
    for row in range(len(data.board)):
        for col in range(len(data.board[0])):
            #check if the value == 0
            if data.board[row][col] == 0:
                return False
    #check if the board is legal
    if not isLegalSudoku(data.board):
        return False
    else:
        canvas.create_text(data.width/2, data.height/2, text="You Win!",
                                    fill ="DarkGoldenrod4",
                                    font = "Helvetica 70 bold")
        #finish the game
        data.gameOver = True
            
            
#function to redraw
def redrawAll(canvas, data):
    drawBoard(canvas, data)
    drawBlocks(canvas, data)
    drawWin(canvas, data)

def playSudoku(sudokuBoard, width=500, height=500):
  
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)
        
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.board = sudokuBoard

    # Initialize any other things you want to store in data
    init(data)

    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()

    # set up events
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))

    # Draw the initial screen
    redrawAll(canvas, data)

    # Start the event loop
    root.mainloop()  # blocks until window is closed
    print("bye!")


def main():
    board = [
[1,2,3,4,5,6,7,8,9],
[5,0,8,1,3,9,6,2,4],
[4,9,6,8,7,2,1,5,3],
[9,5,2,3,8,1,4,6,7],
[6,4,1,2,9,7,8,3,5],
[3,8,7,5,6,4,0,9,1],
[7,1,9,6,2,3,5,4,8],
[8,6,4,9,1,5,3,7,2],
[2,3,5,7,4,8,9,1,6]
]
    playSudoku(board)

if __name__ == '__main__':
    main()
