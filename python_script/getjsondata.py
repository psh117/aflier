import json
import urllib
import time
from datetime import datetime
import threading


class WTJsonThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.__continue = True
		self.rain = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.wind = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.dust = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
		self.temp = [20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20]
		self.tempPast24 = [20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20]
		self.now = datetime.now()
		self.befo_time = self.now.hour - 1
	
	def stop(self):
		self.__continue = False

	def run(self):
		while(self.__continue):
			self.befo_time = self.UpdateJsonData(self.befo_time)
			for i in range (600):
				time.sleep(1)
				if (self.__continue == False):
					break
	
	def UpdateJsonData(self, befo_time):
		now = datetime.now()
		nowHour = now.hour #nowHour = variable[0]
		nowDay = now.day
		nowMonth = now.month
	
		# json read
		url = "http://54.92.73.84:8000/"
		result = json.load(urllib.urlopen(url))
		hourDif = 0
		
		#array pop
		if(nowHour < befo_time):
			hourDif = (nowHour + 24 - befo_time)
		elif (nowHour > befo_time):
			hourDif = nowHour - befo_time
		else :
			print ("Same hour, Skip")
			return nowHour
		
		if(hourDif < 11):
			self.rain[0] = self.rain[hourDif]
			self.rain[1] = self.rain[hourDif+1]
			self.wind[0] = self.wind[hourDif]
			self.wind[1] = self.wind[hourDif+1]
			self.dust[0] = self.dust[hourDif]
			self.dust[1] = self.dust[hourDif+1]
			self.temp[0] = self.temp[hourDif]
			self.temp[1] = self.temp[hourDif+1]
			self.tempPast24[0] = self.tempPast24[hourDif]
			self.tempPast24[1] = self.tempPast24[hourDif+1]
		
		init_time = nowHour
		past_time = nowHour
		for sz in result['data']:
			t = sz['time']
			index = t - init_time
			last_index = past_time - init_time
			#if index >= 12:
			#	break
			self.rain[index] = sz['rain']
			self.wind[index] = sz['wind']
			self.dust[index] = sz['dust']
			self.temp[index] = sz['temp']
			self.tempPast24[index] = sz['tempPast24']
			
			if index>2 :
				diff = self.temp[index] - self.temp[last_index]
				self.temp[index-1] = self.temp[last_index] + (int)(diff * 0.33)
				self.temp[index-2] = self.temp[last_index] + (int)(diff * 0.67)
			if index>2 :
				diff = self.rain[index] - self.rain[last_index]
				self.rain[index-1] = self.rain[last_index] + (diff * 0.33)
				self.rain[index-2] = self.rain[last_index] + (diff * 0.67)
			if index>2 :
				diff = self.dust[index] - self.dust[last_index]
				self.dust[index-1] = self.dust[last_index] + (int)(diff * 0.33)
				self.dust[index-2] = self.dust[last_index] + (int)(diff * 0.67)
			if index>2 :
				diff = self.wind[index] - self.wind[last_index]
				self.wind[index-1] = self.wind[last_index] + (int)(diff * 0.33)
				self.wind[index-2] = self.wind[last_index] + (int)(diff * 0.67)
			if index>2 :
				diff = self.tempPast24[index] - self.tempPast24[last_index]
				self.tempPast24[index-1] = self.tempPast24[last_index] + (int)(diff * 0.33)
				self.tempPast24[index-2] = self.tempPast24[last_index] + (int)(diff * 0.67)
			
			past_time = t
			
			
		for i in range(12):
			print((nowHour+i)%24,self.rain[i], self.wind[i], self.dust[i], self.temp[i], self.tempPast24[i])
		print("Now Hour =", nowHour, "Updated")
		return nowHour


	
