from raspi_serial import *
from wifi import Cell, Scheme
import threading, time

def get_wifi_ssid(cell):
	cell = Cell.all('wlan0')
	ssids = [cells.ssid for cells in cell]
	return ssids

class PCComThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.__cell = Cell.all('wlan0')
	        self.__continue = True
		
	
	def stop(self):
		self.__continue = False

	def run(self):
		while(self.__continue):
			strs = serial_read_line()
			print (strs)
			if(strs == "REQ?CON"):
				serial_send_line("RSP?CON")
				print("respond")
			elif(strs == "GET?SSIDLIST"):
				ssids = get_wifi_ssid(self.__cell)
				serial_send_line("RSP?SSID")
				serial_send_line(str(len(ssids)))
				for ssid in ssids:
					serial_send_line(ssid)
				
			elif(strs == "SET?SSID"):
				print("SET SSID")
				ssid = int(serial_read_line())
				pswd = serial_read_line()
				scheme = Scheme.for_cell('wlan0','home',self.__cell[ssid],pswd)
				try:
					scheme.delete()
				except:
					pass
				try:
					scheme.save()
				except:
					pass
				try:
					scheme.activate()
					serial_send_line("RSP?COMP")
				except:
					serial_send_line("RSP?SSID")
    
if __name__ == '__main__':
	pc_th = PCComThread()
	pc_th.start()
	try:
		while(True):
			 time.sleep(0.1)
	except KeyboardInterrupt: 
		pc_th.stop()
		print("STOP")
		pc_th.joint()

