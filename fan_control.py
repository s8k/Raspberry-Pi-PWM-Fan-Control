#!/usr/bin/python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time
import signal
import sys
import os

# Configuration
FAN_PIN = 18                          # BCM pin used to drive PWM fan
PWM_FREQ = 25000                      # [Hz] 25kHz for Noctua PWM control
WAIT_TIME_TEMP_UP = 5                 # [s] Time to wait between each temperature probe when temperature goes up
WAIT_TIME_TEMP_DOWN = 20              # [s] Time to wait between each temperature probe when temperature goes down

# Configurable temperature and fan speed
MIN_TEMP_OFF = 30
MIN_TEMP_ON = 35
MAX_TEMP = 70
FAN_LOW = 30
FAN_HIGH = 100
FAN_OFF = 0
FAN_MAX = 100

# Get CPU's temperature
def getCpuTemperature():
    res = os.popen("vcgencmd measure_temp").readline()
    temp = res.replace("temp=", "").replace("'C\n", "")
    #print("Temp = {0}".format(temp))
    return temp

# Set fan speed
def setFanSpeed(speed):
    global previousFanSpeed
    if speed > FAN_MAX:
        speed = FAN_MAX
    elif speed < FAN_OFF:
        speed = FAN_OFF
    fan.start(speed)
    previousFanSpeed = speed
    #print("Speed = {0}".format(speed))
    return()

# Handle fan speed
def handleFanSpeed():
    global waitTime
    global previousTemp
    temp = float(getCpuTemperature())
    # Turn off the fan if temperature is below MIN_TEMP_OFF
    if temp < MIN_TEMP_OFF:
        speed = FAN_OFF
    # Set fan speed to LOW if it is already spinning and temperature is below MIN_TEMP_ON
    if previousFanSpeed > FAN_OFF and temp < MIN_TEMP_ON:
        speed = FAN_LOW
    # Set fan speed to MAXIMUM if the temperature is above MAX_TEMP
    elif temp > MAX_TEMP:
        speed = FAN_HIGH
    # Caculate dynamic fan speed
    else:
        speed = FAN_LOW + round((FAN_HIGH - FAN_LOW) * ((temp - MIN_TEMP_ON) ** 2) / ((MAX_TEMP - MIN_TEMP_ON) ** 2))
    setFanSpeed(speed)
    if previousTemp > temp:
        waitTime = WAIT_TIME_TEMP_DOWN
    else:
        waitTime = WAIT_TIME_TEMP_UP
    previousTemp = temp
    return ()

try:
    # Setup GPIO pin
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)
    fan = GPIO.PWM(FAN_PIN, PWM_FREQ)
    waitTime = WAIT_TIME_TEMP_UP
    previousTemp = MIN_TEMP_OFF
    previousFanSpeed = FAN_OFF
    setFanSpeed(FAN_OFF)
    # Handle fan speed every 'waitTime' sec
    while True:
        handleFanSpeed()
        #print("Sleeping for {0}s...".format(waitTime))
        time.sleep(waitTime)

except KeyboardInterrupt: # trap a CTRL+C keyboard interrupt
    setFanSpeed(FAN_HIGH)
