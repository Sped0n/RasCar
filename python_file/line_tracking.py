import RPi.GPIO as GPIO
import cv2
import time
import numpy as np
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
center = 320
cap = cv2.VideoCapture(0)
# center定义



try:
    while (1):
        ret, frame = cap.read()
        img = cv2.flip(frame, -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
        dst = cv2.dilate(dst, None, iterations=2)
        # dst = cv2.erode(dst, None, iterations=6)
        # cv2.imshow("dst", dst)
        color = dst[300]
        try:
            black_count = np.sum(color == 0)
            black_index = np.where(color == 0)
            if black_count == 0:
                black_count = 1
            print("blackcount:", black_count)
            center = (black_index[0][black_count - 1] + black_index[0][0]) / 2
            direction = center - 320
            print("direction", direction)
        except:
            continue
        if abs(direction) > 300:
            car.brake()
            print("break")
        elif direction >= 0:
            if direction <30:
                car.track_right(direction, 1.5)
            else:
                if direction > 70:
                    direction = 70
                car.track_right(direction, 1)
            print("right")
        elif direction < -0:
            if direction > -30:
                car.track_left(direction, 1.5)
            else:
                if direction < -70:
                    direction = -70
                car.track_left(direction,1)
            print("left")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt as result:
    cap.release()
    cv2.destroyAllWindows()
    car.AllStop()
