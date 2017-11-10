import math
import copy

def areLegalValues(values):
    #make a value list containing 1~value factor
    valueList = []
    for i in range(1,len(values)+1):
        valueList.append(i)
    newValueList = copy.copy(valueList)
    
    #make a loop using value to check if the values are legal
    for value in values:
        #define isLegal and if isLegal turns False, it will break the loop
        isLegal = True
        if value != 0:
            if value not in newValueList:
                isLegal = False
                break
            valueIndex = newValueList.index(value)
            newValueList = newValueList[:valueIndex] \
            + newValueList[valueIndex + 1:]
        elif value == 0:
            isLegal = True
    if isLegal == True:
        return True
    else:
        return False
        
def isLegalRow(board, row):
    #make loop using areLegalValues
    if areLegalValues(board[row]):
        return True
    else:
        return False
        
        
def isLegalCol(board, col):
    #make colList that has colmn of each row
    colList = []
    #make loop to make colList
    for row in range(len(board)):
        colList.append(board[row][col])
    #check the colList using areLegalValues
    if areLegalValues(colList):
        return True
    else:
        return False
        
        
def isLegalBlock(board, block):
    #make blockList that has list of each block
    blockList = []
    lenBlock = int((len(board))**.5)
    #calculate both row's and col's start index
    rowStart = (block // lenBlock) * lenBlock
    colStart = (block % lenBlock) * lenBlock
    #make a loop to make block list
    for row in range(rowStart, rowStart + lenBlock):
        for col in range(colStart, colStart + lenBlock):
            blockList.append(board[row][col])
    #check the list using areLegalValues
    if areLegalValues(blockList):
        return True
    else:
        return False
        
        
        
def isLegalSudoku(board):
    #check the board using all of the values above
    for row in range(len(board)):
        if not isLegalRow(board, row):
            return False
    for col in range(len(board[row])):
        if not isLegalCol(board, col):
            return False
    for block in range(len(board)):
        if not isLegalBlock(board, block):
            return False
    return True
        


#function to check if the sudoku is finished
def isFinish(board):
    for row in range(len(board)):
        for col in range(len(board[0])):
            #check if the value == 0
            if board[row][col] == 0:
                return False
    return True
        
        
def solveSudoku(board):
    #base case
    #if the sudoku is solved, return solution 
    if isFinish(board):
        return board
      
    #recursive case
    else:
        #loop through all the cells
        for row in range(len(board)):
            for col in range(len(board)):
                #check if the cell is 0
                if board[row][col] == 0:
                    #put all the possible numbers in the 0 cell
                    for i in range(1,10):
                        board[row][col] = i
                        #check if it is legal
                        if isLegalSudoku(board) == False:
                            #if it isn't, undo the action
                            board[row][col] = 0
                            continue
                        #if it is valid, recurse
                        solution = solveSudoku(board)
                        #check if the recursion has a solution, return it
                        if solution != None:
                            return solution
                        #if it isn't undo the action
                        board[row][col] = 0
                    #if there is no solution, return None
                    return None

def testSolveSudoku():
    print('Testing ', end='')
    board = [
              [ 5, 3, 0, 0, 7, 0, 0, 0, 0 ],
              [ 6, 0, 0, 1, 9, 5, 0, 0, 0 ],
              [ 0, 9, 8, 0, 0, 0, 0, 6, 0 ],
              [ 8, 0, 0, 0, 6, 0, 0, 0, 3 ],
              [ 4, 0, 0, 8, 0, 3, 0, 0, 1 ],
              [ 7, 0, 0, 0, 2, 0, 0, 0, 6 ],
              [ 0, 6, 0, 0, 0, 0, 2, 8, 0 ],
              [ 0, 0, 0, 4, 1, 9, 0, 0, 5 ],
              [ 0, 0, 0, 0, 8, 0, 0, 7, 9 ]
            ]
    solved = solveSudoku(board)
    solution = [
                [5, 3, 4, 6, 7, 8, 9, 1, 2], 
                [6, 7, 2, 1, 9, 5, 3, 4, 8], 
                [1, 9, 8, 3, 4, 2, 5, 6, 7], 
                [8, 5, 9, 7, 6, 1, 4, 2, 3], 
                [4, 2, 6, 8, 5, 3, 7, 9, 1], 
                [7, 1, 3, 9, 2, 4, 8, 5, 6], 
                [9, 6, 1, 5, 3, 7, 2, 8, 4], 
                [2, 8, 7, 4, 1, 9, 6, 3, 5], 
                [3, 4, 5, 2, 8, 6, 1, 7, 9]
               ]
    assert(solved == solution)
    print('Passed')

testSolveSudoku()