import ffmpeg
import numpy as np
import cv2

#video = directory pathway to video file
def Analyze(video):
    #setting up video capture object (webcam right now for testing video data)
    cap = cv2.VideoCapture(video)
    #print(cap.isOpened())

    #looping through each frame of video
    while(cap.isOpened()):
        ret, frame = cap.read()
        #Video analysis operations will go here
        #mean BGRA values
        #mean "brightness" (average of the average grayscale values per frame)
        if ret == True:
            meanbgr = cv2.mean(frame)
            grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            meanbrightness = np.mean(grayscale)
            #print(meanbrightness)
            #print(meanbgr)
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    #releasing captured video data and destroying the window (for testing)
    cap.release()
    cv2.destroyAllWindows()
    print(meanbgr,meanbrightness)
    return meanbgr, meanbrightness




meanbgr,meanbrightness = Analyze(0)
