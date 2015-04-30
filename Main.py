from tkinter import *
from math import *
from rectangle import *
import time
import threading

"""
#--------------------------------------------------------------------------------------#
#---------------------------------CLASSE PORTAL----------------------------------------#
#--------------------------------------------------------------------------------------#
"""

class Portal():
    def __init__(self, positions, color, visible):
        self.centerX = positions[0]
        self.centerY = positions[1]
        self.elements = []
        
        #Sol & Plafond : Portail horizontal
        if(self.centerY < 125 or self.centerY > 788):
            self.width = 300
            self.height = 110
        else:
            self.width = 110
            self.height = 300

        #Coordonnées de l'angle en haut à gauche
        self.topX = self.centerX-self.width/2
        self.topY = self.centerY-self.height/2

        #Coordonnées de l'angle en bas à droite
        self.botX = self.centerX+self.width/2
        self.botY = self.centerY+self.height/2
        
        #Epaisseur du portail
        thickness = 5
        
        if(visible == True):
            #Dans l'angle supérieur gauche, il faut enlever du rayon, dans l'angle inférieur droit, il faut en rajouter
            self.elements += [salle.create_oval(self.topX,           self.topY,           self.botX,           self.botY,           fill=color)]
            self.elements += [salle.create_oval(self.topX+thickness, self.topY+thickness, self.botX-thickness, self.botY-thickness, fill='white')]

            #Hitbox Portail
            self.elements += [salle.create_rectangle(self.topX, self.topY, self.botX, self.botY)]
 
            dude.firstPlan()
       
    def delete(self):
        #Efface tous les éléments contenus dans la liste
        for obj in self.elements:
            salle.delete(obj)

    def getHitbox(self):
        return Rect(self.topX, self.topY, self.width, self.height)

"""
#--------------------------------------------------------------------------------------#
#----------------------------------CLASSE DUDE-----------------------------------------#
#--------------------------------------------------------------------------------------#
"""

class Dude():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.photo = PhotoImage(file="Dude_sans_bras.gif")
        self.image = salle.create_image(self.x, self.y, image=self.photo, anchor=NW)
        self.width = self.photo.width()
        self.height = self.photo.height()
        self.isFalling = False
        self.debug = 0
        self.speed = 20

    #Mouvements
    def move(self, event):
        #Haut
        if (event.char == 'z') and (800 <= self.y+self.height):
            self.y -= self.speed
        #Bas
        elif (event.char == 's') and (self.y+self.height <= 890):
            self.y += self.speed
        #Gauche
        elif (event.char == 'q') and (140 <= self.x):
            self.x -= self.speed
        #Droite
        elif (event.char == 'd') and (self.x+self.width <= 855):
            self.x += self.speed
        #The Game Easter Egg
        elif (event.char == ' '):
            text = salle.create_text(self.x+100, self.y, text="The Game")
            while self.y > -100:
                self.y -= 1
                time.sleep(0.01)
                salle.coords(self.image, self.x, self.y)
                salle.coords(text, self.x+100, self.y)
                salle.update()

        #Hitbox Dude
        salle.delete(self.debug)
        self.debug = salle.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height)

        salle.coords(self.image, self.x, self.y)
        checkHitbox()

    def goDown(self):
        dude.isFalling = True
        start = time.time()
        while(self.y+self.height <= 800):
            #y(t)=1/2gt²
            self.y += 1/2  * 9.81 * (time.time() - start)**2
            salle.coords(self.image, self.x, self.y)
            salle.update()
            time.sleep(0.01)
        dude.isFalling = False
        checkHitbox()

    def firstPlan(self):
        salle.delete(self.image)
        self.image = salle.create_image(self.x, self.y, image=self.photo, anchor=NW)
        salle.update()

    def teleport(self, x, y):
        self.x = x
        self.y = y
        salle.coords(self.image, self.x, self.y)
        self.firstPlan()
        self.goDown()

    def getHitbox(self):
        return Rect(self.x, self.y, self.width, self.height)

