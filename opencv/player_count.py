import cv2
import numpy as np

cap = cv2.VideoCapture('volleyball_match.mp4')

ret, frame1 = cap.read()
ret, frame2 = cap.read()


lower_bound1 = np.array([0, 0, 79])
upper_bound1 = np.array([82, 246, 237])

lower_bound2 = np.array([125, 147, 120])
upper_bound2 = np.array([255, 255, 255])

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    count1 = 0  
    count2 = 0  

    for contour in contours:
        if cv2.contourArea(contour) < 1000:
            continue

        (x, y, w, h) = cv2.boundingRect(contour)

        
        roi = frame1[y:y+h, x:x+w]
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        avg_hsv = np.mean(hsv_roi, axis=(0, 1))

        
        if np.all(avg_hsv >= lower_bound1) and np.all(avg_hsv <= upper_bound1):
            color = (0, 255, 0)  
            count1 += 1
        elif np.all(avg_hsv >= lower_bound2) and np.all(avg_hsv <= upper_bound2):
            color = (0, 0, 255)  
            count2 += 1
        else:
            color = (255, 0, 0)  

        cv2.rectangle(frame1, (x, y), (x+w, y+h), color, 2)

    
    cv2.putText(frame1, f'Class 1: {count1}', (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.putText(frame1, f'Class 2: {count2}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    cv2.imshow('inter', frame1)

    frame1 = frame2 
    ret, frame2 = cap.read()

    if cv2.waitKey(30) & 0xFF == 27:
        break

cv2.destroyAllWindows()
cap.release()
