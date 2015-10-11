from slm1606m import *
from neopixel_user import *
from neopixel import *

import dot_data
import threading, time

color_blue = Color(0,160,182)
color_red = Color(241,15,10)
#color_yellow = Color

class DotThread(threading.Thread):
	def __init__(self, dot):
		threading.Thread.__init__(self)
		self.__continue = True
		self.dot = dot
	def run(self):
		while(self.__continue):
			display_dot_1212(self.dot,5,0,1)
			pass
	def stop(self):
		self.__continue = False

	def changeDot(self, dot):
		self.dot = dot

class LEDThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
                self.__continue = True
		self.strip.begin()
	
	def stop(self):
		self.__continue = False

	def run(self):
		while(self.__continue):
			#self.strip.setPixelColor(0,Color(0,160,182))
			#self.strip.setPixelColor(1,Color(0,160,182))
                        self.strip.setPixelColor(7,color_red)
                        self.strip.setPixelColor(5,color_red)
                        self.strip.setPixelColor(6,color_red)

			#self.strip.setPixelColor(11,Color(0,160,182))
			self.strip.show()
			time.sleep(1)
	
	

dot_th = DotThread(dot_data.dot_38)
dot_th.start()
led_th = LEDThread()
led_th.start()
#dot_th.join()

try:
	while(True):
		time.sleep(0.1)

except KeyboardInterrupt:
	dot_th.stop()
	led_th.stop()
	print("STOP")
	dot_th.join()
	led_th.join()

