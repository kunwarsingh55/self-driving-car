import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)  #Mode = Boradcom
GPIO.setwarnings(False)


class Motor():
    def __init__(self,EnaA,In1A,In2A,EnaB,In1B,In2B):
        self.EnaA = EnaA #EnAble
        self.In1A = In1A #Input 1
        self.In2A = In2A #Input 2
        self.EnaB = EnaB 
        self.In1B = In1B
        self.In2B = In2B 
        #Decare GPIO Pins as output pins
        GPIO.setup(self.In1A,GPIO.OUT)
        GPIO.setup(self.In2A,GPIO.OUT)
        GPIO.setup(self.EnaA,GPIO.OUT)
        GPIO.setup(self.In1B,GPIO.OUT)
        GPIO.setup(self.In2B,GPIO.OUT)
        GPIO.setup(self.EnaB,GPIO.OUT)

        #Setting EnAble Pins as Pwm PIN
        #(All GPIO Pins are capable of PWM signals)
        self.pwmA = GPIO.PWM(self.EnaA, 100);
        self.pwmA.start(0);
        self.pwmB = GPIO.PWM(self.EnaB,100); 
        self.pwmB.start(0);

    #Move Forward with particular speed and for given time and given turn
    def move(self,speed=0.5,turn=0,t=0):
        #Normalizing Values
        speed *= 100
        turn *= 100

        #Turning Logic =  +-turn to left and right motors
        leftSpeed = speed - turn
        rightSpeed = speed + turn
        #Limiting Speed between -100 to 100
        if leftSpeed > 100:
            leftSpeed = 100
        elif rightSpeed < -100:
            rightSpeed = -100
        if rightSpeed > 100:
            rightSpeed = 100
        elif rightSpeed < -100:
            rightSpeed = -100


        self.pwmA.ChangeDutyCycle(abs(leftSpeed));
        self.pwmB.ChangeDutyCycle(abs(rightSpeed));
        
        if leftSpeed > 0:
            GPIO.output(self.In1A,GPIO.HIGH)
            GPIO.output(self.In2A,GPIO.LOW)
        else:
            GPIO.output(self.In1A,GPIO.LOW)
            GPIO.output(self.In2A,GPIO.HIGH)

        if rightSpeed>0:
            GPIO.output(self.In1B,GPIO.HIGH)
            GPIO.output(self.In2B,GPIO.LOW)
        else:
            GPIO.output(self.In1B,GPIO.LOW)
            GPIO.output(self.In2B,GPIO.HIGH)
        sleep(t)
    

    #stop Function
    def stop(self,t=0):
        self.pwmA:ChangeDutyCycle(0);
        self.pwmB:ChangeDutyCycle(0);
        sleep(t)


'''    

'''
def main():
    motor1.move(0.15,0,1)
    motor1.stop(2)
    print("run")
    


#This is main modulw being executed
if __name__ == '__main__':
    motor1 = Motor(5,6,16,22,17,27)
    main()



