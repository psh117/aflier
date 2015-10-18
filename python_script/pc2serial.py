from raspi_serial import *

while (1):
	strs = serial_read_line()
	if(strs == "REQ?CON"):
		serial_send_line("RSP?CON")
    
