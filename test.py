# -*- coding = uft-8 -*-
# @Time : 2021-07-21 10:09
# @Author : yzbyx
# @File : test.py
# @Software : PyCharm

# Beat tracking example
# from __future__ import print_function
import librosa
import matplotlib.pyplot as plt
import librosa.display
import numpy as np

# 1. Get the file path to the included audio example
# Sonify detected beat events
y, sr = librosa.load(r"./resources/output5/ReStarting/vocals.wav", sr=None)
tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
y_beats = librosa.clicks(frames=beats, sr=sr)

# Or generate a signal of the same length as y
y_beats = librosa.clicks(frames=beats, sr=sr, length=len(y))

# Or use timing instead of frame indices
times = librosa.frames_to_time(beats, sr=sr)
y_beat_times = librosa.clicks(times=times, sr=sr)

# Or with a click frequency of 880Hz and a 500ms sample
y_beat_times880 = librosa.clicks(times=times, sr=sr,
                                 click_freq=880, click_duration=0.5)

# Display click waveform next to the spectrogram
plt.figure()
S = librosa.feature.melspectrogram(y=y, sr=sr)
ax = plt.subplot(2, 1, 2)
librosa.display.specshow(librosa.power_to_db(S, ref=np.max),
                         x_axis='time', y_axis='mel')
plt.subplot(2, 1, 1, sharex=ax)
librosa.display.waveplot(y_beat_times, sr=sr, label='Beat clicks')
plt.legend()
plt.xlim(15, 30)
plt.tight_layout()
