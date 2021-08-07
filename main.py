# -*- coding = uft-8 -*-
# @Time : 2021-07-09 20:20
# @Author : yzbyx
# @File : main.py
# @Software : PyCharm
import warnings

import librosa

import rightInfo as info
import bpmAnalysis as bpm
import trackSeparate
import menu
import typeConvertor
import voiceActivityDetection as vad

warnings.filterwarnings('ignore')

filePath = "./resources/MEGALOVANIA.mp3"
stem_num = 5

if __name__ == "__main__":
    info.showInfo()
    print("Please put music file at ./resources folder")
    path = input("Then enter the path of music(./resources/xxx.xxx)\ndefault?(Y/other):")
    s = filePath
    a = 0
    if path == "Y" or path == "y":
        pass
    else:
        #  判断是否需要将文件格式转换为wav格式
        a = 1
        s = path.split("./resources/")
        while True:
            print(s)
            if len(s) == 1:
                path = input("The format of file path is wrong! (./resources/xxx.xxx)\nplease re-enter:")
                s = path.split("./resources/")
            elif "/" in s[-1] or "\\" in s[-1] or len(s[-1].split(".")) != 2:
                path = input("The format of file path is wrong! (./resources/xxx.xxx)\nplease re-enter:")
                s = path.split("./resources/")
            else:
                filePath = path
                break
    t = s.split(".")[-1]
    if t != "wav":
        print("#" * 30)
        print("Converting " + t + " to " + "wav...")
        c = typeConvertor.convertor(filePath)
        c.convert()
        print("Complete!")
    if a == 0:
        filePath = "./resources/" + filePath.split("/")[-1].split(".")[0] + ".wav"
    else:
        filePath = "./resources/" + path.split("/")[-1].split(".")[0] + ".wav"
    print(filePath)
    print("#" * 30)

    while True:
        menuList = menu.show()
        i = int(input("Choose an option:"))
        while True:
            if i in menuList:
                print("#" * 30)
                break
            else:
                i = int(input("\033[0;31mError!\033[0m\nChoose an option again:"))

        # 退出
        if i == 0:
            print("Exiting...")
            i = -1  # 重置选择
            break

        # BPM分析
        elif i == 1:
            print("Processing...")
            bpmResult = bpm.analysis(filePath)
            print(str(bpmResult) + "-->" + str(int(bpmResult + 0.5)), end="\n")
            a = input("Adjust?(Y/N):")
            if a == "Y" or a == "y":
                result = int(input("Enter BPM:"))
                print("Adjustment completed!\n" + "#" * 30)
            else:
                print("#" * 30)
            i = -1  # 重置选择

        # 音轨分离
        elif i == 2:
            numList = [2, 4, 5]
            stem_num = int(input("Stem num(2,4,5):"))
            while True:
                if stem_num in numList:
                    break
                else:
                    stem_num = int(input("\033[0;31mError!\033[0m\nEnter stem num again:"))
            print("Processing...")
            trackSeparate.separate(filePath, stem_num, output=True)
            print("Complete!")
            i = -1  # 重置选择

        # 语音端点检测
        elif i == 3:
            VAD_object = vad.VAD(filePath)
            librosa.beat
