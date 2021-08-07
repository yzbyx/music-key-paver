# -*- coding = uft-8 -*-
# @Time : 2021-07-10 11:06
# @Author : yzbyx
# @File : trackSeparate.py
# @Software : PyCharm

from spleeter.separator import Separator
import warnings
from spleeter.audio.adapter import AudioAdapter

import getSoundSr

warnings.filterwarnings('ignore')


def separate(path, stem_num, output=True):
    separator_ = Separator('spleeter:'+str(stem_num)+'stems', multiprocess=False)

    if not output:
        # Use audio loader explicitly for loading audio waveform :
        audio_loader = AudioAdapter.default()
        sample_rate = getSoundSr.getSr(path).sr()
        waveform, _ = audio_loader.load(path, sample_rate=sample_rate)

        # Perform the separation :
        return separator_.separate(waveform)
    else:
        separator_.separate_to_file(path, './resources/output'+str(stem_num))


if __name__ == "__main__":
    separate("./resources/ReStarting.wav", 5)
