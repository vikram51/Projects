import time
import pigpio
import asyncio
import logging
import RPi.GPIO as GPIO

GPIO.setwarnings(False) #Disable any warning message such as GPIO pins in use
logging.basicConfig(level=logging.ERROR)


LED_PIN = 21

class led:

    def __init__(self, __led_pin):
        self.led_pin = __led_pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.led_pin, GPIO.OUT)

    def switch(self, turn_on):
        if turn_on:
            GPIO.output(self.led_pin, GPIO.HIGH)
        else:
            GPIO.output(self.led_pin, GPIO.LOW)
    
    async def flicker(self, freq):
        while True:
            self.switch(True)
            await asyncio.sleep(freq)
            self.switch(False)
            await asyncio.sleep(freq)

if __name__ == "__main__":
    obj = led(LED_PIN)
    asyncio.run(obj.flicker(0.1))
