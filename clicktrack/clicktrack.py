import matplotlib.pyplot as plt

from functions import TempoFunction
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

BAR_LENGTH = 4

fs = 44100

def get_click(freq):
    click = np.arange(3000, dtype=float)
    click *= freq / fs
    click = np.sin(click[:])
    han = np.hanning(len(click) * 2)
    click *= han[-len(click):]
    
    return click

def make_click_track(functions: list[TempoFunction], dest_file:str):
    beats = []
    for f in functions:
        b = f.get_beats()
        beats += b
    a = np.zeros(int(functions[-1].end.time * fs))
    
    click_high = get_click(3000) * 0.5
    
    bar = 0
    for b in beats:
        
        a[int(b.time * fs)] = (1-int(bar % BAR_LENGTH > 0)) *0.95+0.05
        bar += 1
    wavfile.write(dest_file, fs, np.convolve(a, click_high))
    return beats
