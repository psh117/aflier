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
		self.green = 1
		self.red = 1
	def run(self):
		while(self.__continue):
			display_dot_1212(self.dot,5,self.green,self.red)
			pass
	def stop(self):
		self.__continue = False

	def changeDot(self, dot):
		self.dot = dot
	
	
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
#led_th.colors = [color_rd[0],color_rd[0],color_rd[0],color_rd[1],color_rd[2],color_rd[3],color_rd[4],color_rd[4],color_rd[3],color_rd[2],color_rd[1],color_rd[0]]

led_th.disp_update(0.03,3)
time.sleep(6)
#led_th.fade_in(0.02)
#time.sleep(6)
#led_th.fade_out(0.02)
#time.sleep(6)
#led_th.disp_up(0.4,3)
#time.sleep(6)
#led_th.disp_down(0.4,3)
try:
	while(True):
		# dust
		dot_th.red = 1
		dot_th.changeDot(dot_data.dot_sun)
		for i in range(12):
			led_th.colors[time_table[json_th.alhour[i]]] = color_rd[json_th.dust[i]]
		led_th.fade_in(0.02)
		time.sleep(6)
		led_th.fade_out(0.02)
		time.sleep(6)
		# dust
		dot_th.red = 0
		dot_th.changeDot(dot_data.dot_umbrella)
		for i in range(12):
			led_th.colors[time_table[json_th.alhour[i]]] = color_bl[json_th.wind[i]]
		led_th.fade_in(0.02)
		time.sleep(6)
		led_th.fade_out(0.02)
		time.sleep(6)

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

