 # -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 09:52:20 2020

@author: Dime
"""

import synth
import graph



sg = synth.Signal()
frames= 100 #frames*128 = total samples
pitch= 60

wt = synth.WaveTable(frames, pitch=70)
s = synth.Signal().sin()

wt.waves = ([s]*int(frames))

wt.write('test.wav')

graph.plot_wavetable(wt)

