import time
import pigpio
import asyncio
import logging
import RPi.GPIO as GPIO

GPIO.setwarnings(False) #Disable any warning message such as GPIO pins in use
logging.basicConfig(level=logging.ERROR)

ECHO_PIN = 3
DIST_MULT = 34300/2
TRIG_PIN = 4

class ultrasonic:


    def __init__(self, __echo_pin, __trig_pin):
        self.echo_pin = __echo_pin
        self.trig_pin = __trig_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trig_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    async def checkDistance(self):
        GPIO.output(self.trig_pin, GPIO.LOW)
        await asyncio.sleep(0.2)
        GPIO.output(self.trig_pin, True)
        await asyncio.sleep(0.00001)
        GPIO.output(self.trig_pin, False)

        while GPIO.input(self.echo_pin) == 0:
          signaloff = time.time()
        
        while GPIO.input(self.echo_pin) == 1:
          signalon = time.time()
        timepassed = signalon - signaloff
        distance = timepassed * DIST_MULT
        return distance

    async def continuousDistanceCheck(self, min,  delay, callback):
        if(await self.checkDistance() < min):
            callback();
        await asyncio.sleep(delay)
        await self.continuousDistanceCheck(min, delay, callback)

    def printMin(self):
        print("Min Distance crossed")

if __name__ == "__main__":
    obj = ultrasonic(ECHO_PIN, TRIG_PIN)
    print(asyncio.run(obj.checkDistance()))
    asyncio.run(obj.continuousDistanceCheck(10, 0.2, obj.printMin))
