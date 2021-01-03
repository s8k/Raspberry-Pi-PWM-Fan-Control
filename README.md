# Raspberry Pi PWM Fan Control

This is a simple script to control your pwm fan on raspberry pi.

Here's how I wiring the PWM fan on pi:

English: [Using-Raspberry-Pi-to-Control-a-PWM-Fan-and-Monitor-its-Speed](https://blog.driftking.tw/en/2019/11/Using-Raspberry-Pi-to-Control-a-PWM-Fan-and-Monitor-its-Speed/)

中文：[利用 Raspberry Pi 控制 PWM 風扇及轉速偵測](https://blog.driftking.tw/2019/11/Using-Raspberry-Pi-to-Control-a-PWM-Fan-and-Monitor-its-Speed/)

# The differences of this fork

* The linear fan speed control function changed to the exponential one
* The script does fewer iterations when the temperature gradually goes down (WAIT_TIME_TEMP_DOWN and WAIT_TIME_TEMP_UP)
* Introducing the separate parameters for the minimum temperature to turn the fan on (MIN_TEMP_ON) and to turn it off (MIN_TEMP_OFF)
