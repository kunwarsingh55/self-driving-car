import RPi.GPIO as GPIO
from time import sleep

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




pwmA.ChangeDutyCycle(20);
GPIO.output(In1,GPIO.LOW);
GPIO.output(In2,GPIO.HIGH);

sleep(1)

pwmA.ChangeDutyCycle(0);
sleep(1)

#pwmA.ChangeDutyCycle(20);
#GPIO.output(In1,GPIO.HIGH);
#GPIO.output(In2,GPIO.LOW);
#sleep(1)

print("done")



