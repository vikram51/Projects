#sudo pigpiod please run this command 
from ultrasonic import ultrasonic
from led import led
from gate_state import gate_state
import asyncio
import azure_connect
import time

LED_PIN = 21
ECHO_PIN = 3
TRIG_PIN = 4
SERVO_PIN = 18
GATE_ANGLE = 180
MIN_DIST = 15
CHECK_DELAY = 0.2

async def main():
    
    ledObj = led(LED_PIN)
    flicker_task = asyncio.create_task(ledObj.flicker(0.1))
    
    azure_task = asyncio.create_task(azure_connect.azureConnect())

    ultraObj = ultrasonic(ECHO_PIN, TRIG_PIN)
    gateObj = gate_state(SERVO_PIN, GATE_ANGLE)
    
    ultrasonic_task = ultraObj.continuousDistanceCheck(MIN_DIST, CHECK_DELAY, gateObj.openIt(), gateObj.closeIt())

    await ultrasonic_task
    await flicker_task
    await azure_task

if __name__ == "__main__":
    asyncio.run(main())
