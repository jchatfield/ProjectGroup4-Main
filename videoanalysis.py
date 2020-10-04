import ffmpeg
import numpy as np
import cv2

#video = directory pathway to video file
def Analyze(video):
    #setting up video capture object and np arrays (webcam right now for testing video data)
    meanRed = np.array([])
    meanGreen = np.array([])
    meanBlue = np.array([])
    meanEntropy = np.array([])
    meanBrightness = np.array([])

    cap = cv2.VideoCapture(video)
    #print(cap.isOpened())

    #looping through each frame of video
    while(cap.isOpened()):
        ret, frame = cap.read()
        #Video analysis operations will go here
        #mean BGRA values
        #mean "brightness" (average of the average grayscale values per frame)
        if ret == True:
            bgr = cv2.mean(frame)
            grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            brightness = np.mean(grayscale)
            marg = np.histogramdd(np.ravel(frame), bins = 256)[0]/frame.size
            marg = list(filter(lambda p: p > 0, np.ravel(marg)))
            entropy = -np.sum(np.multiply(marg, np.log2(marg)))

            meanRed = np.append(meanRed,bgr[2])
            meanGreen = np.append(meanRed,bgr[1])
            meanBlue = np.append(meanRed,bgr[0])
            meanEntropy = np.append(meanEntropy,entropy)
            meanBrightness = np.append(meanBrightness,brightness)


            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    #releasing captured video data and destroying the window (for testing)
    cap.release()
    cv2.destroyAllWindows()
    print(meanRed,meanBlue,meanGreen,meanBrightness,meanEntropy)
    return meanRed,meanBlue,meanGreen,meanBrightness,meanEntropy



meanbgr,meanbrightness = Analyze(0)
