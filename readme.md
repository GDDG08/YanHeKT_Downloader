# 北理工延河课堂视频下载

欢迎Star🌟！欢迎提Issue

## 功能介绍

下载[延河课堂](https://www.yanhekt.cn/)的录播视频

- 支持下载非选课班级的课程
- 支持多线程批量下载
- 支持下载电脑视频或教室录像
- 按课程名分类文件夹保存

## 更新日志

- 2023-4-10 同步延河课堂接口更改
- 2023-4-20 更改js执行方式，无需安装nodejs
- 2023-11-12 签名效率优化，优化下载速度
   - 理论可以跑满千兆有线网，可以根据电脑性能修改max_workers数量
- 2024-02-22 自动批量下载，vga和video自动都下载。增加exe、bat文件，方便直接运行和批量运行。

## 使用前准备

1. 下载发布的zip文件，解压缩到某个文件夹内，会有3个文件：signature.js、start.bat、YanHeKT_Downloader_1.2.2.exe。


## 食用方法

1. 获取课程ID

   在课程详情页，注意不是视频播放页，`https://www.yanhekt.cn/course/11111`，从url中获得课程id，如`11111`。

2. 运行脚本
   下载zip文件，解压缩到某个文件夹内，会有4个文件：signature.js、start.bat、YanHeKT_Downloader_1.2.2.exe、ffmpeg.exe。
   
   连续批量下载：
   start.bat中写入需要连续下载的课程id，用文本编辑器打开修改即可，保存后退出，双击bat文件即可快速批量下载，会自动下载全部列表中的视频，包括电脑投影(vga)和监视器视频(video)。

   单个下载：
   也可以双击exe文件直接单个使用，输入课程编号即可，会下载该课程的全部录屏，包括电脑投影(vga)和监视器视频(video)。

3. enjoy



## 致谢

- [M3u8Download](https://github.com/anwenzen/M3u8Download)
- https://github.com/GDDG08/YanHeKT_Downloader
