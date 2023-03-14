import RPi.GPIO as GPIO
import time
import pigpio

GPIO.setwarnings(False) #Disable any warning message such as GPIO pins in use

ECHO_PIN = 3
DIST_MULT = 17000
TRIG_PIN = 4
servo = 2
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

while 1:
    reader = reading(0)
    print("The vehicle is %.2f" %reader,"cms away")
    if (reader < 10):
        pwm.set_servo_pulsewidth( servo, 500 );
        #p.ChangeDutyCycle(2.5)
        print("The Gate is OPEN")
        if state == "CLOSED":
            veh = veh + 1
            state = "OPEN"
        print("Vehicle Count : {}".format(veh))
        time.sleep(2)
    else:
        pwm.set_servo_pulsewidth( servo, 1500 ) ;
        #p.start(7.5)
        #p.ChangeDutyCycle(7.5)
        print("The Gate is CLOSED")
        if state == "OPEN":
            state = "CLOSED"
        print("Vehicle Count : {}".format(veh))
        time.sleep(0.5)      
                