"""
#--------------------------------------------------------------------------------------#
#----------------------------------CLASSE CUBE-----------------------------------------#
#--------------------------------------------------------------------------------------#
"""      

class Cube():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.photo = PhotoImage(file="Cube.gif")
        self.width = self.photo.width()
        self.height = self.photo.height()
        self.image = salle.create_image(self.x, self.y, image = self.photo, anchor=NW)
        self.isFalling = False

    def goDown(self):
        self.isFalling = True
        start = time.time()
        while(self.y+self.height <= 800):
            #y(t)=1/2gt²
            self.y += 1/2 * 9.81 * (time.time() - start)**2
            salle.coords(self.image, self.x, self.y)
            salle.update()
            time.sleep(0.01)
        self.isFalling = False
        checkHitbox()

    def firstPlan(self):
        salle.delete(self.image)
        self.image = salle.create_image(self.x, self.y, image=self.photo, anchor=NW)
        salle.update()

    def teleport(self, x, y):
        self.x = x
        self.y = y
        salle.coords(self.image, self.x, self.y)
        self.firstPlan()
        t = threading.Thread(target=self.goDown)
        t.start()

    def getHitbox(self):
        return Rect(self.x, self.y, self.width, self.height)

    def getHitboxL(self):
        return Rect(self.x, self.y, self.width/4, self.height)

    def getHitboxR(self):
        return Rect(self.x+(self.width-self.width/4), self.y, self.width/4, self.height)

    def getHitboxU(self):
        return Rect(self.x, self.y, self.width, self.height-self.height/3)
    
    def getHitboxD(self):
        return Rect(self.x+self.height/2, self.y-self.width/2, self.width/4, self.height)
    
    def move(self, x, y):
        self.x = x
        self.y = y
        salle.coords(self.image, self.x, self.y)

"""
#--------------------------------------------------------------------------------------#
#----------------------------------CLASSE GUN------------------------------------------#
#--------------------------------------------------------------------------------------#
"""

class Gun():        
    def __init__(self, x, y, name):
        self.element = 0
        self.x = x
        self.y = y
        self.photo = PhotoImage(file=name)
        self.image = salle.create_image(self.x, self.y, image=self.photo, anchor=SW)
        self.width = self.photo.width()
        self.height = self.photo.height()
    """
    def rotate(self, event):
        salle.delete(self.element)
        self.element = salle.create_line(dude.x+dude.width/2, dude.y+dude.height/3, event.x, event.y)
    """

"""
#--------------------------------------------------------------------------------------#
#----------------------------------------MAIN------------------------------------------#
#--------------------------------------------------------------------------------------#
"""

#Heure et temps de recharge en seconde
lastShoot = time.time()
reloadingTime = 0.1

