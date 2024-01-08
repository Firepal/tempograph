import matplotlib.pyplot as plt

from functions import TempoFunction
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt

fs = 44100
click_sound = np.arange(1000, dtype=float)
click_sound *= 3000 / fs
click_sound = np.sin(click_sound[:1000])
han = np.hanning(len(click_sound) * 2)
click_sound *= np.hanning(len(click_sound) * 2)[-len(click_sound):]
click_sound *= 0.7

def make_click_track(functions: list[TempoFunction], dest_file:str):
    beats = []
    for f in functions:
        b = f.get_beats()
        beats += b
    a = np.zeros(int(functions[-1].end.time * fs))
    for b in beats:
        a[int(b.time * fs)] = 1
    wavfile.write(dest_file, fs, np.convolve(a, click_sound))
    return beats
