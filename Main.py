# Portal Main #

from tkinter import *
from math import *

def createPortal(mouse, color):
    #Logs are love, Logs are life. #oui
    chaine.configure(text = "Click spotted in X =" + str(mouse.x) +", Y =" + str(mouse.y))
    
    portal = []

    #Roof or floor, lying portal
    if(mouse.y < 125 or mouse.y > 875):
        portal += [salle.create_oval(mouse.x-150, mouse.y-50, mouse.x+150, mouse.y+50, fill=color)]
        portal += [salle.create_oval(mouse.x-145, mouse.y-45, mouse.x+145, mouse.y+45, fill='white')]
    else:
        portal += [salle.create_oval(mouse.x-50, mouse.y-150, mouse.x+50, mouse.y+150, fill=color)]
        portal += [salle.create_oval(mouse.x-45, mouse.y-145, mouse.x+45, mouse.y+145, fill='white')]

    return portal
    
#Blue portal
def bluePortal(event):
    global bluePortalElements
    delete(bluePortalElements)   
    bluePortalElements = createPortal(event, '#6699ff')

#Orange Portal   
def orangePortal(event):
    global orangePortalElements
    delete(orangePortalElements)  
    orangePortalElements = createPortal(event, '#ff6600')

#Moving fuctions
def move_left(event): 
    move(-20, 0) 
def move_right(event): 
    move(20, 0) 
def move_up(event): 
    move(0, -20) 
def move_down(event): 
    move(0, 20)

def move(moveX, moveY): 
    global x, y, oval
    x += moveX
    y += moveY
    salle.delete(oval)
    oval = salle.create_rectangle(x, y, x+30, y+30, width=2, fill='orange') 
    
def delete(elements):
    #Undraw all objects containing by elements array
    for obj in elements:
        salle.delete(obj)
    #Reset elements array
    elements = []

bluePortalElements = []
orangePortalElements = []

frameW = 1000
frameH = 1000
#Dude coordinate
x = 500
y = 900

frame = Tk()
frame.title("Portal")

salle = Canvas(frame, width=frameW, height=frameH)

# Fond de salle #
salle.create_rectangle(125,875,875,125)

# Profondeur  #
salle.create_line([0, 1000, 125, 875])
salle.create_line([1000, 1000, 875, 875])                                                       
salle.create_line([1000, 0, 875, 125])
salle.create_line([0, 0, 125, 125])

#Set focus to catch mouse and keyboard input
salle.focus_set()

# Binding mouse #
salle.bind("<Button-1>", bluePortal)
salle.bind("<Button-3>", orangePortal)

# Binding Keyboard #
salle.bind("<Up>", move_up)
salle.bind("<Left>", move_left)
salle.bind("<Down>", move_down)
salle.bind("<Right>", move_right)

oval = salle.create_rectangle(x, y, x+30,y+30, width=2, fill='orange')

chaine = Label(frame)
chaine.pack()
salle.pack()

frame.mainloop()
