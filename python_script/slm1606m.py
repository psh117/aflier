import RPi.GPIO as GPIO
import time

dot_umbr = [
0,0,0,0,0,0,0,0,0,0,0,0,
0,0,0,1,1,1,1,1,0,0,0,0,
0,0,1,0,0,0,0,0,1,0,0,0,
0,0,1,0,0,0,1,1,1,1,0,0,
0,0,0,1,0,1,0,0,1,0,1,0,
0,0,0,0,1,0,0,0,1,0,1,0,
0,0,0,0,0,1,0,1,0,0,1,0,
0,0,0,0,1,1,1,0,0,0,1,0,
0,1,0,1,1,0,0,1,0,0,1,0,
0,1,1,1,0,0,0,0,1,1,0,0,
0,0,1,0,0,0,0,0,0,0,0,0,
0,0,0,0,0,0,0,0,0,0,0,0
]

SEL = 13 # select
CLK = 19 # clock
RED = 20 # red 
GRN = 21 # green
BRT = 16 # bright
RST = 26 # reset

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(SEL, GPIO.OUT)
GPIO.setup(CLK, GPIO.OUT)
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(GRN, GPIO.OUT)
GPIO.setup(BRT, GPIO.OUT)
GPIO.setup(RST, GPIO.OUT)

GPIO.output(BRT, 0)
GPIO.output(SEL, 1)
GPIO.output(RST, 0)
GPIO.output(RST, 1)
GPIO.output(RST, 0)


def display_dot_1616(dot,duty,redOn,greenOn):
	for i in range(16):
		for j in range(16):
			GPIO.output(GRN, dot[i*16 + j] & greenOn)
                        GPIO.output(RED, dot[i*16 + j] & redOn)
			GPIO.output(CLK,1)
			GPIO.output(CLK,0)
			
		for j in range(duty):
			GPIO.output(BRT,1)
		GPIO.output(BRT,0)


def display_dot_1212(dot,duty,redOn,greenOn):
        GPIO.output(GRN,0)
	GPIO.output(RED,0)
	for i in range(2):
                for j in range(16):
                        GPIO.output(CLK,1)
                        GPIO.output(CLK,0)
                GPIO.output(BRT,1)
                GPIO.output(BRT,0)

	for i in range(12):
       		GPIO.output(GRN,0)
                GPIO.output(RED,0)
		for j in range(2):
                	GPIO.output(CLK,1)
                	GPIO.output(CLK,0)

		for j in range(12):
			GPIO.output(GRN, dot[i*12 + j] & greenOn)
                        GPIO.output(RED, dot[i*12 + j] & redOn)
			GPIO.output(CLK,1)
			GPIO.output(CLK,0)

		GPIO.output(GRN,0)
                GPIO.output(RED,0)
		for j in range(2):
                        GPIO.output(CLK,1)
                        GPIO.output(CLK,0)
			
		#GPIO.output(BRT,1)
		for j in range(duty):
			GPIO.output(BRT,1)
		GPIO.output(BRT,0)

        GPIO.output(GRN,0)
	GPIO.output(RED,0)
	for i in range(2):
                for j in range(16):
                        GPIO.output(CLK,1)
                        GPIO.output(CLK,0)
                GPIO.output(BRT,1)
                GPIO.output(BRT,0)



# Main program
if __name__ == '__main__':
	while(True):
		display_dot_1212(dot_umbr,1,1,1)
