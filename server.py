import json
import sys
from twisted.internet.protocol import Factory
from twisted.internet.protocol import ClientFactory
from twisted.internet.protocol import Protocol
from twisted.protocols.basic import LineReceiver
from twisted.internet.tcp import Port
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue

class GameServer(object):
    def __init__(self):
        self.port1 = 40060
        self.port2 = 40061
        self.dataport1 = 41060
        self.dataport2 = 41061
        self.conn_queue = DeferredQueue()
        self.data_queue = DeferredQueue()
        self.playersConnected = 0

        self.data_array = {'p1': [], 'p2': []}
        self.data_received = {'p1': False, 'p2': False}

    def listen(self):
        reactor.listenTCP(self.port1, CConnFactory(self, 1))
        reactor.listenTCP(self.port2, CConnFactory(self, 2))
        reactor.run()

class CConn(Protocol):
	def __init__(self, addr, server, player):
		self.addr = addr
		self.server = server
		self.player = player

	def connectionMade(self):

		self.server.playersConnected += 1
		self.server.conn_queue.get().addCallback(self.tellPlayerAboutConn)
		if self.server.playersConnected == 2:
			reactor.listenTCP(self.server.data_port_1, DataConnFactory(self.server, 1))
			reactor.listenTCP(self.server.data_port_2, DataConnFactory(self.server, 2))
			self.transport.write('Make data connection')
			self.server.conn_queue.put('Make data connection')

	def tellPlayerAboutConn(self, data):
		self.transport.write(data)

class CConnFactory(Factory):
	def __init__(self, server, player):
		self.server = server
		self.player = player

	def buildProtocol(self, addr):
		return CConn(addr, self.server, self.player)

class DataConn(LineReceiver):
	def __init__(self, addr, server, player):
		self.addr = addr
		self.server = server
		self.player = 'p'+str(player)

	def lineReceived(self, line):
		"""Data received back from player"""
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
