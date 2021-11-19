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
    center = 320
    slow_down_rate = 0
    cap = cv2.VideoCapture(0)
    while (1):
        # perception
        slow_down_rate = 1;
        dist_mov_ave = car.DistMeasureMovingAverage()
        print('Distance', dist_mov_ave)
        [left_measure, right_measure] = car.InfraredMeasure()
        ret, frame = cap.read()
        img = cv2.flip(frame, -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
        dst = cv2.dilate(dst, None, iterations=2)
        # dst = cv2.erode(dst, None, iterations=6)
        # cv2.imshow("dst", dst)
        color = dst[300]
        black_count = np.sum(color == 0)
        black_index = np.where(color == 0)
        if black_count == 0:
            black_count = 1
            car.back(30)
            print("back")
        print("blackcount:", black_count)
        center = (black_index[0][black_count - 1] + black_index[0][0]) / 2
        direction = center - 320
        print("direction", direction)
        # decision-making
        if (start_time is None) or (time.time() - start_time > 0.5):
            start_time = None
            if left_measure == 0 and right_measure == 1:
                print("Going right, obstacle left")
                car.right(80)
                car.forward(35)
                time.sleep(0.5)
                car.left(80)
                car.forward(35)
                time.sleep(0.5)
            elif left_measure == 1 and right_measure == 0:
                print("Going left, obstacle right")
                car.left(80)
                car.forward(35)
                time.sleep(0.5)
                car.right(80)
                car.forward(35)
                time.sleep(0.5)
            else:
                if dist_mov_ave < 20:
                    car.left(80)
                    print("Left routing")
                    car.forward(45)
                    time.sleep(0.5)
                    car.right(80)
                    car.forward(35)
                    time.sleep(0.5)
                    start_time = time.time()
                elif dist_mov_ave < 100:
                    slow_down_rate = 0.7

        # line tracking
        if abs(direction) > 300:
            car.back(30)
            print("back")
        elif direction >= 0:
            if direction < 30:
                car.track_right(direction, 100/(30+direction)-0.01 * slow_down_rate)
                print("tiny right")
            else:
                if direction > 70:
                    direction = 70
                car.track_right(direction, 0.8 * slow_down_rate)
                print("right")
        elif direction < -0:
            if direction > -30:
                car.track_left(direction, 100/(30+direction)-0.01 * slow_down_rate)
                print("tiny left")
            else:
                if direction < -70:
                    direction = -70
                car.track_left(direction, 0.8 * slow_down_rate)
                print("left")

except KeyboardInterrupt as results:
    print("Measurement stopped by User")
    car.AllStop()
    cap.release()
    cv2.destroyAllWindows()
