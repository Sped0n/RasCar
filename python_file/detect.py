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
            colorR_hsv = cv2.inRange(hsv, color_dist[colorR]['Lower'], color_dist[colorR]['Upper']) + cv2.inRange(hsv, color_dist[colorRP]['Lower'], color_dist[colorRP]['Upper'])
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
                maxR = 0
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    #if i[2] > maxR:
                    maxR = int(i[2])
                    maxX = int(i[0])
                    maxY = int(i[1])
                # detect area constrain
                    if (maxY - maxR) < 0 or (maxX - maxR) < 0:
                        detect_area = None
                    elif (maxY + maxR) > 480 or (maxX +maxR) >640:
                        detect_area = None
                    else:
                        detect_area = (hsv[maxY - maxR:maxY + maxR, maxX - maxR:maxX + maxR])
                    if detect_area is not None:
                        max_circ_area = maxR * maxR * 4
                        # red filter
                        red_mask = cv2.inRange(detect_area, color_dist[colorR]['Lower'],
                                           color_dist[colorR]['Upper']) + cv2.inRange(detect_area,
                                                                                      color_dist[colorRP]['Lower'],
                                                                                      color_dist[colorRP]['Upper'])
                        red_num_point = np.sum(red_mask / 255)
                        Rrate = red_num_point / (maxR * maxR * 4)
                        # green filter
                        green_mask = cv2.inRange(detect_area, color_dist[colorG]['Lower'], color_dist[colorG]['Upper'])
                        green_num_point = np.sum(green_mask / 255)
                        Grate = green_num_point / max_circ_area
                        # blue filter
                        blue_mask = cv2.inRange(detect_area, color_dist[colorB]['Lower'], color_dist[colorB]['Upper'])
                        blue_num_point = np.sum(blue_mask / 255)
                        Brate = blue_num_point / max_circ_area
                        if Rrate > all_rate:
                            cv2.circle(frame, (maxX, maxY), maxR, (255, 0, 0), 2)
                            cv2.circle(frame, (maxX, maxY), 2, (255, 255, 0), 3)
                            Rarea = pi * maxR * maxR
                            print("Red", Rarea)
                        if Grate > all_rate:
                            cv2.circle(frame, (maxX, maxY), maxR, (0, 0, 255), 2)
                            cv2.circle(frame, (maxX, maxY), 2, (0, 0, 255), 3)
                            Garea = pi * maxR * maxR
                            print("Green", Garea)
                        if Brate > all_rate:
                            cv2.circle(frame, (maxX, maxY), maxR, (0, 255, 0), 2)
                            cv2.circle(frame, (maxX, maxY), 2, (0, 255, 0), 3)
                            Barea = pi * maxR * maxR
                            print("Blue", Barea)

        cv2.imshow('camera', frame)
        cv2.waitKey(1)

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()
