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
        self.x = self.centerX-self.width/2
        self.y = self.centerY-self.height/2

        #Coordonnées de l'angle en bas à droite
        self.botX = self.centerX+self.width/2
        self.botY = self.centerY+self.height/2
        
        #Epaisseur du portail
        thickness = 5
        
        if(visible == True):
            #Dans l'angle supérieur gauche, il faut enlever du rayon, dans l'angle inférieur droit, il faut en rajouter
            self.elements += [salle.create_oval(self.x,           self.y,           self.botX,           self.botY,           fill=color)]
            self.elements += [salle.create_oval(self.x+thickness, self.y+thickness, self.botX-thickness, self.botY-thickness, fill='white')]

            #Hitbox Portail
            self.elements += [salle.create_rectangle(self.x, self.y, self.botX, self.botY)]
 
            salle.tag_raise(dude.image)
            salle.tag_raise(cube.image)
       
    def delete(self):
        #Efface tous les éléments contenus dans la liste
        for obj in self.elements:
            salle.delete(obj)

"""
#--------------------------------------------------------------------------------------#
#----------------------------------CLASSE DUDE-----------------------------------------#
#--------------------------------------------------------------------------------------#
"""

class Dude():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.photo = PhotoImage(file="dude_gris.gif")
        self.image = salle.create_image(self.x, self.y, image=self.photo, anchor=NW)
        self.width = self.photo.width()
        self.height = self.photo.height()
        self.debug = 0
        self.speed = 20
        self.isFalling = False
        self.stop = True
        self.lastMove = ''

    #Mouvements
    def move(self, event):
        #Haut
        if (event.char == 'z') and (805 <= self.y+self.height):
            self.y -= self.speed
            self.lastMove = 'up'
        #Bas
        elif (event.char == 's') and (self.y+self.height <= 890):
            self.y += self.speed
            self.lastMove = 'down'
        #Gauche
        elif (event.char == 'q') and (140 <= self.x):
            self.x -= self.speed
            self.lastMove = 'left'
        #Droite
        elif (event.char == 'd') and (self.x+self.width <= 855):
            self.x += self.speed
            self.lastMove = 'right'
        #The Game Easter Egg
        elif (event.char == ' '):
            text = salle.create_text(self.x+100, self.y, text="The Game")
            self.isFalling = True
            start = time.time()
            while(self.y > -self.height):
                t = time.time() - start
                g = 0.25
                a = -g
                self.speed = a * t
                self.y = self.speed * t + self.y
                salle.coords(self.image, self.x, self.y)
                salle.coords(text, self.x+100, self.y)
                salle.update()

        #Hitbox Dude
        salle.delete(self.debug)
        self.debug = salle.create_rectangle(self.x, self.y, self.x+self.width, self.y+self.height)

        salle.coords(self.image, self.x, self.y)
        checkHitbox()

"""
#--------------------------------------------------------------------------------------#
#----------------------------------CLASSE CUBE-----------------------------------------#
#--------------------------------------------------------------------------------------#
"""      

class Cube():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.photo = PhotoImage(file="cube.gif")
        self.image = salle.create_image(self.x, self.y, image=self.photo, anchor=NW)
        self.width = self.photo.width()
        self.height = self.photo.height()
        self.speed = 20
        self.isFalling = False
        self.stop = True

    def move(self, x, y):
        if(800 <= self.y+self.height or self.y+self.height <= 890 or 140 <= self.x or self.x+self.width <= 855):
            self.x = x
            self.y = y
            salle.coords(self.image, self.x, self.y)

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
    global lastShoot, bluePortal, orangePortal, dude

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
                if(sqrt((differenceX)**2 + (differenceY)**2) < otherPortal.height-50):
                    #Si le portail vient de la droite, ajouter la différence pour le coller contre le bord droite
                    if(differenceX >= 0):
                        x += simulPortal.width - abs(differenceX)
                    #Si le portail vient de la gauche, soustraire la différence pour le coller sur le bord gauche
                    else:
                        x -= simulPortal.width - abs(differenceX)

                else:
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
            name = "dude_bleu.gif"

        elif(color == 'orange'):
            if(orangePortal != None):
                orangePortal.delete() 
            orangePortal = Portal([x, y], '#ff6600', True)
            name = "dude_orange.gif"

        dude.photo = PhotoImage(file=name)
        dude.image = salle.create_image(dude.x, dude.y, image=dude.photo, anchor=NW)
        dude.width = dude.photo.width()
        dude.height = dude.photo.height()

        salle.tag_raise(dude.image)
        
        checkHitbox()

