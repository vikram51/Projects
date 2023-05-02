
import time
import pigpio
import asyncio
import logging
import RPi.GPIO as GPIO

GPIO.setwarnings(False) #Disable any warning message such as GPIO pins in use
logging.basicConfig(level=logging.ERROR)


SERVO_PIN = 18
START = 2500
END = 500
SPEED = 3

PWM_FREQ = 50
SPEED_MULT = 10

class servo_motor:
    async def move(self, __angle):
        self.pwm.set_servo_pulsewidth( self.servo_pin, __angle);
    
    def get_step(self):
        return int((self.start - self.end) / (self.speed*SPEED_MULT))
    
    def get_move_sleep(self):
        return self.speed*self.step/(self.start - self.end)

    def __init__(self, __servo_pin, __start,  __end, __speed):
        self.servo_pin = __servo_pin
        self.start = __start
        self.end = __end
        self.speed = __speed
        self.step = self.get_step()
        self.move_sleep = self.get_move_sleep()
        GPIO.setmode(GPIO.BCM)
        self.pwm = pigpio.pi()
        self.pwm.set_mode(self.servo_pin, pigpio.OUTPUT)
        self.pwm.set_PWM_frequency( self.servo_pin, PWM_FREQ )

    async def rotate(self, reverse):
        start = self.start if reverse else self.end
        end = self.end if reverse else self.start
        step = -1*self.step if reverse else self.step
        for x in range(start, end, step):
            print("step angle is {}".format(x))
            await self.move(x)
            await asyncio.sleep(self.move_sleep)

    async def openReturn(self, open,  callback):
        await self.rotate(open)
        await callback()

    def printClose(self):
        print("I have closed")

if __name__ == "__main__":        
    #obj = servo_motor(SERVO_PIN, START, END, SPEED)
    #asyncio.run(obj.rotate(False))
    #asyncio.run(obj.rotate(True))
    obj1 = servo_motor(SERVO_PIN, END, START, SPEED)
    asyncio.run(obj1.openReturn(True, obj1.printClose))
    asyncio.run(obj1.openReturn(False, obj1.printClose))
