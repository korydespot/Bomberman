import sys
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.internet import reactor
from twisted.internet.task import LoopingCall

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

# client networking
class DataConn(Protocol):
    """Once connected, send a message, then print the result."""    
    def connectionMade(self):
        #self.transport.write(b"hello, world!")
        pass
    
    def dataReceived(self, data):
        #print("Server said:", data)
        d = data.decode()
        if (d=='update'):
            clientInfo={
                'x':player1.rect.x,
                'y':player1.rect.y,
            }
            self.transport.write(json.dumps(clientInfo).encode())
    
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

        self.image = pygame.image.load("Bomb.gif").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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

class snake:
    ##x first then y
    leng = 4
    x = random.randint(1,vr.gw-2)
    y = random.randint(1,vr.gh-2)
    dire = 5
    speed = 1
    tailx = []
    taily = []
    deaths = 0

class gamef:
    def __init__(self):
        bombs = []

    def death():
        snake.leng = 4
        snake.x = random.randint(1,vr.gw-2)
        snake.y = random.randint(1,vr.gh-2)
        snake.dire = 5
        snake.speed = 10
        snake.tailx = []
        snake.taily = []
        snake.deaths +=1
        time.sleep(0.5)
        snake.dire = 5

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
            bombs.append(bomb(player1.get_x(),player1.get_y()))
            all_sprites_list.add(bombs)
    def ref():
        gamef.tails()
        if (snake.dire == 0):
            gamef.move(0,-1)
            #snake.y -=1
        elif (snake.dire == 1):
            gamef.move(1,0)
            #snake.x+=1
        elif (snake.dire == 2):
            #snake.y+=1
            gamef.move(0,1)
        elif (snake.dire == 3):
            gamef.move(-1,0)
            #snake.x-=1
    def move(x,y):
        #x check
        if (snake.x+x)>= vr.gw-1:
            if(vr.wl):
                snake.x = 1;
            else:
                gamef.death()
            #print ("out of bounds")
            
        elif(snake.x+x)<= 0:
            #print ("out of bounds")
            if(vr.wl):
                snake.x = vr.gw-2;
            else:
                gamef.death()
            
        else:
            snake.x+=x
        #y check
        if (snake.y+y)>= vr.gh-1:
            #print ("out of bounds")
            if(vr.wl):
                snake.y = 1
            else:
                gamef.death()
        elif(snake.y+y)<= 0:
            #print ("out of bounds")
            if(vr.wl):
                snake.y = vr.gh-2
            else:
                gamef.death()
            
        else:
            snake.y+=y
        #apple
        if (snake.x == apple.x) and (snake.y == apple.y):
            snake.leng+=1
            apple.lvl+=1
            apple.x = random.randint(1,vr.gw-2)
            apple.y = random.randint(1,vr.gh-2)
            #print("Apple pos:\nX - "+str(apple.x)+"\nY - "+str(apple.y))
        cdeaths = snake.deaths;
        for i in range(len(snake.tailx)):
            if(snake.deaths == cdeaths):
                if (snake.x == snake.tailx[i]):
                     if (snake.y == snake.taily[i]):
                         #print("game over")
                         gamef.death();
    def tails():
        snake.tailx.append(snake.x)
        snake.taily.append(snake.y)
        if (len(snake.tailx) > snake.leng):
            snake.tailx.pop(0)
            snake.taily.pop(0)

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
    if (c >= (1000/snake.speed)):
        gamef.ref()
        c=0
        #snake.speed+=1
    pygame.display.flip()

    #clock.tick(100)


vr.sw = vr.gw*vr.pxl
vr.sh = vr.gh*vr.pxl
#setup
clock = pygame.time.Clock()
screen = pygame.display.set_mode((vr.sw, vr.sh))
pygame.display.set_caption("Bomberman")
#pressed = pygame.key.get_pressed()

player1 = bomberguy(40,40)
brick1 = Brick(64,64)
all_sprites_list = pygame.sprite.Group()
all_sprites_list.add(player1)
all_sprites_list.add(brick1)

c = 0
bombs = []    

reactor.connectTCP("localhost",40060,DataConnFactory())
LoopingCall(gameLoop).start(1/100)
reactor.run()
pygame.quit()
