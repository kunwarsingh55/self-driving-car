  

#!/usr/bin/python3
import RPi.GPIO as GPIO
import pigpio
import time
 
servo = 12
 
# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth
 
pwm = pigpio.pi() 
pwm.set_mode(servo, pigpio.OUTPUT)
 
pwm.set_PWM_frequency( servo, 50 )
 
print( "0 deg" )
pwm.set_servo_pulsewidth( servo, 800 ) ;
time.sleep( 2 )
 
print( "90 deg" )
pwm.set_servo_pulsewidth( servo, 1500 ) ;
time.sleep( 2 )
 
print( "180 deg" )
pwm.set_servo_pulsewidth( servo, 2200 ) ;
time.sleep( 2 )

 
print( "90 deg" )
pwm.set_servo_pulsewidth( servo, 1500 ) ;
time.sleep( 2 )
 
# turning off servo
pwm.set_PWM_dutycycle(servo, 0)
pwm.set_PWM_frequency( servo, 0 )