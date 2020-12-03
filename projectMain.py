import numpy as np
import synth
import cv2
import videoanalysis
import math
import wave
import pyaudio
from scipy import interpolate


#MAIN function that loops through the video,analyzes, and plays audio
#video = directory pathway to video file
def MAIN(video):
    #looping through each frame of video
    cap = cv2.VideoCapture(video)
    framerate = cap.get(cv2.CAP_PROP_FPS)

    #if there is an open frame, then analyze it:
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            meanRed,meanBlue,meanGreen,meanBrightness,meanEntropy = videoanalysis.Analyze(frame)
            meanBlue = videoanalysis.Normalize(meanBlue,0,255,55,110)
            meanRed = videoanalysis.Normalize(meanRed,0,255,55,110)
            meanGreen = videoanalysis.Normalize(meanGreen,0,255,55,110)
            midi1 = round(meanRed)
            midi2 = round(meanBlue)
            midi3 = round(meanGreen)
            freq1 = 2**((midi1-69)/12)*440
            freq2 = 2**((midi2-69)/12)*440
            freq3 = 2**((midi3-69)/12)*440
            volume = videoanalysis.Normalize(meanBrightness,0,255,0,1)
            synth.playsynth(freq1,freq2,freq3,volume)


            #little function that ends stuff when you press the q key
            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                synth.end()
                break
        else:
            break


    cap.release()
    cv2.destroyAllWindows()


video = "finalvid.mp4"
MAIN(video)
