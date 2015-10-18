from slm1606m import *
from neopixel_user import *
from neopixel import *
from pc2serial import *
from getjsondata import *

import dot_data
import threading, time


color_blue = Color(0,160,182)


#color_
color_bl = [
	Color(180,240,250), 
	Color(110,200,200), 
	Color(0,80,182), 
	Color(10,40,220), 
	Color(0,0,255)
	]


color_rd = [
	Color(240,220,50),
	Color(200,180,0),
	Color(182,80,0),
	Color(200,40,10),
	Color(255,0,0)
	]

color_red = Color(241,15,10)
color_yellow = Color(182,160,0)

dot = dot_data.dot_17
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

class LEDThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
                self.__continue = True
		self.strip.begin()
		self.colors = [Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0)]
		self.mode = 'show'
		self.dt = 0
	
	def stop(self):
		self.__continue = False

	def run(self):
		while(self.__continue):
			if(self.mode == 'show'):
				for i in range(12):
					self.strip.setPixelColor(i,self.colors[i])
				self.strip.show()
				self.mode = 'none'
			elif(self.mode == 'fade_out'):
				print ('fdae_out st')
				for ratio in range(100,-1,-1):
					for i in range(12):
						r = self.colors[i] >> 16
						g = (self.colors[i]-(r<<16)) >> 8
						b = (self.colors[i]-(r<<16)-(g<<8))
						
						self.strip.setPixelColor(i,Color(int(r*ratio * 0.01),int(g*ratio * 0.01),int(b*ratio * 0.01)))
					
					self.strip.show()
					time.sleep(self.dt)
				print ('fdae_out')
				self.mode = 'none'
					
			elif(self.mode == 'fade_in'):
				for ratio in range(0,101):
					for i in range(12):
						r = self.colors[i] >> 16
						g = (self.colors[i]-(r<<16)) >> 8
						b = (self.colors[i]-(r<<16)-(g<<8))
						self.strip.setPixelColor(i,Color(int(r*ratio * 0.01),int(g*ratio * 0.01),int(b*ratio * 0.01)))
					
					self.strip.show()
					time.sleep(self.dt)
				self.mode = 'none'
				print ('fdae_in')
					
					
			time.sleep(0.1)
		
	def fade_out(self, time):
		self.dt = time
		self.mode = 'fade_out'
	def fade_in(self, time):
		self.dt = time
		self.mode = 'fade_in'
		
	
dot_th = DotThread(dot)
dot_th.start()
led_th = LEDThread()
led_th.start()
json_th = WTJsonThread()
json_th.start()
pc_th = PCComThread()
pc_th.start()
#dot_th.join()
time.sleep(1)
led_th.colors = [color_rd[0],color_rd[0],color_rd[0],color_rd[1],color_rd[2],color_rd[3],color_rd[4],color_rd[4],color_rd[3],color_rd[2],color_rd[1],color_rd[0]]
led_th.fade_in(0.03)
time.sleep(6)
led_th.fade_out(0.05)
try:
	while(True):
		time.sleep(0.1)

except KeyboardInterrupt:
	dot_th.stop()
	led_th.stop()
	json_th.stop()
	pc_th.stop()
	print("STOP")
	dot_th.join()
	led_th.join()
	json_th.join()
	pc_th.join()

