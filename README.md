# music-key-paver 乐曲分析和铺面制作工具（未完成）
A music analysis tools and a key paver for BanG Dream(unfinished)

**基本思路**
*一、乐曲处理*
1.bpm识别（Librosa包）
参考：https://librosa.org/doc/latest/tutorial.html

2.音轨分离（Spleeter包）
参考：https://github.com/deezer/spleeter

3.端点检测（双门限法）
参考：https://blog.csdn.net/sinat_18131557/article/details/106017459

4.主节拍识别（未实现）
目的：主要用于制作铺面键位

*二、铺面制作（未实现）*
基于铺面制作器导出的json文件格式生成铺面
制作器网址：https://reikohaku.gitee.io/ebbb/

json文件结构：
1.铺面基本信息：
例子："timepoints":[{"id":1966857868,"time":0,"bpm":143,"bpb":4}]
id：铺面id
time：偏移量
bpm：节拍速度
bpb：节拍形式

2.滑条信息：
例子："slides":[{"id":1663816869,"flickend":false,"notes":[129951195,1649427469]}
id：滑条id
flickend：末端是否为划键
notes：键组成id

3.按键信息：
例子："notes":[{"type":"single","id":347760186,"timepoint":1326932466,"offset":0,"lane":3}]
type(single,flick,slide)：按键类型（在滑条内的都为slide）
id：按键id
timepoint：时间结点（与基本信息保持相同）
offset：偏移量（1/48拍计为1）
lane：轨道位置（从左至右0~6）