#Créer un Portail
def createPortal(event, color):
    global lastShoot, bluePortal, orangePortal, gun

    if(time.time() - lastShoot > reloadingTime):
        lastShoot = time.time()

        x = event.x
        y = event.y

        if(color == 'blue'):
            portal = bluePortal
            otherPortal = orangePortal
        elif(color == 'orange'):
            portal = orangePortal
            otherPortal = bluePortal

        #Vérifie si le portail qui va être créé n'est pas posé par dessus le deuxième
        if(otherPortal != None):
            #Créé un faux portail pour voir s'il peut être posé 
            simulPortal = Portal([x, y], color, False)

            #Distance entre le centreX des deux portails
            differenceX = simulPortal.centerX - otherPortal.centerX
            #Distance entre le centreY des deux portails
            differenceY = simulPortal.centerY - otherPortal.centerY
            
            if(abs(differenceX) < otherPortal.width and abs(differenceY) < otherPortal.height):
                
                #Si le portail vient de la droite, ajouter la différence pour le coller contre le bord droite
                if(differenceX >= 0):
                    x += simulPortal.width - abs(differenceX)
                #Si le portail vient de la gauche, soustraire la différence pour le coller sur le bord gauche
                else:
                    x -= simulPortal.width - abs(differenceX)
                    
            elif(abs(differenceX) < otherPortal.width and abs(differenceY) < otherPortal.height and abs(differenceY) > abs(differenceX)):
                
                #Si le portail vient de la droite, ajouter la différence pour le coller contre le bord droite
                if(differenceY >= 0):
                    y += simulPortal.height - abs(differenceY)
                #Si le portail vient de la gauche, soustraire la différence pour le coller sur le bord gauche
                else:
                    y -= simulPortal.height - abs(differenceY)

        if(color == 'blue'):
            #Si le portail avait déjà été posé, l'effacer
            if(bluePortal != None):
                bluePortal.delete()
            bluePortal = Portal([x, y], '#6699ff', True)
            gun = Gun(500, 500, "PGunB.gif")

        elif(color == 'orange'):
            if(orangePortal != None):
                orangePortal.delete() 
            orangePortal = Portal([x, y], '#ff6600', True)
            gun = Gun(500, 500, "PGunO.gif")

        checkHitbox()

def checkHitbox():
    global dude, bluePortal, orangePortal
    
    #Si les deux portails sont posés
    if(bluePortal != None and orangePortal != None):

        if(dude.isFalling == False):
            #Si le dude passe par le portail bleu
            if(bluePortal.getHitbox().intersects(dude.getHitbox())):
                dude.teleport(orangePortal.centerX, orangePortal.centerY)
            #Si le dude passe par le portail orange
            elif(orangePortal.getHitbox().intersects(dude.getHitbox())):
                dude.teleport(bluePortal.centerX, bluePortal.centerY)

        if(cube.isFalling == False):
            #Si le cube passe par le portail bleu
            if(bluePortal.getHitbox().intersects(cube.getHitbox())):
                cube.teleport(orangePortal.centerX, orangePortal.centerY)
            #Si le cube passe par le portail orange
            elif(orangePortal.getHitbox().intersects(cube.getHitbox())):
                cube.teleport(bluePortal.centerX, bluePortal.centerY)

    #Collisions entre le cube et le dude
    if(cube.getHitboxL().intersects(dude.getHitbox())):
        cube.move(cube.x+dude.speed, cube.y)
    if(cube.getHitboxR().intersects(dude.getHitbox())):
        cube.move(cube.x-dude.speed, cube.y)
    if(cube.getHitboxU().intersects(dude.getHitbox())):
        cube.move(cube.x, cube.y-dude.speed )
    if(cube.getHitboxD().intersects(dude.getHitbox())):
        cube.move(cube.x, cube.y+dude.speed)
    
frameW = 1000
frameH = 900

frame = Tk()
frame.title("Pyrtal")

salle = Canvas(frame, width=frameW, height=frameH)

dude = Dude(450, 700)
gun = Gun(500, 500, "PGunI.gif")
cube= Cube(300, 800)

bluePortal = None
orangePortal = None

#Fond de la salle
salle.create_rectangle(125,788,875,112)

"""Effet de profondeur (lignes diagonales)"""
#Bas gauche
salle.create_line(0, frameH, 125, 788)
#Bas droit
salle.create_line(frameW, frameH, 875, 788)
#Haut droit
salle.create_line(frameW, 0, 875, 112)
#Haut gauche
salle.create_line(0, 0, 125, 112)

#Focus sur la fenêtre pour pouvoir recevoir les clics de souris et l'appuie de touches
salle.focus_set()

#Configure les touches souris / clavier
salle.bind("<Button-1>", lambda event: createPortal(event, 'blue'))
salle.bind("<Button-3>", lambda event: createPortal(event, 'orange'))
salle.bind("<KeyPress>", dude.move)
#salle.bind("<Motion>", gun.rotate)

chaine = Label(frame)
chaine.pack()
salle.pack()

frame.mainloop()
