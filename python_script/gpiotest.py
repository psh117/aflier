import RPi.GPIO as GPIO
import time

PSD = 23 # select
SW1 = 27 # clock
SW2 = 22 # red 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(PSD, GPIO.IN)
GPIO.setup(SW1, GPIO.IN)
GPIO.setup(SW2, GPIO.IN)

sw1_ls = 0 # last status
sw2_ls = 0
psd_ls = 0


while (1):
  if(sw1_ls != GPIO.input(SW1)):
    sw1_ls = GPIO.input(SW1)
    print("SW1 =",sw1_ls)
    time.sleep(0.05)
    
  if(sw2_ls != GPIO.input(SW2)):
    sw1_ls = GPIO.input(SW2)
    print("SW2 =",sw2_ls)
    time.sleep(0.05)
    
  if(psd_ls != GPIO.input(PSD)):
    psd_ls = GPIO.input(PSD)
    print("PSD =",psd_ls)
    time.sleep(0.05)

