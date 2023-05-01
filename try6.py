# try 6, version 2 Jan 7:07 pm, this version is based on try 4, adding program to calculate the speed.
# best till now (3 Jan, 2:09am), try6 for video 8 and try5 for vidoe_dwonload2, removing th ecommented part from this, find it in try 4.

import numpy as np
import cv2
import time

def cen(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

detected = []
offset = 8
line_pos = 395
count = 0
speed = str(0)

def speed_cal(count):
    spd = count*0.602*3.6
    return spd

cap = cv2.VideoCapture('video8.mp4')
tm1 = int(time.time_ns() / (10**9))

j=198

while cap.isOpened():
    tm2 = int(time.time_ns() / (10**9))
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    _, thresh = cv2.threshold(blur, j, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((1, 1), np.uint8)
    erosion = cv2.erode(thresh, kernel, iterations=1)
    dilation = cv2.dilate(thresh, kernel, iterations=1)

    gblur = cv2.GaussianBlur(dilation, (3, 3), 0)
    median = cv2.medianBlur(dilation, 3)
    
    contours, _ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame, (10, line_pos), (200, line_pos), (255,127,0), 3)
    
    for(i,c) in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(c)
        if cv2.contourArea(c) < 1000:
            continue
        cent = cen(x, y, w, h)
        detected.append(cent)
        cv2.circle(frame, cent, 4, (0, 0,255), -1)
        
    
    for (x,y) in detected:
        if y in range(line_pos-offset, line_pos+offset, 1) and  x in range(10,200):
            count += 1
            detected.remove((x, y))
            print("sleeper detected : "+str(count))
    
    if (abs(tm2-tm1) ==2):
        spd = speed_cal(count)/2
        count = 0
        print(spd," Km/h")
        tm1 = int(time.time_ns() / (10 ** 9))
        speed = str('%.2f' % spd) + ' Km/hr'
    
    cv2.rectangle(frame, (120, 5), (240, 40), (0, 255, 255), -1)
    cv2.putText(frame, speed, (125,30), cv2.FONT_HERSHEY_SIMPLEX,.5, (0,255,0), 1, cv2.LINE_AA)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', median)

    if cv2.waitKey(40) == 27:
        break

cap.release()
cv2.destroyAllWindows()