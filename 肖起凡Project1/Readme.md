# Project1 编程实现音乐节奏或旋律的可视化

- 16307130201 肖起凡

## 内容组成

- main.py：主程序，实现搭建界面以及可视化音频等所有必须功能。

- Cover.png、icon.ico：程序中必需的图形文件，须保证两个文件与main.py/main.exe在同一目录下。

- main.bat：以命令行方式的运行程序，要求对应机器环境路径中包含存储python3的地址。

- main.exe：以可执行程序的方式运行程序。

##  依赖关系
- Python>=3.7

- Numpy>=1.15.2

- PyAudio>=0.2.11 

- PyGame>=1.9.6

- Tkinter

## 程序说明

- 用户在程序提供的窗口中选择需要可视化的*.wmv音频文件（Python的Wave包不支持其他格式的音频文件的处理），然后点击可视化，相应会弹出选中PyGame模块生成的窗口，窗口中会将音频频率的分布可视化显示出来。

## 算法原理

- 利用Python中的Wave包对目标*.wmv分段进行采样得到一个包含采样区间的声道数量、帧率以及其它量化数据的字符串，然后将采样结果转换成一个按时域表示音频信息的数组，对这个数组做傅里叶变换得到这个区间的音频的频域信息，最后利用PyGame包将频域信息可视化成若干个矩阵显示在屏幕上。

## 参考文献

- PyAudio官方文档：http://people.csail.mit.edu/hubert/pyaudio/docs/

- PyGame官方文档：https://github.com/pygame/pygame