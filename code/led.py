#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
import sys

DIO = 13
CLK = 12
STB = 11

LSBFIRST = 0
MSBFIRST = 1

tmp = 0

def _shiftOut(dataPin, clockPin, bitOrder, val):
	for i in range(8):
		if bitOrder == LSBFIRST:
			GPIO.output(dataPin, val & (1 << i))
		else:
			GPIO.output(dataPin, val & (1 << (7 -i)))
		GPIO.output(clockPin, True)
		time.sleep(0.000001)			
		GPIO.output(clockPin, False)
		time.sleep(0.000001)			
	
def sendCommand(cmd):
	GPIO.output(STB, False)
	_shiftOut(DIO, CLK, LSBFIRST, cmd)
	GPIO.output(STB, True)

def TM1638_init():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(DIO, GPIO.OUT)
	GPIO.setup(CLK, GPIO.OUT)
	GPIO.setup(STB, GPIO.OUT)
	sendCommand(0x8f)

def numberDisplay_dec(num):
	digits = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f]
	integer = 0
	decimal = 0

	pro = int(num * 100)

	integer = int(pro / 100)
	decimal = int(pro % 100)

	sendCommand(0x40)
	GPIO.output(STB, False)
	_shiftOut(DIO, CLK, LSBFIRST, 0xc0)
	_shiftOut(DIO, CLK, LSBFIRST, digits[integer/10])
	_shiftOut(DIO, CLK, LSBFIRST, 0x00)
	_shiftOut(DIO, CLK, LSBFIRST, digits[integer%10] | 0x80)
	_shiftOut(DIO, CLK, LSBFIRST, 0x00)
	_shiftOut(DIO, CLK, LSBFIRST, digits[decimal/10])
	_shiftOut(DIO, CLK, LSBFIRST, 0x00)
	_shiftOut(DIO, CLK, LSBFIRST, digits[decimal%10])
	_shiftOut(DIO, CLK, LSBFIRST, 0x00)
	GPIO.output(STB, True)

try:
	TM1638_init()
        temp = float(sys.argv[1])
	numberDisplay_dec(temp)
	time.sleep(5) # 4s

except KeyboardInterrupt:
	GPIO.cleanup()

