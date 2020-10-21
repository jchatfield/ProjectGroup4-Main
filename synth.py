# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 00:55:26 2020

@author: Dime
"""

import math
import wave
import pyaudio
import struct
import numpy as np
from scipy import interpolate



def float_to_bytes(vals):
        """ Convert a sequence of vals to 16-bit bytes """
    
        num = len(vals)
        afloats = np.array(vals)
        afloats = (afloats * 32768).astype('int')
        np.clip(afloats, -32768, 32767, out=afloats)
        return struct.pack('<{0}h'.format(num), *(aval for aval in afloats))   
    
class Signal(object):
    

    def __init__(self, num_samples=128, amp=0.7, phase=0, harm=0, pitch=69):

        self.pitch =  int(2**((pitch-69)/12)*440) #Hz 
        skip = abs(((self.pitch-69)/12))
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
        shift = -self.num_points // (4 * (self.harmonic + 1))

        return np.roll(self.amp * self.arb((np.abs(self._base[:-1]))), shift)

    
    def cycle(self, data):
        # Generate a wave cycle and auto-interpolate as necessary depending on frequency
      
        try:
            dtype = type(data)
            if not isinstance(data, np.ndarray):
                data = np.array(list(data)).astype(np.float32)
        except ValueError:
            raise ValueError("Expected a sequence of data, got type {}.".format(dtype))

        if data.size == self.num_samples:
            return data
        
        new_data = np.array()
        for i in range(0, len(data), 1+skip):
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

    def __init__(self, num_slots, pitch=60, fs=44100, waves=None, wave_len=None):
        #waves is a sequence of numpy arrays

        self.num_slots = num_slots
        self.wave_len = wave_len
        self.pitch = pitch
        self.fs = fs
        
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

        for i in range(self.num_slots):
            yield self.get_index(i)
    
   
    # def write(self, filename, samplerate=44100):
    #     # #Write wavetable to file
    #     # #Make sure filename has .wav extension
    #     for i_waves in 
    #     all = np.array(self.get_waves)
                
    #     wave_file = wave.open(filename, 'w')
    #     wave_file.setnchannels(1)
    #     wave_file.setsampwidth(4)
    #     wave_file.setframerate(samplerate)
        

    #     # for i_wave in self.get_waves():
    #     wave_file.writeframes(bytes(all))   
    #     wave_file.close()
    def write(wavetable, filename, samplerate=44100):
        """ Write wavetable to file """

        wave_file = wave.open(filename, 'w')
        wave_file.setframerate(samplerate)
        wave_file.setnchannels(1)
        wave_file.setsampwidth(2)
        
        for wt_wave in wavetable.get_waves():
            wave_file.writeframes(float_to_bytes(wt_wave))
       
        wave_file.close()
            
   
        # Set chunk size of 1024 samples per data frame
        chunk = 128
    
        
        # Open the sound file 
        wf = wave.open(filename, 'rb')
        
        # Create an interface to PortAudio
        p = pyaudio.PyAudio()
        
        # Open a .Stream object to write the WAV file to
        # 'output = True' indicates that the sound will be played rather than recorded
        stream = p.open(format = pyaudio.paFloat32,
                        channels = 1,
                        rate = samplerate,
                        output = True)
        
        # Read data in chunks
        data = wf.readframes(chunk)
        
        # Play the sound by writing the audio data to the stream
        while True:
            if data != '':
                stream.write(data)
                data = wf.readframes(chunk)
            if data == b'':
                break
            
        # Close and terminate the stream
        wf.close()
        stream.stop_stream()
        stream.close()
      
        p.terminate()
        
        print("Created " + filename)