import serial
import time

port = serial.Serial("/dev/ttyAMA0", baudrate=115200)

def serial_read_line():
	line = ""
	while (1):
		ch = port.read()
		if(ch == '\r' or ch == '\n'):
			return line
		line += ch
		
def serial_send_line(strs):
	port.write(strs + "\r\n")
	
if __name__ == '__main__':
	while (1):
		print("start")
		rcv = readLine()
		print(rcv)	
		port.write("Message : " + rcv + "\r\n")
