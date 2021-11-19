import cv2
import numpy as np

colorY = 'yellow'
colorR = 'red'
colorRP = 'red1'
colorG = 'green'
colorB = 'blue'
pi = 3.1415926
all_rate = 0.65  # the color select rate
circularity = 95  # hough circularity, the higher it is, the more accurate it is.
hough_params_2 = 25  # The parameter is set according to the size of the circle in your image. When the circle in
# this image is smaller, then this value should be set smaller. When the setting is smaller, then more circles are
# detected and a lot of noise is generated when larger circles are detected. So it should be changed according to the
# size of the detected circle

color_dist = {'red': {'Lower': np.array([0, 60, 60]), 'Upper': np.array([10, 255, 255])},
              'red1': {'Lower': np.array([156, 60, 60]), 'Upper': np.array([180, 255, 255])},
              'blue': {'Lower': np.array([100, 43, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              'yellow': {'Lower': np.array([26, 43, 46]), 'Upper': np.array([34, 255, 255])}
              }

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cv2.namedWindow('camera', cv2.WINDOW_AUTOSIZE)  # 测试

while (1):
    ret, frame = cap.read()
    if ret:
        if frame is not None:
            # grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)
            # dst = cv2.pyrMeanShiftFiltering(frame, 10, 100)
            grey = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2GRAY)
            hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)
            hsv = cv2.erode(hsv, None, iterations=2)
            colorY_hsv = cv2.inRange(hsv, color_dist[colorY]['Lower'], color_dist[colorY]['Upper'])
            Ycnts = cv2.findContours(colorY_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            circles = cv2.HoughCircles(grey, cv2.HOUGH_GRADIENT, 1, circularity, param1=100, param2=hough_params_2,
                                       minRadius=10, maxRadius=80)
            # rec detect
            if Ycnts:
                maxcnt = max(Ycnts, key=cv2.contourArea)
                rect = cv2.minAreaRect(maxcnt)
                box = cv2.boxPoints(rect)
                area = cv2.contourArea(box)
                # print(area)
                cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)

            if circles is not None:
                x = circles[0][:, 0].astype(int)
                y = circles[0][:, 1].astype(int)
                r = circles[0][:, 2].astype(int)
                num = circles[0].shape[0]
                rate = np.zeros(num)
                for i in range(num):  # traverse all detected circles
                    detect_area = (hsv[y[i]-r[i]: y[i]+r[i], x[i]-r[i]:x[i]+r[i]])  # A square in the detected circle
                    height, width, channel = detect_area.shape
                        # red filter
                    if height !=0 and width !=0:
                        red_mask = cv2.inRange(detect_area, color_dist[colorR]['Lower'],
                                           color_dist[colorR]['Upper']) + cv2.inRange(detect_area,
                                                                                      color_dist[colorRP]['Lower'],
                                                                                      color_dist[colorRP]['Upper'])
                        red_num_point = np.sum(red_mask / 255)
                        Rrate = red_num_point / (height * width)
                        # green filter
                        green_mask = cv2.inRange(detect_area, color_dist[colorG]['Lower'], color_dist[colorG]['Upper'])
                        green_num_point = np.sum(green_mask / 255)
                        Grate = green_num_point / (height * width)
                        # blue filter
                        blue_mask = cv2.inRange(detect_area, color_dist[colorB]['Lower'], color_dist[colorB]['Upper'])
                        blue_num_point = np.sum(blue_mask / 255)
                        Brate = blue_num_point / (height * width)
                        if Rrate > all_rate:
                            cv2.circle(frame, (x[i], y[i]), r[i], (255, 0, 0), 2)
                            cv2.circle(frame, (x[i], y[i]), 2, (255, 255, 0), 3)
                            Rarea = pi * r[i] * r[i]
                            print("Red", Rarea)
                        if Grate > all_rate:
                            cv2.circle(frame, (x[i], y[i]), r[i], (0, 0, 255), 2)
                            cv2.circle(frame, (x[i], y[i]), 2, (0, 0, 255), 3)
                            Garea = pi * r[i] * r[i]
                            print("Green", Garea)
                        if Brate > all_rate:
                            cv2.circle(frame, (x[i], y[i]), r[i], (0, 255, 0), 2)
                            cv2.circle(frame, (x[i], y[i]), 2, (0, 255, 0), 3)
                            Barea = pi * r[i] * r[i]
                            print("Blue", Barea)

        cv2.imshow('camera', frame)
        cv2.waitKey(1)

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
