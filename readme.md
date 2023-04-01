# 北理工延河课堂视频下载

##　功能介绍

下载[延河课堂](https://www.yanhekt.cn/)的录播视频

- 支持下载非选课班级的课程
- 支持多线程批量下载
- 支持下载电脑视频或教室录像
- 按课程名分类文件夹保存



## 使用前准备

1. 下载/克隆本仓库或release

2. 安装python依赖包

   ```shell
   pip install -r requirements.txt
   ```

3. 确保命令行环境有ffmpeg，本仓库也附带了可执行文件

4. [optional]由于视频加密解算，需要运行js，如果遇到js执行报错（Windows平台），请安装[node.js](https://nodejs.org/en)

## 食用方法

1. 获取课程ID

   在课程详情页，注意不是视频播放页，`https://www.yanhekt.cn/course/11111`，从url中获得课程id，如`11111`。

2. 运行脚本

   ```
   python main.py 11111 
   ```

3. 程序自动获取课程信息，打印视频列表

4. 输入要下载的视频序号，这里请直接提供列表或使用range（我懒得写匹配，直接用eval）

   ```python
   # 支持的格式
   [1,2,3]
   [1,4,5]
   range(13)
   range(3, 6)
   ```

5. 选择下载投影录屏(vga)或者教室录像(video)

   ```python
   # 示例输入
   # NULL | ILLEGAL -> video
   vga
   video
   ```

6. enjoy



## 致谢

- [M3u8Download](https://github.com/anwenzen/M3u8Download)
