import RPi.GPIO as GPIO
import tkinter as tk
import threading
import time
import pigpio
import asyncio
import logging
import json

from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device import MethodResponse
import random
import pnp_helper

GPIO.setwarnings(False) #Disable any warning message such as GPIO pins in use
logging.basicConfig(level=logging.ERROR)



DEVICE_ID_SCOPE = "0ne00976B17"
DEVICE_ID = "mwciuczxs7"
DEVICE_KEY = "vEzNNhL4aLB+N/sWsBAmzHy4a67u9YTnZAHXwf1V1CI="    #Primary Key

model_id = "dtmi:pigatecontrol:PiGate_lp;1"
sensorName1 = "gate_open_count"

MAX_CAP = 5
ECHO_PIN = 3
DIST_MULT = 17000
TRIG_PIN = 4
servo = 18
veh = 0
state = "CLOSED"
pwm = pigpio.pi()


gate_text = "The Gate is CLOSED"
gate_text_color = "orange"

root = tk.Tk()
root.title("Counting Vehicles")
gate_label = tk.Label(root, fg=gate_text_color, font=("Helvetica", 16))
gate_label.place(x=50, y=75)
veh_label = tk.Label(root, fg="blue", font=("Helvetica", 16))
veh_label.place(x=60, y=50)
#veh_label.pack()
#gate_label.pack()
root.geometry("300x150+0+0")

def reset_counter():
    global veh
    veh = 0
    update_label()    

def veh_text(veh_count):
    return "Vehicle Count : {}".format(veh_count)

async def send_telemetry_from_car_counter(device_client, telemetry_msg, component_name=None):
    msg = pnp_helper.create_telemetry(telemetry_msg, component_name)
    await device_client.send_message(msg)
    print("Sent message")
    print(msg)
    await asyncio.sleep(1)

async def provision_device(provisioning_host, id_scope, registration_id, symmetric_key, model_id):
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=provisioning_host,
        registration_id=registration_id,
        id_scope=id_scope,
        symmetric_key=symmetric_key,
    )

    provisioning_device_client.provisioning_payload = {"modelId": model_id}
    return await provisioning_device_client.register()

async def reading(sensor):
    if sensor == 0:
        GPIO.setup(TRIG_PIN,GPIO.OUT)
        GPIO.setup(ECHO_PIN,GPIO.IN)
        GPIO.output(TRIG_PIN, GPIO.LOW)

        await asyncio.sleep(0.2)
        GPIO.output(TRIG_PIN, True)
        await asyncio.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)

        while GPIO.input(ECHO_PIN) == 0:
          signaloff = time.time()
        
        while GPIO.input(ECHO_PIN) == 1:
          signalon = time.time()
        timepassed = signalon - signaloff
        distance = timepassed * DIST_MULT
        return distance
    else:
        print ("Incorrect usonic() function varible.")

async def gate_opener(device_client):
    global state
    global veh
    global gate_text
    reader = await reading(0)
    print("The vehicle is %.2f" %reader,"cms away")
    if (reader < 10):
        #p.ChangeDutyCycle(2.5)
        
        if state == "CLOSED":
            if veh < MAX_CAP:
                gate_text="The Gate is OPEN"
                gate_text_color="green"
                pwm.set_servo_pulsewidth( servo, 500 );
                veh = veh + 1
                await send_telemetry(device_client, veh)
                state = "OPEN"
        await asyncio.sleep(2)
    else:
        #p.start(7.5)
        #p.ChangeDutyCycle(7.5)
        if state == "OPEN":
            state = "CLOSED"
            if veh >= MAX_CAP:
                gate_text="Parking is FULL!"
                gate_text_color="red"
                pwm.set_servo_pulsewidth( servo, 1500);
            else:
                pwm.set_servo_pulsewidth( servo, 1500);
                gate_text_color="orange"
                gate_text="The Gate is CLOSED"
        await asyncio.sleep(2)      
    await gate_opener(device_client)

def update_label():
    gate_label.config(text=gate_text, fg=gate_text_color)
    veh_label.config(text=veh_text(veh))
    print("updating labels")
    root.after(1000, update_label)

async def send_telemetry(device_client, veh_count):
    print("Sending telemetry from various components")

    veh_count_msg = {"ParkingCounter": veh_count}
    print("sending count {}".format(veh_count_msg))
    await send_telemetry_from_car_counter(
        device_client, veh_count_msg
    )

def gate_opener_worker(device_client):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(gate_opener(device_client))
    loop.run_forever()

async def update_gate_label(self):
    self.gate_label["text"] = gate_text
    await asyncio.sleep(1000)

async def update_veh_label(self):
    global veh
    self.veh_label["text"] = veh_text(veh)
    await asyncio.sleep(1000)

async def main(async_loop):
    #GPIO.setup(18, GPIO.OUT)
    #p = GPIO.PWM(18, 50)
    pwm.set_mode(servo, pigpio.OUTPUT)

    pwm.set_PWM_frequency( servo, 50 )

    GPIO.setmode(GPIO.BCM)

    provisioning_host = (
        "global.azure-devices-provisioning.net"
    )
    id_scope = DEVICE_ID_SCOPE
    registration_id = DEVICE_ID
    symmetric_key = DEVICE_KEY

    registration_result = await provision_device(
        provisioning_host, id_scope, registration_id, symmetric_key, model_id
    )

    if registration_result.status == "assigned":
        print("Device was assigned")
        print(registration_result.registration_state.assigned_hub)
        print(registration_result.registration_state.device_id)
        device_client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key=symmetric_key,
            hostname=registration_result.registration_state.assigned_hub,
            device_id=registration_result.registration_state.device_id,
            product_info=model_id,
        )
    else:
        raise RuntimeError(
            "Could not provision device. Aborting Plug and Play device connection."
        )

    pwm.set_servo_pulsewidth( servo, 1500);
    await device_client.connect()
    t1 = threading.Thread(target=gate_opener_worker, args = (device_client,))
    t1.start()
    print("showing UI")
    root.after(1000, update_label)
    root.mainloop()
    #ui_task = asyncio.create_task(root.mainloop())
    #gate_task = asyncio.create_task(gate_opener(device_client))
    #await ui_task
    print("gate opener running")
    #await gate_task
    #await asyncio.gather(gate_opener(device_client), task())
    #t1.join()

button = tk.Button(root, text="Reset Counter", command=reset_counter).pack(pady=20)


if __name__ == "__main__":
    async_loop = asyncio.get_event_loop()
    asyncio.run(main(async_loop))
