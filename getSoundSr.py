# -*- coding = uft-8 -*-
# @Time : 2021-07-19 15:34
# @Author : yzbyx
# @File : getSoundSr.py
# @Software : PyCharm
from pydub import AudioSegment


class getSr:
    _path = ""
    sound = 0

    def __init__(self, path):
        self._path = path
        self.sound = AudioSegment.from_file(self._path, format="wav")

    def sr(self):
        return self.sound.frame_rate


if __name__ == '__main__':
    c = getSr(r".\resources\output5\ReStarting\vocals.wav")
    print(c.sr())
