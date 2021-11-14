import RPi.GPIO as GPIO
import time
from ultrasound import CarUltrasound
from infrared import CarInfrared
from move import CarMove

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class Car(CarMove, CarUltrasound, CarInfrared):
    def __init__(self):
        CarMove.__init__(self)
        CarUltrasound.__init__(self)
        CarInfrared.__init__(self)

    def AllStop(self):
        CarMove.MotorStop(self)
        GPIO.cleanup()

try:
    car = Car()
    start_time = None
    while (1):
        # perception
        dist_mov_ave = car.DistMeasureMovingAverage()
        print('Distance', dist_mov_ave)

        [left_measure, right_measure] = car.InfraredMeasure()

        # decision-making
        if (start_time is None) or (time.time() - start_time > 0.5):
            start_time = None
            if left_measure == 0 and right_measure == 1:
                print("Going right")
                car.right(80)
            elif left_measure == 1 and right_measure == 0:
                print("Going left")
                car.left(80)
            elif left_measure == 0 and right_measure == 0:
                print("Going back")
                car.back(50)
            else:
                if dist_mov_ave < 20:
                    car.left(80)
                    print("Going left")
                    start_time = time.time()
                elif dist_mov_ave < 100:
                    car.forward(dist_mov_ave / 2 + 40)
                else:
                    car.forward(90)
    else:
        pass

except KeyboardInterrupt as results:
    print("Measurement stopped by User")
    car.AllStop()
