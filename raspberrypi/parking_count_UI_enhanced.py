#sudo pigpiod please run this command 
import RPi.GPIO as GPIO
import tkinter as tk
import threading
import time
import pigpio

GPIO.setwarnings(False) #Disable any warning message such as GPIO pins in use

MAX_CAP = 5
ECHO_PIN = 3
DIST_MULT = 17000
TRIG_PIN = 4
servo = 18
veh = 0
state = "CLOSED"

#GPIO.setup(18, GPIO.OUT)
#p = GPIO.PWM(18, 50)
pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)

pwm.set_PWM_frequency( servo, 50 )

GPIO.setmode(GPIO.BCM)


def reading(sensor):
    if sensor == 0:
        GPIO.setup(TRIG_PIN,GPIO.OUT)
        GPIO.setup(ECHO_PIN,GPIO.IN)
        GPIO.output(TRIG_PIN, GPIO.LOW)

        time.sleep(0.2)
        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
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

def gate_opener():

    global state
    global veh
    while 1:
        reader = reading(0)
        print("The vehicle is %.2f" %reader,"cms away")
        if (reader < 10):
            #p.ChangeDutyCycle(2.5)
            
            if state == "CLOSED":
                if veh < MAX_CAP:
                    gate_label.config(text="The Gate is OPEN", fg="green")
                    pwm.set_servo_pulsewidth( servo, 500 );
                    veh = veh + 1
                    label.config(text="Vehicle Count : {}".format(veh), fg="blue")
                    state = "OPEN"
                    time.sleep(2)
        else:
            #p.start(7.5)
            #p.ChangeDutyCycle(7.5)
            if state == "OPEN":
                state = "CLOSED"
                if veh >= MAX_CAP:
                    gate_label.config(text="Parking is FULL!", fg="red")
                    pwm.set_servo_pulsewidth( servo, 1500);
                else:
                    pwm.set_servo_pulsewidth( servo, 1500);
                    gate_label.config(text="The Gate is CLOSED", fg="orange")
            time.sleep(0.5)      
                    
def update_label():
    pwm.set_servo_pulsewidth( servo, 1500);
    gate_label.config(text="The Gate is CLOSED")
    label.config(text="Vehicle Count : {}".format(veh))
    #root.after(100, update_label)

root = tk.Tk()
root.title("Counting Vehicles")
gate_label = tk.Label(root, fg="orange")
label = tk.Label(root, fg="blue")
label.pack()
gate_label.pack()
root.geometry("1000x500+0+0")

update_label()

t1 = threading.Thread(target=gate_opener, args = ())
t1.start()

root.mainloop()
t1.join()
