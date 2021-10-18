from machine import Pin, PWM
from time import sleep

RPIN = PWM(Pin(21), 255)
GPIN = PWM(Pin(22), 255)
BPIN = PWM(Pin(23), 255)




class COLOR:
	def __init__(self, RPIN, GPIN, BPIN):
		self.RPIN = RPIN
		self.GPIN = GPIN
		self.BPIN = BPIN

	def RED_color(self):
		RPIN.duty(255)
		GPIN.duty(-1)
		BPIN.duty(-1)

	def BLUE_color(self):
		RPIN.duty(-1)
		GPIN.duty(-1)
		BPIN.duty(255)	

	def GREEN_color(self):
		RPIN.duty(-1)
		GPIN.duty(255)
		BPIN.duty(-1)	

	def YELLOW_color(self):
		RPIN.duty(255)
		GPIN.duty(255)
		BPIN.duty(-1)

	def PURPLE_color(self):
		RPIN.duty(255)
		GPIN.duty(-1)
		BPIN.duty(255)

	def SKY_color(self):
		RPIN.duty(-1)
		GPIN.duty(255)
		BPIN.duty(255)

	def WHITE_color(self):
		RPIN.duty(51)
		GPIN.duty(51)
		BPIN.duty(51)

blink = COLOR(-1,-1,-1)
