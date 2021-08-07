# -*- coding = uft-8 -*-
# @Time : 2021-07-09 20:20
# @Author : yzbyx
# @File : bpmAnalysis.py
# @Software : PyCharm

import librosa
import getSoundSr


def analysis(f):
    y, sr = librosa.load(f)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=getSoundSr.getSr(filePath).sr)
    return tempo


if __name__ == '__main__':
    filePath = "./resources/ReStarting.wav"
    print(analysis(filePath))
