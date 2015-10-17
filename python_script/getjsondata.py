import json
import urllib
import time
from datetime import datetime

rain = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
wind = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
dust = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
temp = [20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20]
tempPast24 = [20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20]

now = datetime.now()
befo_time = now.hour - 1

def UpdateJsonData(befo_time):
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
		rain[0] = rain[hourDif]
		rain[1] = rain[hourDif+1]
		wind[0] = wind[hourDif]
		wind[1] = wind[hourDif+1]
		dust[0] = dust[hourDif]
		dust[1] = dust[hourDif+1]
		temp[0] = temp[hourDif]
		temp[1] = temp[hourDif+1]
		tempPast24[0] = tempPast24[hourDif]
		tempPast24[1] = tempPast24[hourDif+1]
	
	init_time = nowHour
	past_time = nowHour
	for sz in result['data']:
		t = sz['time']
		index = t - init_time
		last_index = past_time - init_time
		#if index >= 12:
		#	break
		rain[index] = sz['rain']
		wind[index] = sz['wind']
		dust[index] = sz['dust']
		temp[index] = sz['temp']
		
		if index>2 :
			diff = temp[index] - temp[last_index]
			temp[index-1] = temp[last_index] + (int)(diff * 0.33)
			temp[index-2] = temp[last_index] + (int)(diff * 0.67)
		if index>2 :
			diff = rain[index] - rain[last_index]
			rain[index-1] = rain[last_index] + (int)(diff * 0.33)
			rain[index-2] = rain[last_index] + (int)(diff * 0.67)
		if index>2 :
			diff = dust[index] - dust[last_index]
			dust[index-1] = dust[last_index] + (int)(diff * 0.33)
			dust[index-2] = dust[last_index] + (int)(diff * 0.67)
		if index>2 :
			diff = wind[index] - wind[last_index]
			wind[index-1] = wind[last_index] + (int)(diff * 0.33)
			wind[index-2] = wind[last_index] + (int)(diff * 0.67)
		
		past_time = t
		
		
	for i in range(12):
		print(nowHour+i,rain[i], wind[i], dust[i], temp[i])
	print("Now Hour =", nowHour, "Updated")
	return nowHour

while (1):
	befo_time = UpdateJsonData(befo_time)
	time.sleep(1800)
	
