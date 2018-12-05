import json
import sys
import time
import signal

from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet.tcp import Port
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue


class bomberguy():
    def __init__(self,x,y):
        super().__init__()

       
        self.x = x
        self.y = y
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
   
    def moveRight(self, pixels):
        self.x += pixels
    def moveLeft(self, pixels):
        self.x -= pixels
    def moveUp(self, pixels):
        self.y -= pixels
    def moveDown(self, pixels):
        self.y += pixels

class bomb():
    def __init__(self,x,y):
        super().__init__()

        self.x = x
        self.y = y

class Brick():
    def __init__(self,x,y):
        super().__init__()

        self.x = x
        self.y = y

player = bomberguy(40,40)
def moveplayer(button):
    if(button == "up"):
        player.moveUp(30)
    if(button == "left"):
        player.moveLeft(30)
    if(button == "down"):
        player.moveDown(30)
    else:
        return





class GameServer(object):
    def __init__(self):
        self.port1 = 40060
        self.dataport = 41060
        #self.conn_queue = DeferredQueue()
        self.data_queue = DeferredQueue()
        self.playersConnected = 0
        self.playerCount = 0
        self.lastSent = 0

        self.data_array = {}
        self.data_received = {}

    def listen(self):
        print("Server Started.")
        reactor.listenTCP(self.port1, CConnFactory(self))
        reactor.run()

    def sendAll(self):
        if all(self.data_received.values()):
            print(self.data_array)
            #    print("Data sent to p"+str(i+1))
            elapsed = time.time()-self.lastSent
            if(elapsed < 2):
                reactor.callLater(2.1 - elapsed, self.sendAll)
            else:
                for i in range(self.playersConnected):
                    self.data_queue.put(['update',self.data_array])
                self.lastSent = time.time()

class CConnFactory(Factory):
    def __init__(self, server):
        self.server = server        
        
    def buildProtocol(self, addr):
        return CConn(addr, self.server)
    
class CConn(Protocol):
    def __init__(self, addr, server):
        self.addr = addr
        self.server = server
        self.server.playersConnected += 1
        self.player = server.playersConnected
        
    def connectionMade(self):
        print("Got new client!")
        server.data_array[self.player]=[]
        server.data_received[self.player]=False

        self.transport.write(json.dumps(('connected',None)).encode())
        #self.transport.write(b'update')

        #self.server.conn_queue.get().addCallback(self.tellPlayerAboutConn)
        #if self.server.playersConnected == 2:
        #    reactor.listenTCP(self.server.dataport1, DataConnFactory(self.server, 1))
        #    reactor.listenTCP(self.server.dataport2, DataConnFactory(self.server, 2))
        #    self.transport.write('Make data connection')
        #    self.server.conn_queue.put('Make data connection')

    def dataReceived(self,data):
        if not self.server.data_received[self.player]:
            self.server.data_array[self.player] = json.loads(data)
            self.server.data_received[self.player] = True
            self.server.data_queue.get().addCallback(self.sendToPlayer)
            self.server.sendAll()
                

    def sendToPlayer(self, data):
        #print 'Sending array to both players'
        print("Data sent to p"+str(self.player))
        self.transport.write(json.dumps(data).encode())
        self.server.data_received[self.player] = False
        return data

    def connectionLost(self, reason):
        print("Lost a client!")
        self.server.data_array.pop(self.player)
        self.server.data_received.pop(self.player)
        self.server.playersConnected-=1
        #self.factory.clients.remove(self)



class DataFactory(Factory):
    def __init__(self, server, player):
        self.server = server
        self.player = player

    def buildProtocol(self, addr):
        return DataConn(addr, self.server, self.player)

class DataConn(LineReceiver):
    def __init__(self, addr, server, player):
        self.addr = addr
        self.server = server
        self.player = 'p'+str(player)

    def lineReceived(self, line):
        #"""Data received back from player"""
        #print 'Received data from', self.player, line
        self.server.data_array[self.player] = json.loads(line)
        self.server.data_received[self.player] = True
        if self.server.data_received['p1'] == self.server.data_received['p2'] == True:
            self.sendToPlayer(self.server.data_array)
            self.server.data_queue.put(self.server.data_array)
        else:
            self.server.data_queue.get().addCallback(self.sendToPlayer)

    def sendToPlayer(self, data):
        #print 'Sending array to both players'
        self.sendLine(json.dumps(data))
        self.server.data_received[self.player] = False


if __name__ == '__main__':
	server = GameServer()
	server.listen()


