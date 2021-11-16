import RPi.GPIO as GPIO
import time
from move import CarMove

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class Car(CarMove):
    def __init__(self):
        CarMove.__init__(self)

    def AllStop(self):
        CarMove.MotorStop(self)
        GPIO.cleanup()

car=Car()

try:
    car.left(80)
    car.forward(40)
    time.sleep(1)
    car.right(80)
    car.forward(50)
    time.sleep(1)
    car.brake()
except KeyboardInterrupt as result:
    car.AllStop()
