import numpy as np
import cv2
import math
from scipy import interpolate
#This function analyzes a single video frame and outputs 5
#different video features, meanRGB, brightness, and entropy
#The function will be used once per video frame and then output
#to the synth function


def Analyze(frame):
    bgr = cv2.mean(frame)
    grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    brightness = np.mean(grayscale)
    marg = np.histogramdd(np.ravel(frame), bins = 256)[0]/frame.size
    marg = list(filter(lambda p: p > 0, np.ravel(marg)))
    entropy = -np.sum(np.multiply(marg, np.log2(marg)))

    meanRed = bgr[2]
    meanGreen = bgr[1]
    meanBlue = bgr[0]
    meanEntropy = entropy
    meanBrightness = brightness
    return meanRed,meanBlue,meanGreen,meanBrightness,meanEntropy




#normalization function given known max and min values and known new max and new min values
#using to map known values from the video parameters to a different set of values.
#RGB is mapped to midi which is then converted to frequency, brightness is mapped to volume (0 - 1)
def Normalize(value,min,max,newmin,newmax):
    normalized = (newmax-newmin)/(max-min)*(value-max) + newmax
    return normalized
