from servo import servo_motor
import asyncio

START = 500
GATE_ANGLE = 90
SPEED = 5
SERVO_PIN = 18

CURRENT_STATE = "CLOSED"
MAX_RANGE = 2000
MAX_ANGLE = 180

async def printOpen():
    print("OPEN")

class gate_state:
    
    def get_end(self):
        return int(MAX_RANGE/MAX_ANGLE * self.gate_angle) + START
    
    def __init__(self, __servo_pin, __gate_angle):
        self.servo_pin = __servo_pin
        self.gate_angle = __gate_angle
        self.servo_obj = servo_motor(self.servo_pin, START, self.get_end(), SPEED)

    async def stateChange(self, state):
        global CURRENT_STATE
        if(CURRENT_STATE != state):
            openGate = (state == "OPEN")
            if (not openGate):
                await asyncio.sleep(4)
            await self.servo_obj.openReturn(openGate, printOpen)
            CURRENT_STATE = state
        return self.stateChange(state)
