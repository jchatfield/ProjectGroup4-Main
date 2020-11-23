# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 00:55:26 2020

@author: Dime
"""

import time
import wave
import pyaudio
import struct
import numpy as np
from scipy import interpolate



def float_to_bytes(vals):
        """ Convert a sequence of float values to 16-bit bytes """
    
        num = len(vals)
        afloats = np.array(vals)
        afloats = (afloats * 32768).astype('int')
        np.clip(afloats, -32768, 32767, out=afloats)
        return struct.pack('<{0}h'.format(num), *(aval for aval in afloats))   
    
class Signal(object):
    

    def __init__(self, num_samples=int(5*48000), amp=0.6, phase=0, harm=0):

        #self.freq =  int(2**((pitch-69)/12)*440) #convert to Hz 
        #self.pitch = pitch
        #self.skip = abs(((self.pitch-69)/12))
        self.num_samples = num_samples
        self.amp = amp
        self.phase = phase
        self.harm = harm
   
        
    @property
    def ramp(self):
       #  Generate the base cycle, a ramp from -1 to 1
        
        repeats = self.harm + 1
        normal_phase = self.phase / (2 * np.pi)
        start = normal_phase
        stop = start + repeats

        
           
        sig = np.linspace(start, stop, num= self.num_samples, dtype=np.float32)
        
        
        # wrap and shift to +/- 1
        wrap_limit = np.finfo(np.float32).eps
        sig %= 1 + wrap_limit
        sig *= 2
        sig[sig > 1] -= 2
        
        return sig
        # samples = []
        # current_sample = 0
        # while len(samples) < self.num_samples:
        #     current_sample += self.pitch
        #     current_sample = current_sample % sig.size
        #     samples.append(sig[current_sample])
        #     current_sample += 1

        # return np.array(samples)
    
    def normalize(inp):

        bias = (np.amax(inp) + np.amin(inp)) / 2
        inp -= bias
        amp = np.amax(np.absolute(inp))
    
        if amp > 0:
            inp /= amp
    
        return inp

    
    def saw(self):
        """ Generate a sawtooth """

        return self.amp * self.ramp
    
    def sin(self):
        
        return self.amp * self.cycle(np.sin(np.pi * self.ramp))
    
    def tri(self):
        """ Generate a triangle """

        # shift to start at 0
        shift = -self.num_samples // (4 * (self.harm + 1))

        return np.roll(self.amp * self.cycle((np.abs(self._base[:-1]))), shift)

    
    def cycle(self, data):
        # Generate a wave cycle and auto-interpolate as necessary
      
        try:
            dtype = type(data)
            if not isinstance(data, np.ndarray):
                data = np.array(list(data)).astype(np.float32)
        except ValueError:
            raise ValueError("Expected a sequence of data, got type {}.".format(dtype))

        if data.size == self.num_samples:
            return data
        
        new_data = np.array()
        for i in range(0, len(data)):
            new_data += data[i]

        interp_y = new_data
        num = interp_y.size
        interp_x = np.linspace(0, num, num=num)
        interp_xx = np.linspace(0, num, num=self.num_samples)
        #interp_yy = np.interp(interp_xx, interp_x, interp_y)
        tck = interpolate.splrep(interp_x, interp_y)
        interp_yy = interpolate.splev(interp_xx, tck)
        self.normalize(interp_yy)

        return interp_yy

class WaveTable(object):
    """ An n-slot wavetable """

    def __init__(self, num_slots, pitch=60, fs=48000, waves=None, wave_len=None):
        #waves is a sequence of numpy arrays

        self.num_slots = num_slots
        self.wave_len = wave_len
        self.fs = fs
        self.freq = int(2**((pitch-69)/12))*440
        self.inc = self.freq * (self.num_slots / self.fs)
      
        
        self.table = []

        if waves is not None:
            self.waves = waves
            
    @property
    def waves(self):
        """ wavetable waves """
        return self.table
    
    @waves.setter
    def waves(self, value):

        if hasattr(value, '__iter__') and value:

            if self.wave_len is None:
                self.wave_len = len(value[0])
                self.table = value
            else:
                self.table = [Signal(num_samples=self.wave_len).cycle(x) for x in value]   
    
    def clear(self):
       # Clear wavetable

        self.waves = []
        
    def get_index(self, index):


        if self.wave_len is None:
            if self.waves:
                self.wave_len = len(self.table[0])
            else:
                raise ValueError("Set wave_len or waves before calling get_index")

        if index >= len(self.waves):
            return np.zeros(self.wave_len)

        return Signal(num_samples=self.wave_len).cycle(self.table[index])

    def get_waves(self):
       #return all waves loaded on table
       
           table = []

           for i in range(self.num_slots):
               table.append(self.get_index(i))
               
           return table

            
    #Reads and returns at most n frames of audio, as a bytes object. (Relative to 1Hz)
    def readpitch(self, n): 
        inc = self.inc #increment
        table = self.get_waves
        
        x= np.linspace(0, len(table), n)
        y= table
        p = [] #have to add new skipped samples to p one-by-one
        for i in range(0, len(table), inc):
            p = p.append(table[i])
            
        px = np.linspace(0, len(p), n)   
        weighted = np.interp(px, x, y)
        
        new = float_to_bytes(weighted)
        
        return new 
    
    def write(self, samplerate=48000):
        """ Write table to audio stream """
        fs = self.fs
        sig = np.array(list(self.get_waves()))
        #table = float_to_bytes(sig)
        
        # Create an interface to PortAudio
        p = pyaudio.PyAudio()
        
        # define callback
        def callback(in_data, frame_count, time_info, status):
            data = sig.readpitch(frame_count) #have to write my own readframes
            return (data, pyaudio.paContinue)
        
        # open stream using callback
        stream = p.open(format=p.get_format_from_width(2),
                channels=2,
                rate= fs,
                output=True,
                stream_callback=callback)
        
    
        # start the stream (4)
        stream.start_stream()


            
        # Close and terminate the stream
        #stream.stop_stream()

      
        #p.terminate()
        
        print("Created audio")