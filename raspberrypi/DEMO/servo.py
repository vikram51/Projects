
import time
import pigpio
import asyncio
import logging
import RPi.GPIO as GPIO

GPIO.setwarnings(False) #Disable any warning message such as GPIO pins in use
logging.basicConfig(level=logging.ERROR)


SERVO_PIN = 18
MAX = 2500
MIN = 500
STEP = 5

class servo_motor:
    async def move(self, angle):
        self.pwm.set_servo_pulsewidth( self.servo_pin, angle);

    def __init__(self, __servo_pin):
        self.servo_pin = __servo_pin
        GPIO.setmode(GPIO.BCM)
        self.pwm = pigpio.pi()
        self.pwm.set_mode(self.servo_pin, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency( self.servo_pin, 50 )
        asyncio.run(self.move(0))
        asyncio.run(asyncio.sleep(0.2))

    async def rotate(self, delay, reverse):
        start = MAX if reverse else MIN
        end = MIN if reverse else MAX
        step = -1*STEP if reverse else STEP
        for x in range(start, end, step):
            print(x)
            await self.move(x)
            await asyncio.sleep(delay*STEP/(MAX - MIN))
        
obj = servo_motor(SERVO_PIN)
asyncio.run(obj.rotate(2, False))
asyncio.run(obj.rotate(2, True))
