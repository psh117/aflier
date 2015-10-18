import RPi.GPIO as GPIO
import time, threading

PSD = 23 # select
SW1 = 27 # clock
SW2 = 22 # red 

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(PSD, GPIO.IN)
GPIO.setup(SW1, GPIO.IN)
GPIO.setup(SW2, GPIO.IN)

class GPIOThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.psd = 0
		self.sw1 = 0
		self.sw2 = 0
        self.__continue = True
		
	def stop(self):
		self.__continue = False

	def run(self):
		while (self.__continue):
			if(self.sw1 != GPIO.input(SW1)):
				self.sw1 = GPIO.input(SW1)
				print("SW1 =",self.sw1)
				time.sleep(0.05)
			
			if(self.sw2 != GPIO.input(SW2)):
				self.sw2 = GPIO.input(SW2)
				print("SW2 =",self.sw2)
				time.sleep(0.05)
			
			if(self.psd != GPIO.input(PSD)):
				self.psd = GPIO.input(PSD)
				print("PSD =",self.psd)
				time.sleep(0.05)
		

