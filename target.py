from tkinter import *
import random

####################################
# customize these functions
####################################

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))


def init(data):
    #define key factors for a view, a boundary, targets, and scrolling
    data.viewWidth = 400
    data.viewHeight = 400
    data.scrollX = data.viewWidth/2
    data.scrollY = data.viewHeight/2
    data.boundaryWidth = data.viewWidth * 2
    data.boundaryHeight = data.viewHeight* 2
    data.boundaryOutlineWidth = 5
    data.targetCX = data.viewWidth/2
    data.targetCY = data.viewHeight/2
    data.targetXSpeed = 10
    data.targetYSpeed = 10
    data.targetList =[]
    
    #randomly choose target's radious
    data.targetR = random.choice([5, 15, 25])
    data.targetRMax = max([5, 15, 25])
     
    #define score
    data.score = 0
    
    #define time(= 20sec)
    data.time = 20000
    
    #key booleans for the game
    data.isFirstRun = True
    data.isGameStarted = False
    data.isGameOver = False
    
def distance(x1, y1, x2, y2):
    return ((x1-x2)**2 + (y1-y2)**2)**.5

def mousePressed(event, data):
    #make a reverse loop for targes' overlapping
    for row in range(len(data.targetList)-1,-1,-1):
        #check if event.x and event.y are within the target circle
        if (distance(event.x, event.y, data.targetList[row][0]-\
         data.scrollX, data.targetList[row][1] -data.scrollY)\
          <= data.targetList[row][2]):
   
                #delete the clicked target from the list
                deleteIndex = row
                data.targetList.pop(deleteIndex)
                
                #add 1 to the score
                data.score += 1
                
                #add 1 second every 5 targets deleted
                if data.score % 5 == 0:
                    data.time += 1000
                    
                #after deleting one target, break the loop
                break


def keyPressed(event, data):
    #start game
    if (event.keysym == "p"):
        data.isGameStarted = True
        
    #move the view during the game
    if  data.isGameStarted == True:
        if (event.keysym == "Up"):
            data.scrollY -= data.viewHeight/10
        if (event.keysym == "Down"):
            data.scrollY += data.viewHeight/10
        elif (event.keysym == "Left"):
            data.scrollX -= data.viewWidth/10
        elif(event.keysym == "Right"):
            data.scrollX += data.viewWidth/10
            
        #restart the game after the game over
        if data.isGameOver == True:
            if (event.keysym == "s"):
                init(data)
    