def getHitbox(entity):
        return Rect(entity.x, entity.y, entity.width, entity.height)
        
#FIXME: Eviter que l'entité se téléporte en boucle (sera corrigé avec l'axe z)
def teleport(entity, x, y):
        entity.stop = False
        entity.x = x
        entity.y = y
        salle.coords(entity.image, entity.x, entity.y)
        salle.tag_raise(entity.image)
        #TODO: Essayer de ne plus utiliser de Thread
        if(entity.isFalling == False):
            t = threading.Thread(target=goDown, args=(entity,))
            t.start()

def goDown(entity):
        entity.isFalling = True
        start = time.time()
        while(entity.stop == False):
            t = time.time() - start
            g = 9.81
            a = g
            if entity.speed < 40: 
                entity.speed = a * t + 20
                entity.y = entity.speed * t + entity.y
            else:
                entity.y = entity.speed + entity.y
            print('Entité :',entity.__class__.__name__,'| Temps écoulé :',round(t, 2),'| Vitesse :',round(entity.speed, 2))
            salle.coords(entity.image, entity.x, entity.y)
            salle.update()
            checkHitbox()
        entity.isFalling = False
        entity.speed = 20

def checkHitbox():
    global dude, cube, bluePortal, orangePortal
    
    #Si les deux portails sont posés
    if(bluePortal != None and orangePortal != None):
        checkPortalCollision(dude)
        checkPortalCollision(cube)

    #Collisions entre le cube et le dude
    if(getHitbox(cube).perspective(getHitbox(dude))):
        if(dude.lastMove == 'up'):
            cube.move(cube.x, cube.y-dude.speed)
        elif(dude.lastMove == 'down'):
            cube.move(cube.x, cube.y+dude.speed)
        elif(dude.lastMove == 'right'):
            cube.move(cube.x+dude.speed, cube.y)
        elif(dude.lastMove == 'left'):
            cube.move(cube.x-dude.speed, cube.y)

    if(dude.y+dude.height > cube.y+cube.height):
        salle.tag_raise(dude.image)
    elif(dude.y+dude.height < cube.y+cube.height):
        salle.tag_raise(cube.image)
    
def checkPortalCollision(entity):
    #Si l'entité a atteint le sol alors on check les portails
    if(entity.y+entity.height >= 780):
        #Si l'entité passe par le portail bleu
        if(getHitbox(bluePortal).intersects(getHitbox(entity))):
            teleport(entity, orangePortal.centerX, orangePortal.centerY)
        #Si l'entité passe par le portail orange
        elif(getHitbox(orangePortal).intersects(getHitbox(entity))):
            teleport(entity, bluePortal.centerX, bluePortal.centerY)
        else:
            #L'entité n'est pas téléporté et a atteint le sol, on arrête de la faire tomber
            entity.stop = True
    
frameW = 1000
frameH = 900

frame = Tk()
frame.title("Pyrtal")

salle = Canvas(frame, width=frameW, height=frameH)

bluePortal = None
orangePortal = None

#TODO: faire une vraie salle avec de vrais murs (collisions)

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

dude = Dude(450, 700)
cube= Cube(300, 800)

#Configure les touches souris / clavier
salle.bind("<Button-1>", lambda event: createPortal(event, 'blue'))
salle.bind("<Button-3>", lambda event: createPortal(event, 'orange'))
salle.bind("<KeyPress>", dude.move)

chaine = Label(frame)
chaine.pack()
salle.pack()

frame.mainloop()
