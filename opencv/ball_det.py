import cv2
import numpy as np


cap = cv2.VideoCapture('volleyball_match.mp4')


lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))


template = cv2.imread('pic4.png', cv2.IMREAD_GRAYSCALE)


ret, old_frame = cap.read()
old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)


mask = np.zeros_like(old_frame)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    
    res = cv2.matchTemplate(frame_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    
    ball_center = (max_loc[0] + template.shape[1] // 2, max_loc[1] + template.shape[0] // 2)

    
    p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, np.array([ball_center], dtype=np.float32), None, **lk_params)

    
    for i, (new, old) in enumerate(zip(p1, np.array([ball_center], dtype=np.float32))):
        a, b = new.ravel()
        c, d = old.ravel()
        mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)), (0, 255, 0), 2)
        frame = cv2.circle(frame, (int(a), int(b)), 5, (0, 255, 0), -1)

    img = cv2.add(frame, mask)

    
    cv2.imshow('Ball Tracking', img)

    
    old_gray = frame_gray.copy()

    
    if cv2.waitKey(30) & 0xFF == 27:
        break


cap.release()
cv2.destroyAllWindows()
