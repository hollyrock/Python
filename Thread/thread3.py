import time
from threading import Thread

def printer():
	for _ in range(3):
		print "hello"
		time.sleep(1.0)
		
thread = Thread(target=printer)
thread.start()
#thread.join()
print "good bye"
