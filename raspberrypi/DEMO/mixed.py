from ultrasonic import ultrasonic
from led import led
from servo import servo_motor
import asyncio
import time

LED_PIN = 21
ECHO_PIN = 3
TRIG_PIN = 4
SERVO_PIN = 18
START = 2500
END = 1500
SPEED = 3
MIN_DIST = 15
CHECK_DELAY = 0.2

CURRENT_STATE = "CLOSED"

async def printOpen():
    print("OPEN")

async def stateChange(state, servoObj):
    global CURRENT_STATE
    if(CURRENT_STATE != state):
        openGate = (state == "OPEN")
        if (not openGate):
            await asyncio.sleep(4)
        await servoObj.openReturn(openGate, printOpen)
        CURRENT_STATE = state
    return stateChange(state, servoObj)
        
async def main():
    ledObj = led(LED_PIN)
    flicker_task = asyncio.create_task(ledObj.flicker(0.2))

    ultraObj = ultrasonic(ECHO_PIN, TRIG_PIN)
    servoObj = servo_motor(SERVO_PIN, START, END, SPEED)
    
    ultrasonic_task = ultraObj.continuousDistanceCheck(MIN_DIST, CHECK_DELAY, stateChange("OPEN", servoObj), stateChange("CLOSED", servoObj))

    await ultrasonic_task
    await flicker_task

if __name__ == "__main__":
    asyncio.run(main())
