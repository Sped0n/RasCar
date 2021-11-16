import cv2
cap1=cv2.VideoCapture(0)
width=640
height=480
cap1.set(cv2.CAP_PROP_FRAME_WIDTH,width)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT,height)
while True:
    ret1,frame1=cap1.read()
    print(ret1)
    img1=cv2.flip(frame1,-1)
    img=cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    cv2.imshow("img",img)
    cv2.imshow("img1",img1)

    input=cv2.waitKey(20)
    if input==ord('q'):
        break

cap1.release()
cv2.destroyAllWindows()
