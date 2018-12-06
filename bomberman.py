import sys
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
flag = 'true'

import json

try:
    import pygame
    pygame.init()
except:
    print("----<error>-----\nSomething wrong with pygame\nPlz run with Python 3 and make sure pygame is installed")
    input()
    exit()
a = False
b = False
try:
    import random
    a = True
    import time
    b = True
except:
    print("----<error>-----\nProblem with imported modules\nModules|Imported\nrandom |"+str(a)+"\ntime   |"+str(b)+"\nPlease fix")


def keyd():
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            return "up"
        if pressed[pygame.K_RIGHT]:
            return "right"
        if pressed[pygame.K_DOWN]:
            return "down"      
        if pressed[pygame.K_LEFT]:
            return "left"       
        if pressed[pygame.K_SPACE]:
            return "space"
            



# client networking
class DataConn(Protocol):
    """Once connected, send a message, then print the result."""    
    def connectionMade(self):
        #self.transport.write(b"hello, world!")
        pass

    def dataReceived(self, data):
        #print("Server said:", data)
        action, data = json.loads(data.decode())
        print(action)
        if (action=='connected' or action=='update'):
            clientInfo={
                'x':player1.rect.x,
                'y':player1.rect.y,
            }
            self.transport.write(json.dumps(clientInfo).encode())
        else:
            print(d)
    
    def connectionLost(self, reason):
        print("connection lost")

class DataConnFactory(ClientFactory):
    #def __init__(self, server, player):
    #	self.server = server
    #	self.player = player

    protocol = DataConn
    def clientConnectionFailed(self, connector, reason):
        print("Connection failed - goodbye!")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost - goodbye!")
        reactor.stop()


class bomberguy(pygame.sprite.Sprite):

    def __init__(self,x,y):
        super().__init__()
        self.currentbomb = 1
        self.maxbomb = 1
        self.image = pygame.image.load("Bomberman.gif").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def get_x(self):
        return self.rect.x
    def get_y(self):
        return self.rect.y
    def moveRight(self, pixels):
        self.rect.x += pixels
    def moveLeft(self, pixels):
        self.rect.x -= pixels
    def moveUp(self, pixels):
        self.rect.y -= pixels
    def moveDown(self, pixels):
        self.rect.y += pixels
        #pygame.draw.rect(self.image, [0,0,18,22])

class bomb(pygame.sprite.Sprite):


    def __init__(self,x,y):
        super().__init__()
        self.fuse = 50
        self.triggered = False
        self.image = pygame.image.load("Bomb.gif").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer =  pygame.time.get_ticks()
    def tick(self):
        self.fuse -= 1
        return self.fuse
    def explode(self):
        self.bomberguy.currentbomb += 1

class exbomb(pygame.sprite.Sprite):


    def __init__(self,x,y):
        super().__init__()
        self.fuse = 10
        self.triggered = False
        self.image = pygame.image.load("Bomb2.gif").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer = pygame.time.get_ticks()
    def tick(self):
        self.fuse -= 1
        return self.fuse
    def explode(self):
        self.bomberguy.currentbomb += 1

class Brick(pygame.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()

        self.image = pygame.image.load("Brick.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y




class vr:
    #grid width
    gw = 15
    #grid height
    gh = 15
    #square size
    pxl = 32
    #screen width
    sw = 0
    #screen height
    sh = 0
    #wall loop
    wl = False
    #points
    points = 0
    #color offset
    coloroffset = 8
    #is the game over
    done = False

class gamef:
 

    def CheckBomb():
        #print ("here")
        for bomb in bombs:
            if bomb.tick() < 0:
                player1.currentbomb -= 1
                nexbomb = exbomb(bomb.rect.x,bomb.rect.y)
                exbombs.append(nexbomb)
                all_sprites_list.add(exbombs)
                bombs.remove(bomb)
                all_sprites_list.remove(bomb)
        for wexbomb in exbombs:
            if wexbomb.tick() < 0:
                exbombs.remove(wexbomb)
                all_sprites_list.remove(wexbomb)
                

    def activateBomb(self,bomb):
        if not bomb.triggered:
            bomb.explode()
            self.bombs.remove(bomb)
            explosion = pygame.image.load("bomb2.gif")

    # just for testing the bomb
    def keyd():
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            player1.moveUp(32)
        if pressed[pygame.K_RIGHT]:
            player1.moveRight(32)
        if pressed[pygame.K_DOWN]:
            player1.moveDown(32)
        if pressed[pygame.K_LEFT]:
            player1.moveLeft(32)
        if pressed[pygame.K_SPACE]:
            if (player1.maxbomb >= player1.currentbomb):
                nbomb = bomb(player1.get_x(),player1.get_y())
                bombs.append(nbomb)
                all_sprites_list.add(bombs)
                player1.currentbomb += 1

    def grid():
        ty = False
        for x in range(int(vr.sw/vr.pxl)):
            for y in range(int(vr.sh/vr.pxl)):
                of = 0
                if (y%2)==0:
                    of = 1
                if (((x+of)%2)==0):
                    pygame.draw.rect(screen, (32,32,32),pygame.Rect(x*vr.pxl,y*vr.pxl,vr.pxl,vr.pxl))

                else:
                    pygame.draw.rect(screen, (64,64,64),pygame.Rect(x*vr.pxl,y*vr.pxl,vr.pxl,vr.pxl))
                ty = not ty
    def draw():
        #Framerate of 10
        pygame.draw.rect(screen, (8,8,8),pygame.Rect(0,0,vr.pxl,vr.sh))
        pygame.draw.rect(screen, (8,8,8),pygame.Rect(vr.sw-vr.pxl,0,vr.pxl,vr.sh))
        pygame.draw.rect(screen, (8,8,8),pygame.Rect(0,0,vr.sw,vr.pxl))
        pygame.draw.rect(screen, (8,8,8),pygame.Rect(0,vr.sh-vr.pxl,vr.sw,vr.pxl))
        color=(0,255,0)
        col = 0
        os = vr.coloroffset
        color=(0,0,192)
        #pygame.draw.rect(screen, color, pygame.Rect(vr.pxl*snake.x,vr.pxl*snake.y, vr.pxl, vr.pxl))
        all_sprites_list.draw(screen)


def gameLoop():
    global c
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            vr.done = True
            exit()
            quit()
    
    gamef.grid()
    if(c > 5):
        gamef.keyd()
        c = 0
    c+=1
    gamef.draw()
    gamef.CheckBomb()
    pygame.display.flip()

    #clock.tick(100)


vr.sw = vr.gw*vr.pxl
vr.sh = vr.gh*vr.pxl
#setup
clock = pygame.time.Clock()
screen = pygame.display.set_mode((vr.sw, vr.sh))
pygame.display.set_caption("Bomberman")
#pressed = pygame.key.get_pressed()
global player1
player1 = bomberguy(40,40)
brick1 = Brick(64,64)
global all_sprites_list
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player1)
all_sprites_list.add(brick1)

c = 0
exbombs = []
bombs = []    
reactor.connectTCP("localhost",40060,DataConnFactory())
LoopingCall(gameLoop).start(1/100)
reactor.run()
gameLoop()
pygame.quit()


