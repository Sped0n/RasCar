import RPi.GPIO as GPIO
import time
import cv2
import numpy as np
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
                #elif dist_mov_ave < 100:
                    #car.forward(dist_mov_ave / 2 + 40)
                else:
                    cap = cv2.VideoCapture(0)
                    ret, frame = cap.read()
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
                    # dst = cv2.dilate(dst, None, iterations=2)
                    dst = cv2.erode(dst, None, iterations=6)
                    # cv2.imshow("dst", dst)
                    color = dst[400]
                    black_count = np.sum(color == 255)
                    black_index = np.where(color == 255)
                    if black_count == 0:
                        black_count = 1
                    center = (black_index[0][black_count - 1] + black_index[0][0]) / 2
                    direction = center - 320
                    print(direction)
                    if abs(direction) > 250:
                        car.brake()
                    elif direction >= 0:
                        if direction > 70:
                            direction = 70
                            car.track_right(direction)
                    elif direction < -0:
                        if direction < -70:
                            direction = -70
                            car.track_left(direction)


except KeyboardInterrupt as results:
    print("Measurement stopped by User")
car.AllStop()
cap.release()
cv2.destroyAllWindows()
