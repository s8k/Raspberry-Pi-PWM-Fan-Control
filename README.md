# Raspberry Pi PWM Fan Control

This is a simple script to control your pwm fan on raspberry pi.

Here's how I wiring the PWM fan on pi:

English: [Using-Raspberry-Pi-to-Control-a-PWM-Fan-and-Monitor-its-Speed](https://blog.driftking.tw/2019/11/Using-Raspberry-Pi-to-Control-a-PWM-Fan-and-Monitor-its-Speed/)

中文：[利用 Raspberry Pi 控制 PWM 風扇及轉速偵測](https://blog.driftking.tw/2019/11/Using-Raspberry-Pi-to-Control-a-PWM-Fan-and-Monitor-its-Speed/)

# Difference from the original branch

* Linear fan speed control function changed to exponential
* Fewer probings when temperature goes down (WAIT_TIME_TEMP_DOWN and WAIT_TIME_TEMP_UP)
* Separate parameters for minimum temperature to turn the fan on (MIN_TEMP_ON) and to turn off (MIN_TEMP_OFF)
