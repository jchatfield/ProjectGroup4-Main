import pyaudio
import numpy as np
import time

#script using pyaudio to create a waveform and play it per frame using the
#analyzed features from the video
#Using R,G,B for frequency and brightness for volume
p = pyaudio.PyAudio()


# for paFloat32 sample values must be in range [-1.0, 1.0]
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                output=True)




#actual synth function
#creates a waveform per frame and uses analyzed values to create it
#this function is called once per frame
#creates three different wavetables whos frequency is dependent on the red,green,and blue values. They are then
#added together to give the synth more depth.
def playsynth(f1,f2,f3,volume):
    volume = volume   # range [0.0, 1.0]
    fs = 44100       # sampling rate, Hz, must be integer
    duration = 1/6   # in seconds, may be float
    table = (np.sin(2*np.pi*np.arange(fs*duration)*f1/fs)).astype(np.float32)
    table2 = (np.sin(2*np.pi*np.arange(fs*duration)*f2/fs)).astype(np.float32)
    table3 = (np.sin(2*np.pi*np.arange(fs*duration)*f3/fs)).astype(np.float32)
    newtable = (table+table2+table3)/3
    # play. May repeat with different volume values (if done interactively)
    stream.write(volume*newtable)






#ending function that can be called when the q key is pressed or when the video ends
#will end the audio streaming and video and close the video frame.
def end():
    stream.stop_stream()
    stream.close()
    p.terminate()
