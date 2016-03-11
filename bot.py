import re
import socket
import sys
import time
import threading

class Bot(threading.Thread):
	def __init__(self, channel, nickname, password):
		super(Bot, self).__init__()
		self.__channel = channel
		self.__message = ""

		self.__con = socket.socket()
		self.__con.connect(('irc.twitch.tv', 6667))

		self.sendPass(password)
		self.sendNick(nickname)
		self.joinChannel(channel)

	def run(self):
		data = ""
		while (True):
			try:
				data = data+self.__con.recv(1024).decode('UTF-8')	
				data_split = re.split(r"[~\r\n]+", data)
				data = data_split.pop()
				for line in data_split:
					line = str.rstrip(line)
					line = str.split(line)
					if len(line) >= 1:
						if line[0] == 'PING':
							self.sendPong(line[1])

			except socket.error:
				print ("Socket error.")
				sys.exit()
			except socket.timeout:
				print ("Socket timeout.")
				sys.exit()

	def sendPong(self, message):
		self.__con.send(bytes('PONG %s\r\n' % message, 'UTF-8'))

	def sendMessage(self, message):
		self.__con.send(bytes('PRIVMSG %s :%s\r\n' % (self.__channel, message), 'UTF-8'))
		
	def sendNick(self, nickname):
		self.__con.send(bytes('NICK %s\r\n' % nickname, 'UTF-8'))
	
	def sendPass(self, password):
		self.__con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))
	
	def joinChannel(self, channel):
		self.__con.send(bytes('JOIN %s\r\n' % channel, 'UTF-8'))

	def partChannel(self, channel):
		self.__con.send(bytes('PART %s\r\n' % channel, 'UTF-8'))
