# -*- coding = uft-8 -*-
# @Time : 2021-07-11 12:53
# @Author : yzbyx
# @File : menu.py
# @Software : PyCharm

def show():
    print("-" * 12 + ">" + "Menu" + "<" + "-" * 12)
    # ---> 功能菜单 <--- #
    menuList = [0, 1, 2, 3, 4]
    print("\033[0;34m0.\033[0m" + "Exit")
    print("\033[0;34m1.\033[0m" + "BPM calculate")
    print("\033[0;34m2.\033[0m" + "Track separate")
    print("\033[0;34m3.\033[0m" + "Voice activity detection")
    # ---> 菜单结束 <--- #
    return menuList
