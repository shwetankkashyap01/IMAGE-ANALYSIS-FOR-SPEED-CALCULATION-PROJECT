# version 2 Jan 3:48 pm, done with the speed part, till now the best version for that downloaded video

import numpy as np
import cv2
import time

detected = []
offset = 1
line_pos = 150
count = 0
speed =str(0)

def speed_cal(count):
    spd = count*0.602*3.6
    return spd


def cen(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx,cy

cap = cv2.VideoCapture('video_download2.mp4')
tm1 = int(time.time_ns() / (10 ** 9))

while(True):
    tm2 = int(time.time_ns() / (10 ** 9))
    _, frame = cap.read()
    frame1 = cv2.GaussianBlur(frame,(9,9),5)
    hsv = cv2.cvtColor(frame1, cv2.COLOR_BGR2HSV)
    
    l_b = np.array([0, 0, 160])
    u_b = np.array([255, 255, 255])
    
    mask = cv2.inRange(hsv, l_b, u_b)
    res = cv2.bitwise_and(frame, frame, mask = mask)
    
    kernel = np.ones((3,3), np.uint8)
    erosion = cv2.erode(mask, kernel, iterations=1)
    dilation = cv2.dilate(mask, kernel, iterations=1)
    
    res2 = cv2.bitwise_and(frame, frame, mask=erosion)
    res3 = cv2.bitwise_and(frame, frame, mask=dilation)
    
    contours, _ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.line(frame, (80, line_pos), (440, line_pos), (255,127,0), 3)
    
    for(i,c) in enumerate(contours):
        (x, y, w, h) = cv2.boundingRect(c)
        if cv2.contourArea(c) < 1000:
            continue
        cent = cen(x, y, w, h)
        detected.append(cent)
        cv2.circle(frame, cent, 4, (0, 0,255), -1)
        
        for (x,y) in detected:
            if y in range(line_pos-offset, line_pos+offset, 1) and x in range(150, 350):
                count+=1
                detected.remove((x,y))
                cv2.line(frame, (80, line_pos), (440, line_pos), (255,255,255), 3)
                print("sleeper detected : "+str(count))
    
    if (abs(tm2-tm1) ==1):
        spd = speed_cal(count)
        count = 0
        print(spd," Km/h")
        tm1 = int(time.time_ns() / (10 ** 9))
        speed = str('%.2f' % spd) + ' Km/hr'
 
    cv2.imshow('frame', frame)
    cv2.imshow('mask', dilation)
    if cv2.waitKey(40) == 27:
        break

cap.release()
cv2. destroyAllWindows()
        