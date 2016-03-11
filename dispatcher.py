"""
Proof of concept. Can be considerably improved.
"""
import argparse
from bot import Bot
import collections, itertools, threading
from utilities import timeMillis, wait

def consume(iterator, n):
	collections.deque(itertools.islice(iterator, n))

"""
In users.txt every user is of the form:
username1
	Pass: 'password'
	oauth:...

username2
	Pass: 'password'
	oauth:...

... and so on
"""
def readInUsers(stream, file='users.txt'):
	bots = []
	with open(file) as f:
		content = f.readlines()
		content = [line.rstrip() for line in content]
		iterator = iter(range(0, len(content)))
		for i in iterator:
			username = content[i].lower()
			oauth = content[i+2].strip('\t\n')
			consume(iterator, 3)
			bots.append(Bot(stream, username, oauth))
	return bots
	

def main():
	parser = argparse.ArgumentParser(description='Spam bot.')
	parser.add_argument('Stream', type=str, metavar='S', nargs=1, help='Stream to spam.')
	args = parser.parse_args()
	stream = args.Stream[0]
	if stream[0] != '#':
		stream = '#'+stream

	spam1 = "SUPERLARGESPAM FishMoley SUPERLARGESPAM FishMoley SUPERLARGESPAM FishMoley SUPERLARGESPAM FishMoley SUPERLARGESPAM FishMoley SUPERLARGESPAM FishMoley SUPERLARGESPAM FishMoley SUPERLARGESPAM FishMoley SUPERLARGESPAM FishMoley SUPERLARGESPAM FishMoley SUPERLARGESPAM FishMoley SUPERLARGESPAM FishMoley SUPERLARGESPAM FishMoley SUPERLARGESPAM FishMoley SUPERLARGESPAM FishMoley"
	bots = readInUsers(stream)

	for bot in bots:
		bot.start()
	for i in range(0, 100):
		flip = True
		for j in range(0, 10):
			for bot in bots:
				if flip == True:
					bot.sendMessage(spam1+" .")
				else:
					bot.sendMessage(spam1)
				wait(1000)
			flip = not flip
		wait(30000)

if __name__ == '__main__':
	main()