def timerFired(canvas, data):
    #check if the game going on
    if data.isGameStarted == True and data.isGameOver == False:
        #decrease time
        data.time -= 100
        
        #make a new target every 0.5 second
        if (data.time//100) % 5 == 0:
            makeNewTarget(data)
            
        #define game over
        if data.time == 0:
            data.isGameOver = True
            

def redrawAll(canvas, data):
    #redraw all factors
    drawStartInstruction(canvas, data)
    drawTarget(canvas, data, data.targetCX, data.targetCY, data.targetR)
    moveTarget(data)
    drawTimeLeft(canvas, data)
    drawScore(canvas, data)
    drawBoundary(canvas, data)
    drawGameOverScreen(canvas, data)


def drawStartInstruction(canvas, data):
    #check if the game started
    if data.isGameStarted == False:
        canvas.create_text(data.viewWidth/2, data.viewHeight\
         /4, text = "Targets Game!", font = "Helvetica 50 bold")
        canvas.create_text(data.viewWidth/2, data.viewHeight * 3/4,\
         text = "Press 'p' to play", font = "Helvetica 30 bold")
 
        
def drawTimeLeft(canvas, data):
    #check if the game going on
    if data.isGameStarted == True and data.isGameOver == False:
        canvas.create_text(data.viewWidth/20, data.viewHeight * 2/20, \
        text = "Time Left: " + str(data.time//1000),\
         font = "Helvetica 25 bold", anchor = "w")
 
    
def drawScore(canvas, data):
    #check if the game going on
    if data.isGameStarted == True and data.isGameOver == False:
        canvas.create_text(data.viewWidth/20, data.viewHeight * 18/20,\
         text = "Score: " + str(data.score), \
         font = "Helvetica 25 bold", anchor = "w")
  
        
def drawBoundary(canvas, data):
    #check if the game going on
    if data.isGameStarted == True and data.isGameOver == False:
        canvas.create_rectangle(-data.scrollX ,\
        -data.scrollY, data.boundaryWidth-data.scrollX,\
         data.boundaryHeight-data.scrollY, fill = "", \
         width = data.boundaryOutlineWidth)

    
def drawTarget(canvas, data, cx, cy, r):
    #check if the game started
    if data.isGameStarted == False:
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill= "red",width=0)
        canvas.create_oval(cx-r*4/5, cy-r*4/5, cx+r*4/5,\
         cy+r*4/5, fill= "white", width=0)
        canvas.create_oval(cx-r*3/5, cy-r*3/5, cx+r*3/5, \
        cy+r*3/5, fill= "red", width=0)
        canvas.create_oval(cx-r*2/5, cy-r*2/5, cx+r*2/5, \
        cy+r*2/5, fill= "white", width=0)
        canvas.create_oval(cx-r*1/5, cy-r*1/5, cx+r*1/5, \
        cy+r*1/5, fill= "red", width=0)
    
    #check if the game going on
    if data.isGameStarted == True and data.isGameOver == False:
        #draw targets referring to target list
        for targetData in data.targetList:
            cx = targetData[0]
            cy = targetData[1]
            r = targetData[2]
            canvas.create_oval(cx-r-data.scrollX, cy-r-data.scrollY, \
            cx+r-data.scrollX, cy+r-data.scrollY, fill= "red",width=0)
            canvas.create_oval(cx-r*4/5-data.scrollX, cy-r*4/5-data.scrollY, \
            cx+r*4/5-data.scrollX, cy+r*4/5-data.scrollY,\
            fill= "white", width=0)
            canvas.create_oval(cx-r*3/5-data.scrollX, cy-r*3/5-data.scrollY, \
            cx+r*3/5-data.scrollX, cy+r*3/5-data.scrollY, fill= "red", width=0)
            canvas.create_oval(cx-r*2/5-data.scrollX, cy-r*2/5-data.scrollY,\
            cx+r*2/5-data.scrollX, cy+r*2/5-data.scrollY, \
            fill= "white", width=0)
            canvas.create_oval(cx-r*1/5-data.scrollX, cy-r*1/5-data.scrollY,\
             cx+r*1/5-data.scrollX, cy+r*1/5-data.scrollY, fill= "red", width=0)


def moveTarget(data):
    #check if the game started
    if data.isGameStarted == False:
        #check if the run the very first run
        if data.isFirstRun == True:
            randomX = random.randint(data.targetRMax, \
            data.viewWidth-data.targetRMax)
            randomY = random.randint(data.targetRMax,\
             data.viewHeight-data.targetRMax)
            data.targetCX = randomX
            data.targetCY = randomY
            data.isFirstRun = False
    
        #check if target on the boundary, and change the vector
        if data.targetCX + data.targetRMax >= data.viewWidth \
        or data.targetCX - data.targetRMax <= 0:
            data.targetXSpeed = - data.targetXSpeed
        if data.targetCY + data.targetRMax >= data.viewHeight\
         or data.targetCY- data.targetRMax <= 0:
            data.targetYSpeed = - data.targetYSpeed
        
        #add targetSpeed to move the target
        data.targetCX += data.targetXSpeed
        data.targetCY += data.targetYSpeed
  
    
def makeNewTarget(data):
    #check if the game going on
    if data.isGameStarted == True and data.isGameOver == False:
        #randomly define the place of target emergence within the boundary area
        randomX = random.randint(data.targetRMax+data.boundaryOutlineWidth, \
        data.boundaryWidth-data.targetRMax-data.boundaryOutlineWidth)
        randomY = random.randint(data.targetRMax+data.boundaryOutlineWidth, \
        data.boundaryHeight-data.targetRMax-data.boundaryOutlineWidth)
        data.targetCX = randomX
        data.targetCY = randomY
        #randomly choose the radius of targets
        data.targetR = random.choice([5, 15, 25])
        #make a list of target information
        data.targetList += [[data.targetCX, data.targetCY, data.targetR]]
        
        
def drawGameOverScreen(canvas, data):
    #check if the game is over
    if data.isGameOver == True:
        canvas.create_rectangle(0,0, data.viewWidth,\
         data.viewHeight, fill= "red")
        canvas.create_text(data.viewWidth/2, data.viewHeight * 1/4, \
        text = "GAME OVER!", font = "Helvetica 50 bold", fill = "white")
        canvas.create_text(data.viewWidth/2, data.viewHeight * 2/4, \
        text = "Final Score: " + str(data.score),\
         font = "Helvetica 30 bold", fill = "white")
        canvas.create_text(data.viewWidth/2, data.viewHeight * 3/4, \
        text = "Press 's' to start again", \
        font = "Helvetica 30 bold", fill = "white")
  
    
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
        timerFired(canvas, data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
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

def playTarget():
    viewWidth = 400
    viewHeight = 400
    
    run(viewWidth, viewHeight)
    
def main():
    playTarget()

if __name__ == '__main__':
    main()
    