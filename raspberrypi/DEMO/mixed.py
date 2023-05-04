#sudo pigpiod please run this command 
from ultrasonic import ultrasonic
from led import led
from gate_state import gate_state
import asyncio
import azure_connect
import threading
import time
import tkinter as tk
import queue


LED_PIN = 21
ECHO_PIN = 3
TRIG_PIN = 4
SERVO_PIN = 18
GATE_ANGLE = -90
MIN_DIST = 15
CHECK_DELAY = 0.2

gui_queue = queue.Queue()


async def handleGateOnDistanceContinuosuly():
    
    ledObj = led(LED_PIN)
    flicker_task = asyncio.create_task(ledObj.flicker(0.1))
    
    azure_task = asyncio.create_task(azure_connect.azureConnect())

    ultraObj = ultrasonic(ECHO_PIN, TRIG_PIN)
    gateObj = gate_state(SERVO_PIN, GATE_ANGLE)
    
    ultrasonic_task = ultraObj.continuousDistanceCheck(MIN_DIST, CHECK_DELAY, gateObj.openIt(), gateObj.closeIt())

    await ultrasonic_task
    await flicker_task
    await azure_task

def gateMain():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(handleGateOnDistanceContinuosuly())
    loop.run_forever()
    
def periodicGuiUpdate():
    while True:
        try:
            fn = gui_queue.get_nowait()
        except queue.Empty:
            break
        fn()
    root.after(200, periodicGuiUpdate)

def reset_counter():
    #global veh
    #global gate_text
    veh = 0
    #gate_text = "The Gate is CLOSED"
    #gui_queue.put(lambda: update_label("orange"))


if __name__ == "__main__":
    
    root = tk.Tk()
    root.title("Counting Vehicles")
    gate_label = tk.Label(root, font=("Helvetica", 16))
    gate_label.place(x=50, y=75)
    veh_label = tk.Label(root, fg="blue", font=("Helvetica", 16))
    veh_label.place(x=60, y=50)
    #veh_label.pack()
    #gate_label.pack()
    root.geometry("300x150+0+0")
    
    button = tk.Button(root, text="Reset Counter", command=reset_counter).pack(pady=20)
        
    gateThread = threading.Thread(target=gateMain)
    gateThread.start()
    
    periodicGuiUpdate()
    reset_counter()
    root.mainloop()

    gateThread.join()
   
