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
        
    async def waitForEchoTill(self, isHigh):
        #print ("check echo for {}".format(isHigh))
        #await asyncio.sleep(0.0001)
        while GPIO.input(self.echo_pin) == isHigh:
            continue
        return time.time()
    
    def nonAwaitEcho(self, isHigh):
        #print ("check echo for {}".format(isHigh))
        #await asyncio.sleep(0.0001)
        while GPIO.input(self.echo_pin) == isHigh:
           continue
        return time.time()

    async def checkEcho(self):
        print("checking echo for 0")
        #await signaloff
        signaloff = await self.waitForEchoTill(0)
        print("checking echo for 1")
        signalon = await self.waitForEchoTill(1)
        return signalon - signaloff
    
    async def trigPulse(self):
        print("sending pulse")
        GPIO.output(self.trig_pin, GPIO.LOW)
        await asyncio.sleep(0.2)
        GPIO.output(self.trig_pin, True)
        time.sleep(0.00001)
        GPIO.output(self.trig_pin, False)

    async def checkDistance(self):
       
        #timePassedTask = asyncio.create_task(self.checkEcho())
        trigPulseTask = asyncio.create_task(self.trigPulse())
        await trigPulseTask

        signaloff = self.nonAwaitEcho(0)
        signalon = self.nonAwaitEcho(1)
        #timepassed = await timePassedTask 
        

        #distance = timepassed * DIST_MULT
        distance = (signalon - signaloff) * DIST_MULT
        print("Distance measured : {}".format(distance))
        return distance
    
    async def printMin(self):
        print("await check")
        #await asyncio.sleep(0.1)
        return self.printMin()

    async def continuousDistanceCheck(self, min,  delay, callbackMin, callback):
        try:
            while True:
                distance = await self.checkDistance()
                if(distance < min):
                    print("Min Distance crossed")
                    callbackMin = await callbackMin
                else:
                    print("Min Distance NOT crossed")
                    callback = await callback
                await asyncio.sleep(delay)
        except KeyboardInterrupt:
            print("Exciting continuous checking mode")

if __name__ == "__main__":
    obj = ultrasonic(ECHO_PIN, TRIG_PIN)
    #print(asyncio.run(obj.checkDistance()))
    asyncio.run(obj.continuousDistanceCheck(10, 1, obj.printMin(), obj.printMin()))
