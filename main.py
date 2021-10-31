import pygame
import random
import math

lengde = 2000 #vindu x akse
bredde = 1200 #vindu y akse

win = pygame.display.set_mode((lengde,bredde), pygame.RESIZABLE)

pygame.display.set_caption("Planet visualisajson")

class dot:
    def __init__(self, xpos, ypos, radius, xFart, yFart):
        self.xpos = xpos
        self.ypos = ypos
        self.radius = radius
        self.xFart = xFart
        self.yFart = yFart
    def tegn(self):
        pygame.draw.circle(win, (255,255,255), (int(self.xpos),int(self.ypos)), int(self.radius))


def tegnDotter():
    
    for dot in dotter:
        dot.xpos += dot.xFart
        dot.ypos += dot.yFart

        if dot.xpos > lengde:
            dot.xpos -= lengde
        if dot.ypos > bredde:
            dot.ypos -= bredde
        if dot.xpos < 0:
            dot.xpos += lengde
        if dot.ypos < 0:
            dot.ypos += bredde
        dot.tegn()
        
def kollisjon():
    sammenslaainger = []
    for i in range(len(dotter)):
        for j in range(i+1, len(dotter)):
            avstand = math.sqrt((dotter[i].xpos - dotter[j].xpos)**2 + (dotter[i].ypos - dotter[j].ypos)**2)
            if avstand <= (dotter[i].radius + dotter[j].radius):
                sammenslaainger.append([dotter[i], dotter[j]])
    
    for par in sammenslaainger:
        volum0 = math.pi*(par[0].radius)**2
        volum1 = math.pi*(par[1].radius)**2 
        if volum0 < volum1:
            par[1].radius = math.sqrt((volum0 + volum1)/math.pi)
            par[1].xFart = ((volum1/(volum0+volum1))*par[1].xFart + (volum0/(volum0+volum1))*par[0].xFart)/2
            par[1].yFart = ((volum1/(volum0+volum1))*par[1].yFart + (volum0/(volum0+volum1))*par[0].yFart)/2
            dotter.remove(par[0])
        else:
            par[0].radius = math.sqrt((volum0 + volum1)/math.pi)
            par[0].xFart = ((volum1/(volum0+volum1))*par[1].xFart + (volum0/(volum0+volum1))*par[0].xFart)/2
            par[0].yFart = ((volum1/(volum0+volum1))*par[1].yFart + (volum0/(volum0+volum1))*par[0].yFart)/2
            dotter.remove(par[1])


def gravitasjon():
    for dot in dotter:
        for motdot in dotter:
            if dot != motdot:
                xAvstand = (motdot.xpos - dot.xpos)
                yAvstand = (motdot.ypos - dot.ypos)
                verdiX = xAvstand/(abs(xAvstand)+abs(yAvstand))
                verdiY = yAvstand/(abs(xAvstand)+abs(yAvstand))
                #avstand = (math.sqrt((motdot.xpos - dot.xpos)**2 + (motdot.ypos - dot.ypos)**2) - ((dot.radius+motdot.radius)/2))
                avstand = (math.sqrt((motdot.xpos - dot.xpos)**2 + (motdot.ypos - dot.ypos)**2))
                maxAvstand = math.sqrt((bredde)**2 + (lengde)**2)
                omvendtAvstand = (maxAvstand-avstand)
                avstandkraft = (omvendtAvstand/maxAvstand)**(24)

                storrelseForhold = ((math.pi*(motdot.radius**2))/(math.pi*(dot.radius**2)))
                kraft = storrelseForhold*avstandkraft

                endringX = verdiX*kraft
                endringY = verdiY*kraft


                dot.xFart += endringX/40
                dot.yFart += endringY/40




running = True
dotter = []

dotter.append(dot(900,600,30, 0, 0))

for i in range(50):
    f = 3
    retning = random.randint(0,360)
    x = random.randint(0,lengde)
    y = random.randint(0,bredde)
    fartX = round(random.uniform(-f, f), 2)
    fartY = round(random.uniform(-f, f), 2)
    storrelse = random.randint(2, 5)
    dotter.append(dot(x,y,storrelse, fartX,fartY))

while running:
    win.fill((50,50,50))
    clock = pygame.time.Clock()
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.VIDEORESIZE:
            sreen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            lengde = event.w
            bredde = event.h
    
    keys = pygame.key.get_pressed()
    kollisjon()
    gravitasjon()
    tegnDotter()
    pygame.display.update()
    
