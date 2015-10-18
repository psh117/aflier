from raspi_serial import *
from wifi import Cell, Scheme

gCell = Cell.all('wlan0')

def get_wifi_ssid(cell):
	cell = Cell.all('wlan0')
	ssids = [cells.ssid for cells in cell]
	return ssids

while (1):
	strs = serial_read_line()
	print (strs)
	if(strs == "REQ?CON"):
		serial_send_line("RSP?CON")
		print("respond")
	elif(strs == "GET?SSIDLIST"):
		ssids = get_wifi_ssid(gCell)
		serial_send_line("RSP?SSID")
		serial_send_line(str(len(ssids)))
		for ssid in ssids:
			serial_send_line(ssid)
		
	elif(strs == "SET?SSID"):
		print("SET SSID")
		ssid = int(serial_read_line())
		pswd = serial_read_line()
		scheme = Scheme.for_cell('wlan0','home',gCell[ssid],pswd)
		try:
			scheme.delete()
		except:
			pass
		try:
			scheme.save()
		except:
			pass
		scheme.activate()
		print("Complete")
    
