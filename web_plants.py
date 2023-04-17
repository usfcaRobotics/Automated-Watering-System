# The Robotics Association
# April 12, 2023
# Session run by: Zoe Wong :)

# Automatic Plant Watering System
# Source: https://www.hackster.io/ben-eagan/raspberry-pi-automated-plant-watering-with-website-8af2dc?f=1

# This file contains the flask server for the plant watering website.

from flask import Flask, render_template
import psutil
import datetime
import water
import os

app = Flask(__name__)

def template(text = ""):
    now = datetime.datetime.now()
    timeString = now
    templateDate = {
        'time' : timeString,
        'text' : text
        }
    return templateDate

@app.route("/")
def load():
    templateData = template()
    return render_template('main.html', **templateData)

@app.route("/last_watered")
def check_last_watered():
    templateData = template(text = water.get_last_watered())
    return render_template('main.html', **templateData)

@app.route("/sensor")
def sense_status():
    status = water.get_status()
    print("status: " + water.get_status());
    message = ""
    if (status == 0):
        message = "Water me please!"
    else:
        message = "I'm a happy plant"

    templateData = template(text = message)
    return render_template('main.html', **templateData)

@app.route("/water")
def water_plant():
    water.pump_on()
    templateData = template(text = "Watered Once")
    return render_template('main.html', **templateData)

@app.route("/auto/water/<toggle>")
def auto_water(toggle):
    running = False
    if toggle == "ON":
        templateData = template(text = "Auto Watering On")
        for process in psutil.process_iter():
            try:
                if process.cmdline()[1] == 'auto_water.py':
                    templateData = template(text = "Already running")
                    running = True
            except:
                pass
        if not running:
            os.system("python3 auto_water.py&")
    else:
        templateData = template(text = "Auto Watering Off")
        os.system("pkill -f water.py")

    return render_template('main.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)