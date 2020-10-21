# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 09:52:20 2020

@author: Dime
"""

import synth
import graph



sg = synth.Signal()

wt = synth.WaveTable(1024)
wt.clear()
s = synth.Signal().sin()
s2 = synth.Signal().saw()
wt.waves = ([s]*1024) 

wt.write('test.wav')

graph.plot_wave(s)