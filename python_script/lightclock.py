from slm1606m import *
from neopixel import *

import threading, time

class DotThread(threading.Thread):
	def __init__(self, dot):
		threading.Thread.__init__(self)
		self.__continue = True
		self.dot = dot
	def run(self):
		while(self.__continue):
			display_dot_1212(self.dot,5,1,1)
			pass
	def stop(self):
		self.__continue = False

	def changeDot(self, dot):
		self.dot = dot



dot_th = DotThread(dot_umbr)
dot_th.start()
#dot_th.join()

try:
	while(True):
		time.sleep(0.1)
except KeyboardInterrupt:
	dot_th.stop()
	print("STOP")
	dot_th.join()

