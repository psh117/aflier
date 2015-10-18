from raspi_serial import *
from wifi import Cell, Scheme

def get_wifi_ssid():
	ssids = [cell.ssid for cell in Cell.all('wlan0')]
	return ssids

while (1):
	strs = serial_read_line()
	print (strs)
	if(strs == "REQ?CON"):
		serial_send_line("RSP?CON")
		print("respond")
	if(strs == "GET?SSIDLIST"):
		ssids = get_wifi_ssid()
		serial_send_line("RSP?SSID")
		serial_send_line(str(len(food)))
		for ssid in ssids:
			serial_send_line(ssid)
		
    
