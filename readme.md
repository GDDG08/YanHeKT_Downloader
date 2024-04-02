# 北理工延河课堂视频下载

欢迎Star🌟！欢迎提Issue

本项目在 网协2023“十行代码”比赛 荣获特等奖🎉 指路👉[Github](https://github.com/BITNP/poems-2023/)

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
- 2024-4-2 (🌟)更改signature实现方式
   - 放弃js执行，不再使用js2py，提升兼容性 [issue#5](https://github.com/GDDG08/YanHeKT_Downloader/issues/5)
   - 现在时间sign和url后缀 都是py原生

## 使用前准备

1. 下载/克隆本仓库或release

2. 安装python依赖包

   ```shell
   pip install -r requirements.txt
   # (其实就一个requests)
   ```

3. 确保命令行环境有ffmpeg，本仓库的release也附带了ffmpeg(仅exe)

   如果最终视频没有合并，说明ffmpeg环境存在问题

4. (1.1后版本忽略)~~[optional]由于视频加密解算，需要运行js，如果遇到js执行报错，请安装[node.js](https://nodejs.org/en)~~

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

## Todo（画大饼）

- @ZJC-GH 同学添加了批量下载功能，
   - 有需要的同学可以到[这个仓库](https://github.com/ZJC-GH/YanHeKT_Downloader) release中下载使用
   - 目前已合并到dev分支
- 计划使用`argparse`完善命令行参数，优化下交互体验
- （超大饼）在参数写完后整个简单的gui


## 致谢

- [M3u8Download](https://github.com/anwenzen/M3u8Download)
