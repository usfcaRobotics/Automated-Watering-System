import sys
import datetime
import time
try:
	import RPi.GPIO as GPIO
except ImportError:
	from unittest.mock import MagicMock
	GPIO = MagicMock()
	sys.modules['RPi'] = MagicMock()
	sys.modules['RPi.GPIO'] = MagicMock()

GPIO.setmode(GPIO.BOARD)

def get_status(pin = 8):
	GPIO.setup(pin, GPIO.IN)
	return GPIO.LOW

def init_output(pin):
	GPIO.setup(pin, GPIO.OUT)
	GPIO.output(pin, GPIO.LOW)
	GPIO.output(pin, GPIO.HIGH)

def pump_on(pump_pin = 7, delay = 1):
	print("pumping water...")
	init_output(pump_pin)
	f = open("last_watered.txt", "w")
	f.write("Last watered {}".format(datetime.datetime.now()))
	f.close()
	GPIO.output(pump_pin, GPIO.LOW)
	time.sleep(delay)
	GPIO.output(pump_pin, GPIO.HIGH)

def get_last_watered():
	try:
		f = open("last_watered.txt", "r")
		return f.readline()
	except:
		return "Never"

def auto_water(delay = 5, pump_pin = 7, water_sensor_pin = 8):
	consecutive_water_count = 0
	init_output(pump_pin)
	print("Here we go! Press CTRL+C to exit")
	try:
		while consecutive_water_count < 10:
			time.sleep(delay)
			wet = get_status(pin = water_sensor_pin) == 0
			if not wet:
				pump_on(pump_pin, 1)
				consecutive_water_count += 1
			else:
				consecutive_water_count = 0
	except KeyboardInterrupt:
		GPIO.cleanup()











