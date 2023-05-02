from servo import servo_motor
import asyncio
import azure_connect

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
    
    def __get_end(self):
        return int(MAX_RANGE/MAX_ANGLE * self.__gate_angle) + START
    
    def __init__(self, servo_pin, gate_angle):
        self.__veh_count = 0 
        self.__servo_pin = servo_pin
        self.__gate_angle = gate_angle
        self.__servo_obj = servo_motor(servo_pin, START, self.__get_end(), SPEED)

    async def __stateChange(self, state):
        global CURRENT_STATE
        if(CURRENT_STATE != state):
            openGate = (state == "OPEN")
            if (not openGate):
                await asyncio.sleep(4)
            await self.__servo_obj.openReturn(openGate, printOpen)
            CURRENT_STATE = state
        return self.__stateChange(state)
    
    async def openIt(self):
        self.__veh_count += 1
        await azure_connect.send_telemetry(self.__veh_count)
        return self.__stateChange("OPEN")
    
    async def closeIt(self):
        return self.__stateChange("CLOSED")