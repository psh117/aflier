# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.
import time

from neopixel import *
import threading, time

# led number = time_table[hour]
time_table = [6,5,4,3,2,1,0,11,10,9,8,7,6,5,4,3,2,1,0,11,10,9,8,7]


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


# LED strip configuration:
LED_COUNT      = 12      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)


# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
	"""Generate rainbow colors across 0-255 positions."""
	if pos < 85:
		return Color(pos * 3, 255 - pos * 3, 0)
	elif pos < 170:
		pos -= 85
		return Color(255 - pos * 3, 0, pos * 3)
	else:
		pos -= 170
		return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
	"""Draw rainbow that uniformly distributes itself across all pixels."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel(((i * 256 / strip.numPixels()) + j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)
				

class LEDThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
                self.__continue = True
		self.strip.begin()
		self.colors = [Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0), Color(0,0,0)]
		self.mode = 'show'
		self.dt = 0
		self.count = 0
	
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
			
			elif(self.mode == 'disp_up'):
				self.reset_pix_data()
				for i in range(self.count):
					self.strip.setPixelColor(time_table[11],color_rd[1])
					self.strip.setPixelColor(time_table[12],color_rd[2])
					self.strip.setPixelColor(time_table[1],color_rd[1])
					self.strip.show()
					time.sleep(self.dt)
					self.strip.setPixelColor(time_table[11],0)
					self.strip.setPixelColor(time_table[12],0)
					self.strip.setPixelColor(time_table[1],0)
					self.strip.show()
					time.sleep(self.dt)
				self.mode = 'none'
			elif(self.mode == 'disp_down'):
				self.reset_pix_data()
				for i in range(self.count):
					self.strip.setPixelColor(time_table[5],color_bl[1])
					self.strip.setPixelColor(time_table[6],color_bl[2])
					self.strip.setPixelColor(time_table[7],color_bl[1])
					self.strip.show()
					time.sleep(self.dt)
					self.strip.setPixelColor(time_table[5],0)
					self.strip.setPixelColor(time_table[6],0)
					self.strip.setPixelColor(time_table[7],0)
					self.strip.show()
					time.sleep(self.dt)
				self.mode = 'none'
			elif(self.mode == 'disp_update'):
				for k in range(self.count):
					for i in range(12):
						self.reset_pix_data();
						self.strip.setPixelColor(time_table[(i+11)%12],color_rd[0])
						self.strip.setPixelColor(time_table[(i+12)%12],color_rd[1])
						self.strip.setPixelColor(time_table[(i+13)%12],color_rd[0])
						self.strip.show()
						time.sleep(self.dt)
				self.reset_pix_data()
				self.strip.show()
				self.mode = 'none'
			time.sleep(0.1)
	
	def reset_pix_data(self):
		for i in range(12):
			self.strip.setPixelColor(i,0)
	def fade_out(self, time):
		print ('fade_out 1')
		self.dt = time
		self.mode = 'fade_out'
	def fade_in(self, time):
		print ('fdae_in 1')
		self.dt = time
		self.mode = 'fade_in'
	def disp_up(self, time, count):
		print ('disp_up 1')
		self.dt = time
		self.count = count
		self.mode = 'disp_up'
	def disp_down(self, time, count):
		print ('disp_down 1')
		self.dt = time
		self.count = count
		self.mode = 'disp_down'
	def disp_update(self, time, count):
		print ('disp_update 1')
		self.dt = time
		self.count = count
		self.mode = 'disp_update'
		
	

print("NeoPixel Driver Loaded")

# Main program logic follows:
if __name__ == '__main__':
	# Create NeoPixel object with appropriate configuration.
	strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
	# Intialize the library (must be called once before other functions).
	strip.begin()

	print 'Press Ctrl-C to quit.'
	while True:
		# Color wipe animations.
		colorWipe(strip, Color(255, 0, 0))  # Red wipe
		colorWipe(strip, Color(0, 255, 0))  # Blue wipe
		colorWipe(strip, Color(0, 0, 255))  # Green wipe
		# Theater chase animations.
		theaterChase(strip, Color(127, 127, 127))  # White theater chase
		theaterChase(strip, Color(127,   0,   0))  # Red theater chase
		theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
		# Rainbow animations.
		rainbow(strip)
		rainbowCycle(strip)
		theaterChaseRainbow(strip)
