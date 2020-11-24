import numpy as np
import synth
import cv2
import videoanalysis
import math
import wave
import pyaudio
import othertest
from scipy import interpolate


#p is the video player function that will be used to play the synth in the
#main function
#p = pyaudio.PyAudio()
#def playAudio(p,param1,param2,param3,sr):

    #volume = param2/2     # range [0.0, 1.0]
    #fs = 44100       # sampling rate, Hz, must be integer
    #duration = 1/sr # in seconds, may be float
    #f = param1*10 + param3*20        # sine frequency, Hz, may be float

    # generate samples, note conversion to float32 array
    #samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    #stream = p.open(format=pyaudio.paFloat32,
                    #channels=1,
                    #rate=fs,
                    #output=True)

    # play. May repeat with different volume values (if done interactively)
    #stream.write(volume*samples)

    #stream.stop_stream()


#MAIN function that loops through the video,analyzes, and plays audio
#video = directory pathway to video file
def MAIN(video):
    #looping through each frame of video
    cap = cv2.VideoCapture(video)
    framerate = cap.get(cv2.CAP_PROP_FPS)
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            meanRed,meanBlue,meanGreen,meanBrightness,meanEntropy = videoanalysis.Analyze(frame)
            meanBrightness = videoanalysis.Normalize(meanBrightness,0,255,21,128)


            #playAudio(p,meanBlue,meanEntropy,meanRed,framerate)




            cv2.imshow('frame', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break


    cap.release()
    cv2.destroyAllWindows()


video = "oops.mp4"
MAIN(video)
