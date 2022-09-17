curveMax = 1
curveMin = -1
curveValue = -1

servoMax = 2200
servoMin = 800

curveRange = (curveMax - curveMin)
servoRange = (servoMax - servoMin)

newValue = (((curveValue - curveMin) * servoRange) / curveRange) + servoMin

while curveValue <= 1:
    newValue = (((curveValue - curveMin) * servoRange) / curveRange) + servoMin
    print(newValue)
    curveValue += 0.1

'''
 
NewValue = (((OldValue - OldMin) * NewRange) / OldRange) + NewMin


'''