# The Robotics Association
# March 29, 2023
# Session run by: Zoe Wong :)

# Automatic Plant Watering System
# Source: https://www.hackster.io/ben-eagan/raspberry-pi-automated-plant-watering-with-website-8af2dc?f=1

# This file contains functions for sensing when the plant is dry, 
# turning on the water pump, logging when the plant has been watered, 
# and automatically triggering the pump when needed.

# Note: this version was written to work for testing purposes to run
# without the hardware necessary for the project. Code that will
# be changed when we have the hardware parts has been labelled with
# "For now".

import sys
import datetime
import time

# For when we have an actual raspberry pi:
# import RPi.GPIO as GPIO

# For now: (because we don't have a raspberry pi connected)
try:
    import RPi.GPIO as GPIO
except ImportError:
    from unittest.mock import MagicMock
    GPIO = MagicMock()
    sys.modules['RPi'] = MagicMock()
    sys.modules['RPi.GPIO'] = MagicMock()

GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

# reads last_watered.txt file or prints "NEVER!" if it was never watered
def get_last_watered():
    try:
        f = open("last_watered.txt", "r")
        return f.readline()
    except:
        return "NEVER!"
      
# returns status of the pin
# GPIO.HIGH (plant is wet) or GPIO.LOW (plant is dry)
def get_status(pin = 8):
    GPIO.setup(pin, GPIO.IN) # set up the pin as input

    # For when connected to raspberry pi:
    # return GPIO.input(pin) # returns status of pin

    # For now: (because we don't have a sensor, pretend plant is always dry)
    return GPIO.LOW

# initialize pin as output
def init_output(pin):
    GPIO.setup(pin, GPIO.OUT) # set the pin as output
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)
    
# automatically calls pump_on periodically if the status of the pin
# from get_status is GPIO.LOW
def auto_water(delay = 5, pump_pin = 7, water_sensor_pin = 8):
    consecutive_water_count = 0
    init_output(pump_pin)
    print("Here we go! Press CTRL+C to exit")
    try:
        while consecutive_water_count < 10:
            time.sleep(delay) # waits 5 seconds
            wet = get_status(pin = water_sensor_pin) == 0 # 0 is same as GPIO.LOW or false
            if not wet:
                pump_on(pump_pin, 1)
                consecutive_water_count += 1
            else:
                consecutive_water_count = 0
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup() # cleanup all GPI

# resets pump output status, writes log to last_watered file, 
# turns pump on for 1 sec and then off again
def pump_on(pump_pin = 7, delay = 1):
    # For now: (because we don't have a pump, just print a message)
    print("pumping water...")

    # writes the time so we know when we last watered it
    init_output(pump_pin)
    f = open("last_watered.txt", "w") 
    f.write("Last watered {}".format(datetime.datetime.now())) 
    f.close()

    # turns pump on, waits, turns pump off
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(delay) 
    GPIO.output(pump_pin, GPIO.HIGH) 
    