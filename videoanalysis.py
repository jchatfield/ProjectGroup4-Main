import ffmpeg
import numpy as np
import cv2


#setting up video capture object (webcam right now for testing video data)
cap = cv2.VideoCapture(0)


print(cap.isOpened())


#looping through each frame of video
while(cap.isOpened()):
    ret, frame = cap.read()

    #Video analysis operations will go here
    if ret == True:
        meanbgr = cv2.mean(frame)
        print(meanbgr)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break


#releasing captured video data and destroying the window (for testing)
cap.release()
cv2.destroyAllWindows()
