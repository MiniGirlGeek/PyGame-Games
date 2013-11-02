import pygame, sys, time
from pygame.locals import *
from time import *

pygame.init()
fpsClock = pygame.time.Clock()
mouse = pygame.mouse

windowSurfaceObj = pygame.display.set_mode((640, 480))
drawingSurfaceObj = windowSurfaceObj.copy()
pygame.display.set_caption('Paintme')

catSurfaceObj = pygame.image.load('paintbrush.png')
RED = pygame.Color(255, 0, 0)
ORANGE = pygame.Color(255, 136, 0)
YELLOW = pygame.Color(255, 221, 0)
GREEN = pygame.Color(145, 255, 0)
BLUE = pygame.Color(0, 183, 255)
PURPLE = pygame.Color(198, 186, 232)
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
mousex, mousey = 0, 0

lastColorUpdate = 0
lastSizeUpdate = 0
delay = 0.1


drawingSurfaceObj.fill(WHITE)

fontObj = pygame.font.Font('freesansbold.ttf', 32)
msg = 'Click to Draw :)'
colors = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE, BLACK, WHITE]
colorNo = 0
soundObj = pygame.mixer.Sound('pen.wav')
pygame.mouse.set_visible(False)
brushColor = colors[colorNo]
brushSize = 20

def handleEvent(event):
    global msg
    
    if event.type == QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == MOUSEBUTTONDOWN:
        soundObj.play()

    elif event.type == MOUSEBUTTONUP:
        mousex, mousey = event.pos
        if event.button in (1, 2, 3):
            msg = 'Click to Draw'
            soundObj.stop()
            

    elif event.type == KEYDOWN:
        if event.key == K_c:
            drawingSurfaceObj.fill(WHITE)
        elif event.key == K_ESCAPE:
            pygame.event.post(pygame.event.Event(QUIT))
        elif event.key == K_s:
            mods = pygame.key.get_mods()
            if mods & KMOD_LCTRL:
                saveImage()


def paintSpot(mousex, mousey):
    global msg
    left_pressed, middle_pressed, right_pressed = mouse.get_pressed()
    if left_pressed and mousey > 80:
        msg = 'painting...'
        pygame.draw.circle(drawingSurfaceObj, brushColor, (mousex, mousey), brushSize, 0)

def saveImage():
    global msg
    saveSurfaceObj = pygame.Surface([640, 480])
    saveSurfaceObj.blit(drawingSurfaceObj, (0, -90))
    msgSurfaceObj = fontObj.render("Made with Paintme", False, WHITE)
    msgRectobj = msgSurfaceObj.get_rect()
    msgRectobj.topleft = (20, 400)
    saveSurfaceObj.blit(msgSurfaceObj, msgRectobj)
    pygame.image.save(saveSurfaceObj,'painting.png')
    msg = 'Saved :)'

def refreshScreen():
    global msg, colors
    pygame.draw.rect(drawingSurfaceObj, pygame.Color(153, 118, 69), (0, 0, 640, 90))
    for i in range(0, len(colors)):
        border = 6
        if i == colorNo:
            border = 0
        pygame.draw.circle(drawingSurfaceObj, colors[i], (275+(i*40), 40), 15, border)

    windowSurfaceObj.blit(drawingSurfaceObj, (0,0))
    msgSurfaceObj = fontObj.render(msg, False, BLACK)
    msgRectobj = msgSurfaceObj.get_rect()
    msgRectobj.topleft = (10, 20)
    windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)

def updateBrush():
    mousex, mousey = pygame.mouse.get_pos()
    pygame.draw.circle(windowSurfaceObj, brushColor, (mousex, mousey), brushSize, 4)
    windowSurfaceObj.blit(catSurfaceObj, (mousex, mousey))
    paintSpot(mousex, mousey)
    
def checkBrushColor():
    global brushColor, colorNo, colors, lastColorUpdate, delay

    if time() - lastColorUpdate < delay:
        return
    lastColorUpdate = time()
    
    keyPressed = pygame.key.get_pressed()
    if keyPressed[pygame.K_LEFT]:
        colorNo -= 1
    elif keyPressed[pygame.K_RIGHT]:
        colorNo += 1

    if colorNo == -1:
        colorNo = 7
    elif colorNo == 8:
        colorNo = 0
    brushColor = colors[colorNo]

    
def checkBrushSize():
    global brushSize, lastSizeUpdate, delay

    if time() - lastSizeUpdate < delay:
        return

    lastSizeUpdate = time()
    
    keyPressed = pygame.key.get_pressed()
    if keyPressed[pygame.K_UP]:
        brushSize += 5
    elif keyPressed[pygame.K_DOWN]:
        brushSize -= 5

    if brushSize > 200:
        brushSize = 200
    elif brushSize < 6:
        brushSize = 5

    
while True:
    refreshScreen()
    checkBrushColor()
    checkBrushSize()
    updateBrush()

    for event in pygame.event.get():
        handleEvent(event)

    pygame.display.update()
    fpsClock.tick(60)

    
