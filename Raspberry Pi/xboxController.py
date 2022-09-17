
import pygame
from time import sleep
pygame.init()
controller = pygame.joystick.Joystick(0)
controller.init()
#!/usr/bin/python3
import RPi.GPIO as GPIO
import pigpio
import time
 
servo = 12

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

Ena= 26
In1= 6
In2= 5


GPIO.setup(Ena,GPIO.OUT)
GPIO.setup(In1,GPIO.OUT)
GPIO.setup(In2,GPIO.OUT)


pwmA =GPIO.PWM(Ena,100);
pwmA.start(0);




#pwmA.ChangeDutyCycle(20);
#GPIO.output(In1,GPIO.LOW);
#GPIO.output(In2,GPIO.HIGH);



#pwmA.ChangeDutyCycle(20);
#GPIO.output(In1,GPIO.HIGH);
#GPIO.output(In2,GPIO.LOW);
#sleep(1)

curveMax = 1
curveMin = -1
curveValue = 0

servoMax = 2370
servoMin = 790

curveRange = (curveMax - curveMin)
servoRange = (servoMax - servoMin)

speedMax = 1
speedMin = -1
speedValue = 0

thMax = 100
thMin = 0

speedRange = (speedMax - speedMin)
thRange = (thMax - thMin)
print("done")
 
# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth
 
pwm = pigpio.pi() 
pwm.set_mode(servo, pigpio.OUTPUT)
 
pwm.set_PWM_frequency( servo, 50 )
 
 
def getJS(name=''):
 
    global buttons
    # retrieve any events ...
    for event in pygame.event.get():                                # Analog Sticks
        if event.type == pygame.JOYAXISMOTION:
            print("AXIS", event.axis , "Value = " , event.value)
            if event.axis == 100:
                #print(event.value)
                speedValue = event.value
                if(speedValue > -0.95):
                    thValue = (((speedValue - speedMin) * thRange) / speedRange) + thMin
                    #print(thValue)
                    if(thValue > 100):
                        thValue = 100
                    pwmA.ChangeDutyCycle(thValue);
                    GPIO.output(In1,GPIO.HIGH);
                    GPIO.output(In2,GPIO.LOW);
                else:
                    pwmA.ChangeDutyCycle(0);
            if event.axis == 5:
                #print(event.value)
                speedValue = event.value
                if(speedValue > -0.95):
                    thValue = (((speedValue - speedMin) * thRange) / speedRange) + thMin
                    #print(thValue)
                    if(thValue > 100):
                        thValue = 100
                    pwmA.ChangeDutyCycle(thValue);
                    GPIO.output(In1,GPIO.HIGH);
                    GPIO.output(In2,GPIO.LOW);
                else:
                    pwmA.ChangeDutyCycle(0);
                
            if event.axis == 0:
                if(event.value != 0.0):
                    #print(round(event.value,2))
                    if(event.value > 0.2):
                        curveValue = event.value
                        newValue = (((curveValue - curveMin) * servoRange) / curveRange) + servoMin
                        pwm.set_servo_pulsewidth( servo, newValue ) ;
                        print(newValue)
                    if(event.value < -0.2):
                        curveValue = event.value
                        newValue = (((curveValue - curveMin) * servoRange) / curveRange) + servoMin
                        pwm.set_servo_pulsewidth( servo, newValue ) ;
                        print(newValue)
                    elif (event.value > -0.2 and event.value < 0.2):
                        pwm.set_servo_pulsewidth( servo, 1500 ) ;
                        
                        
            #else:
                #pwm.set_servo_pulsewidth( servo, 1500 ) ;
        elif event.type == pygame.JOYBUTTONDOWN:                    # When button pressed
            print(event.dict, event.joy, event.button, 'PRESSED')
            if event.button == 3:
                pwmA.ChangeDutyCycle(30);
                GPIO.output(In1,GPIO.HIGH);
                GPIO.output(In2,GPIO.LOW);
            if event.button == 0:
                pwmA.ChangeDutyCycle(30);
                GPIO.output(In1,GPIO.LOW);
                GPIO.output(In2,GPIO.HIGH);
            
            
        elif event.type == pygame.JOYBUTTONUP:                      # When button released
            print(event.dict, event.joy, event.button, 'released')
            pwmA.ChangeDutyCycle(0);
            
                    
 
    
def main():
    #print(getJS()) # To get all values
    #sleep(0.05)
    getJS('share') # To get a single value
    sleep(0.05)
 
 
if __name__ == '__main__':
  while True:
    main()
