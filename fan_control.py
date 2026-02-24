#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import os

# --- Configuration ---
FAN_PIN = 18            # BCM pin for PWM fan
PWM_FREQ = 10000        # 10kHz for PWM fans
WAIT_UP = 5             # Poll frequency when heating up
WAIT_DOWN = 15          # Poll frequency when cooling down

# --- Thermal Thresholds ---
# Pi 4 idles ~40-50°C. Keeping OFF below 50°C ensures total silence at idle.
TEMP_START = 50         # Fan starts spinning here
TEMP_TARGET = 72        # Target to stay below (Max cooling starts here)
HYSTERESIS = 5          # Temp must drop to (TEMP_START - HYSTERESIS) to turn OFF

# --- PWM Speeds ---
# Noctua fans usually need ~30% PWM to overcome friction and spin reliably.
FAN_LOW = 24
FAN_HIGH = 100
FAN_OFF = 0

def get_cpu_temp():
    try:
        res = os.popen("vcgencmd measure_temp").readline()
        return float(res.replace("temp=", "").replace("'C\n", ""))
    except Exception:
        return TEMP_START + 1 # Fallback safety

def calculate_speed(temp, prev_speed):
    # 1. Hysteresis: Stop 'fan-flutter' near the start threshold
    if temp < (TEMP_START - HYSTERESIS):
        return FAN_OFF

    # 2. Keep fan off if we haven't hit the start trigger yet
    if temp < TEMP_START and prev_speed == FAN_OFF:
        return FAN_OFF

    # 3. Max Protection
    if temp >= TEMP_TARGET:
        return FAN_HIGH

    # 4. Cubic Curve Optimization
    # Stay at FAN_LOW for longer, ramping up aggressively only near 70°C
    # Formula: Low + (Range * (Progress^3))
    progress = (temp - TEMP_START) / (TEMP_TARGET - TEMP_START)
    speed = FAN_LOW + (FAN_HIGH - FAN_LOW) * (progress ** 3)

    return int(speed)

def main():
    # Setup GPIO
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FAN_PIN, GPIO.OUT, initial=GPIO.LOW)

    pwm = GPIO.PWM(FAN_PIN, PWM_FREQ)
    pwm.start(FAN_OFF)

    current_speed = FAN_OFF
    prev_temp = get_cpu_temp()

    try:
        while True:
            temp = get_cpu_temp()
            new_speed = calculate_speed(temp, current_speed)

            # Only update PWM if speed actually changed to save CPU cycles
            if new_speed != current_speed:
                pwm.ChangeDutyCycle(new_speed)
                current_speed = new_speed

            # Dynamic sleep based on thermal trend
            sleep_time = WAIT_DOWN if temp < prev_temp else WAIT_UP
            prev_temp = temp

            time.sleep(sleep_time)

    except KeyboardInterrupt:
        # Safety: Set fan to 100% if script is killed manually
        pwm.ChangeDutyCycle(FAN_HIGH)
        print("\nFan control stopped. Fan set to MAX for safety.")

if __name__ == "__main__":
    main()
