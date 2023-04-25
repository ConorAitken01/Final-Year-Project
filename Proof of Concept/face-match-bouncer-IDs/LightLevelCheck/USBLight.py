from datetime import time

import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)
while True:
    threshold = 50
    ret, frame = cap.read()
    if ret:
        brightness = cv2.mean(frame)[0]
        print(brightness)
    if brightness < threshold:
        print('usb_light_on_command')
        cv2.waitKey(100)
    else:
        print('usb_light_off_command')

cap.release()
cv2.destroyAllWindows()

