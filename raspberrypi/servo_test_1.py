#!/usr/bin/python3
import RPi.GPIO as GPIO
import pigpio
import time

servo = 2

# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth

pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)

pwm.set_PWM_frequency( servo, 50 )

while 1: 
    for i in range(500, 2500, 50):
        print( "{} deg".format(180/2500*i) )
        pwm.set_servo_pulsewidth( servo, i ) ;
        time.sleep( 0.5 )

    for i in range(2500, 500, -50):
        print( "{} deg".format(180/2500*i) )
        pwm.set_servo_pulsewidth( servo, i ) ;
        time.sleep( 0.5 )

# turning off servo
pwm.set_PWM_dutycycle( servo, 0 )
pwm.set_PWM_frequency( servo, 0 )
