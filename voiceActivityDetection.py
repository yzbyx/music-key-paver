# -*- coding = uft-8 -*-
# @Time : 2021-07-18 23:11
# @Author : yzbyx
# @File : voiceActivityDetection.py
# @Software : PyCharm
# 短时能量和过零率的双门限端点检测
import os
import warnings
import wave

import librosa
from matplotlib import pyplot as plt

import getSoundSr
import numpy as np

warnings.filterwarnings('ignore')


# 计算每一帧的能量
def calEnergy(wave_data, segment, panning, sr):
    segment_frame = int(segment * sr / 1000)
    panning_frame = int(panning * sr / 1000)
    energy = []
    s = 0
    i = 0
    temp = 0  # 用于确定是否达到一帧的数据长度
    while i < len(wave_data):
        if temp == segment_frame:
            i = i - (segment_frame - panning_frame)
            temp = 0
            energy.append(s)
            s = 0
        elif i == len(wave_data) - 1:
            energy.append(s)
        s = s + pow(wave_data[i], 2)
        i = i + 1
        temp = temp + 1
    return energy


def showImage(data, panning=20., title=None):
    plt.rcParams['figure.dpi'] = 1000
    time = [j * panning / 1000 for j in range(len(data))]
    plt.plot(time, data, linewidth=0.5)
    plt.title(title)
    # plt.show()


# 自定义函数，计算数值的符号。
def sgn(data):
    if data >= 0:
        return 1
    else:
        return 0


class VAD:
    _fileList = []

    def __init__(self, path):
        self.segment = 35  # 分段25ms
        self.panning = 20  # 平移10ms
        self.path = path
        self.energy = []
        self.zeroCrossingRate = []
        self.y, self.sr = librosa.load(self.path, sr=getSoundSr.getSr(self.path).sr())
        self.time = [i / self.sr for i in range(len(self.y))]

    def scanFile(self):
        dirPath = self.path.split("/")
        dirPath.pop()  # 弹出最后一个元素
        dirPathTemp = dirPath
        dirPath = "./"
        for i in range(len(dirPathTemp)):
            dirPath = dirPath + dirPathTemp[i]
            if i < len(dirPathTemp):
                dirPath = dirPath + "/"
        self._fileList = os.listdir(dirPath)
        return self._fileList

    # 短时能量 short time energy
    def STE(self):
        self.energy = calEnergy(self.y, self.segment, self.panning, self.sr)
        return self.energy

    # 过零率 zero cross counter
    def ZCC(self):
        self.zeroCrossingRate = []
        s = 0
        for i in range(len(self.y)):
            sample_num = int(self.segment * self.sr / 1000)
            s = s + np.abs(sgn(self.y[i]) - sgn(self.y[i - 1]))
            if i % sample_num == 0:
                self.zeroCrossingRate.append(float(s) / (sample_num - 1))
                s = 0
            elif i == len(self.y) - 1:
                self.zeroCrossingRate.append(float(s) / (sample_num - 1))
        return self.zeroCrossingRate

    def merge(self):
        plt.subplot(4, 1, 1)
        plt.plot(self.time, self.y)
        plt.subplot(4, 1, 2)
        f = wave.open(self.path, "rb")
        # getparams() 一次性返回所有的WAV文件的格式信息
        params = f.getparams()
        # nframes 采样点数目
        nchannels, sampwidth, framerate, nframes = params[:4]
        # readframes() 按照采样点读取数据
        str_data = f.readframes(nframes)  # str_data 是二进制字符串

        # 以上可以直接写成 str_data = f.readframes(f.getnframes())

        # 转成二字节数组形式（每个采样点占两个字节）
        wave_data = np.fromstring(str_data, dtype=np.short)
        time_temp = [i / self.sr for i in range(len(wave_data))]
        plt.plot(time_temp, wave_data)

        temp_max = []
        temp_min = []
        print(self.segment*self.sr/1000)
        for i in range(0, len(self.y), int(self.segment * self.sr / 1000)):
            piece = self.y[i:(i + int(self.segment * self.sr / 1000))]
            temp_max.append(max(piece))
            temp_min.append(min(piece))
        time_temp = [j * self.segment / 1000 for j in range(len(temp_max))]
        plt.subplot(4, 1, 3)
        plt.plot(time_temp, temp_max)
        plt.subplot(4, 1, 4)
        plt.plot(time_temp, temp_min)

        plt.show()

    # 利用短时能量，短时过零率，使用双门限法进行端点检测
    def endPointDetect(self):
        s = 0
        for en in self.energy:
            s = s + en
        energyAverage = s / len(self.energy)

        s = 0
        for en in self.energy[:5]:
            s = s + en
        ML = s / 5
        MH = energyAverage / 4  # 较高的能量阈值
        ML = (ML + MH) / 4  # 较低的能量阈值
        s = 0
        for zcr in self.zeroCrossingRate[:5]:
            s = float(s) + zcr
        Zs = s / 5  # 过零率阈值

        A = []
        B = []
        C = []

        print(MH)
        # 首先利用较大能量阈值 MH 进行初步检测
        flag = 0
        for i in range(len(self.energy)):
            if len(A) == 0 and flag == 0 and self.energy[i] > MH:
                A.append(i)
                flag = 1
            elif flag == 0 and self.energy[i] > MH and i - 1 > A[len(A) - 1]:
                A.append(i)
                flag = 1
            elif flag == 0 and self.energy[i] > MH and i - 1 <= A[len(A) - 1]:
                A = A[:len(A) - 1]
                flag = 1

            if flag == 1 and self.energy[i] < MH:
                A.append(i)
                flag = 0
        print("较高能量阈值，计算后的浊音A:" + str(A) + "节点数：" + str(len(A)))

        showImage(self.energy, panning=self.panning, title=str(self.segment) + "ms")
        A_np = np.array(A)
        A_np = A_np * self.panning / 1000
        a = [0 for i in range(0, len(A))]
        plt.plot(A_np, a, 'rx')
        tempo, beats = librosa.beat.beat_track(y=self.y, sr=self.sr)
        print(tempo)
        b = librosa.frames_to_time(beats, sr=self.sr)
        plt.plot(b, [5 for i in range(0, len(b))], 'gx')
        plt.show()

        # 利用较小能量阈值 ML 进行第二步能量检测
        for j in range(len(A)):
            i = A[j]
            if j % 2 == 1:
                while i < len(self.energy) and self.energy[i] > ML:
                    i = i + 1
                B.append(i)
            else:
                while i > 0 and self.energy[i] > ML:
                    i = i - 1
                B.append(i)
        print("较低能量阈值，增加一段语言B:" + str(B) + "节点数：" + str(len(B)))

        # 利用过零率进行最后一步检测
        for j in range(len(B)):
            i = B[j]
            if j % 2 == 1:
                while i < len(self.zeroCrossingRate) and self.zeroCrossingRate[i] >= 3 * Zs:
                    i = i + 1
                C.append(i)
            else:
                while i > 0 and self.zeroCrossingRate[i] >= 3 * Zs:
                    i = i - 1
                C.append(i)
        print("过零率阈值，最终语音分段C:" + str(C) + "节点数：" + str(len(C)))
        return C


if __name__ == '__main__':
    v = VAD(r"./resources/output5/ReStarting/drums_01.wav")
    # showImage(v.y)
    # print(v.scanFile())
    # print(len(v.y))
    # print(v.sr)
    # print(len(v.time))
    # print(v.time[-1])
    # # v.merge()
    v.STE()
    v.ZCC()
    v.endPointDetect()
    # v.ZCC()


