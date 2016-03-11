import time

def timeMillis():
	return int(round(time.time() * 1000))

def wait(duration):
	before = timeMillis()
	while (timeMillis() - before <= duration):
		continue
