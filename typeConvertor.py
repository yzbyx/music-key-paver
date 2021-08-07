# -*- coding = uft-8 -*-
# @Time : 2021-07-19 15:41
# @Author : yzbyx
# @File : typeConvertor.py
# @Software : PyCharm

from pydub import AudioSegment


class convertor:
    _path = ""
    _name = ""
    sound = 0

    def __init__(self, path):
        self._path = path
        self.sound = AudioSegment.from_file(self._path, format="mp3")

    def convert(self, targetType="wav"):
        self._name = self._path.split("/")[-1].split(".")[0]
        self.sound.export(r"./resources/" + self._name + "." + targetType, format="wav")


if __name__ == '__main__':
    c = convertor(r"./resources/MEGALOVANIA.mp3")
    c.convert()
    # print(c.sound)
