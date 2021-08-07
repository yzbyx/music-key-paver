# -*- coding = uft-8 -*-
# @Time : 2021-07-09 20:33
# @Author : yzbyx
# @File : rightInfo.py
# @Software : PyCharm

version = "1.0"


def showInfo():
    print("#" * 30 + "\n" + "\t" + "\033[0;34mMusic Key Paver V" + version + "\n" + "\t\tAuthor:yzbyx\033[0m" + "\n" + "#" * 30)
    screen_clear()


def getInfo():
    print("#" * 30 + "\n" + "\t" + "Music Key Paver V" + version + "\n" + "\t\tAuthor:yzbyx" + "\n" + "#" * 30)


def screen_clear():
    # ache = os.system('cls') # Pycharm中无效
    pass