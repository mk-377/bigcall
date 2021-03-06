import RPi.GPIO as GPIO
import time

GPIO.cleanup()

while True:
    GPIO.setmode(GPIO.BOARD)
    TRIG = 12
    ECHO = 11
    GPIO.setup(TRIG,GPIO.OUT,initial=0)
    GPIO.setup(ECHO,GPIO.IN)
    time.sleep(0.1)
    print('starting')
    GPIO.output(TRIG,1)
    time.sleep(0.00001)
    GPIO.output(TRIG,0)

    while GPIO.input(ECHO) == 0:
        pass
        start = time.time()

    while GPIO.input(ECHO) == 1:
        print('YES')
        pass
        stop = time.time()

    print((stop - start) * 17000)

    GPIO.cleanup()


    