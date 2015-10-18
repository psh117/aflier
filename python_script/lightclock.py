from slm1606m import *
from neopixel_user import *
from neopixel import *
from pc2serial import *
from getjsondata import *
from gpiotest import *

import dot_data
import threading, time

import pygame # audio


color_blue = Color(0,160,182)

color_red = Color(241,15,10)
color_yellow = Color(182,160,0)

dot = dot_data.dot_hum
	

# program thread
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

pygame.mixer.init()

# circle init
led_th.disp_update(0.03,3)

# 60 sec after alarm
time.sleep(3)
pygame.mixer.music.load("/home/pi/aflier/wav/alram_meet_fall.wav")
pygame.mixer.music.play()
time.sleep(1)

# PSD detect
while (GPIO.input(PSD) == 0):
	led_th.disp_color(0.005)

# Compare Past Temp (Colder then past)

pygame.mixer.music.stop()
time.sleep(5)

led_th.disp_down(0.4,3)

time.sleep(5)

def psd_reader():
	if (GPIO.input(PSD)):
		pygame.mixer.music.load("/home/pi/aflier/wav/today_total.wav")
		pygame.mixer.music.play()
		while pygame.mixer.music.get_busy() == True:
			led_th.disp_update(0.03,1)
			
def psd_ready_sleep(time):	
	for i in range(int(time*10)):
		psd_reader()
		time.sleep(0.1)
try:
	while(True):
		# dust
		dot_th.red = 1
		dot_th.changeDot(dot_data.dot_pm)
		for i in range(12):
			led_th.colors[time_table[json_th.alhour[i]]] = color_rd[json_th.dust[i]]
		led_th.fade_in(0.02)
		psd_ready_sleep(5)
		led_th.fade_out(0.02)
		psd_ready_sleep(5)
		# rain
		dot_th.red = 0
		dot_th.changeDot(dot_data.dot_umbrella)
		for i in range(12):
			rain_level = 0
			if(json_th.rain[i] > 0.9):
				rain_level = 4
			elif(json_th.rain[i] > 0.7):
				rain_level = 3
			elif(json_th.rain[i] > 0.5):
				rain_level = 2
			elif(json_th.rain[i] > 0.2):
				rain_level = 1
			led_th.colors[time_table[json_th.alhour[i]]] = color_bl[rain_level]
		led_th.fade_in(0.02)
		psd_ready_sleep(5)
		led_th.fade_out(0.02)
		psd_ready_sleep(5)
		
		#snow
		dot_th.red = 0
		dot_th.changeDot(dot_data.dot_snow)
		for i in range(12):
			led_th.colors[time_table[json_th.alhour[i]]] = color_bl[json_th.snow[i]]
		led_th.fade_in(0.02)
		psd_ready_sleep(5)
		led_th.fade_out(0.02)
		psd_ready_sleep(5)
		
		# wind
		dot_th.red = 0
		dot_th.changeDot(dot_data.dot_umbrella) # TODO replace dot_umbrella to dot_wind
		for i in range(12):
			led_th.colors[time_table[json_th.alhour[i]]] = color_bl[json_th.wind[i]]
		led_th.fade_in(0.02)
		psd_ready_sleep(5)
		led_th.fade_out(0.02)
		psd_ready_sleep(5)

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

