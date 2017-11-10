from tkinter import *

#set level
def init(data):
    data.level = 1

#function to call a single teddy face
def teddyFace(canvas, xc, yc, r):
    #draw a face
    canvas.create_oval(xc-r, yc-r, xc+r, yc + r, fill = "brown", width=r/10)
    
    #draw the part around the mouse
    canvas.create_oval(xc-r/2, yc+r/3-r/2, xc+r/2,  yc+r/3+r/2, fill = "bisque", width=r/15)
    
    #draw eyes
    canvas.create_oval(xc-r/3-r/6, yc-r/3-r/6, xc-r/3+r/6,  yc-r/3+r/6, fill = "black")
    canvas.create_oval(xc+r/3-r/6, yc-r/3-r/6, xc+r/3+r/6,  yc-r/3+r/6, fill = "black")
    
    #draw a nose
    canvas.create_oval(xc-r/6, yc+r/5-r/6, xc+r/6, yc+r/5 + r/6, fill = "black")
    
    #define coordinate for arc
    #draw a mouse
    coord1 = xc-r/8-r/8, yc+r/2-r/8, xc-r/8+r/8, yc+r/2+r/8
    coord2 = xc+r/8-r/8, yc+r/2-r/8, xc+r/8+r/8, yc+r/2+r/8
    canvas.create_arc(coord1, start=180, extent=180,fill="black",style=ARC,width=r/15)
    canvas.create_arc(coord2, start=180, extent=180,fill="black",style=ARC,width=r/15)
    
    
def fractalTeddy(canvas, xc, yc, r, level):
    
    #base case
    #draw a single teddy face
    if level ==1:
        teddyFace(canvas, xc, yc, r)
    
    #recursive case
    #draw a single face and two other faces on the top right and left of 
    #original face
    else:
        teddyFace(canvas, xc, yc, r)
        fractalTeddy(canvas, xc-r*21/20, yc-r*21/20, r/2,level-1)
        fractalTeddy(canvas, xc+r*21/20, yc-r*21/20, r/2,level-1)

#define keyPressed
def keyPressed(event, data):
    #define increasing action
    if event.keysym in ["Up", "Right"]:
        data.level += 1
    #define decreasing action
    elif event.keysym in ["Down", "Left"]:
        data.level -= 1
    
#define redrawAll
def redrawAll(canvas, data):
    fractalTeddy(canvas, data.width/2, data.height/2, 100, data.level)

def mousePressed(event, data): pass

def timerFired(data): pass
        

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

run(500, 500)