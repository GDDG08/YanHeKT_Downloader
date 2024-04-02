# 北理工延河课堂视频下载

欢迎Star🌟！欢迎提Issue

本项目在 网协2023“十行代码”比赛 荣获**特等奖**🎉 指路👉[Github](https://github.com/BITNP/poems-2023/)

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
- **2024-4-2 (🌟)更改signature实现方式**
   - 放弃js执行，不再使用js2py，提升兼容性 [issue#5](https://github.com/GDDG08/YanHeKT_Downloader/issues/5)
   - 现在时间sign和url后缀 都是py原生
- 2024-4-2 (🌟)更改交互方式，添加完整的**命令行参数**
   - 支持一次下载全部课时，感谢@ZJC-GH同学的建议和pr
   - 支持分别或同时下载VGA和Video
   - 支持增量下载，自动跳过已下载文件
   - 更改临时文件存储位置，放在`temp`中
   - 可以自定义输出文件夹位置
   - **详见 #食用方法**
   - 优化ffmpeg输出


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

   在课程详情页，**注意不是视频播放页**，如`https://www.yanhekt.cn/course/11111`，

   从url中获得课程id，如`11111`

2. 命令行参数

   - **指定课程的ID**

     - `<courseID>`，直接给出

       ```shell
       # 例：查看课程信息及视频列表
       python main.py 11111
       ```

   - **选择下载的课时序号**

     - `--all`，下载全部课时
     - `--list 0 2 4 `，下载选定的课时列表
     - `--range 3 5`，下载一个范围内的课时
       ```shell
       # 例：下载第3-8节课
       python main.py 11111 --range 3 9
       python main.py 11111 -L 3 9
       ```

   - **选择下载的视频类型**

     - `--dual`，同时下载电脑录屏和教室视频**（默认）**
     - `--vga `，仅下载电脑录屏
     - `--video`，仅下载教室视频
       ```shell
       # 例：下载第3-8节课，仅下载电脑录屏
       python main.py 11111 --range 3 9 --vga
       ```

   - 增量下载

     - `--skip`，跳过已下载，仅下载新上传的视频
       ```shell
       # 例：定期更新课程全部视频
       python main.py 11111 --all --skip
       ```

3. 更多高级用法请参考命令行提示

   ```shell
   !python main.py --help
   
   # usage: main.py [-h] [-A | -L i [i ...] | -R i i] [-D | -G | -V] [-S] [--dir DIR] [--max-workers num] courseID
   
   # GDDG08/YanHeKT_Downloader
   
   # positional arguments:
   # courseID              Course ID of YanHeKT
   
   # options:
   # -h, --help            show this help message and exit
   
   # Lesson Selection:
   # IF NONE, PRINT LESSON LIST AND EXIT.
   
   # -A, --all             Download all lessons
   # -L i [i ...], --list i [i ...]
   #                         Select of lesson index (e.g., --list 1 2 4)
   # -R i i, --range i i   Select range of lessons (e.g., --range 3 5 for [3,5))
   
   # Video Type:
   # -D, --dual            Download both VGA(PC) and Video (default)
   # -G, --vga             Download VGA(PC) only
   # -V, --video           Download Video only
   
   # Configurations:
   # -S, --skip            Skip existing files
   # --dir DIR             Output directory (e.g., --dir ./output)
   # --max-workers num     Max workers for downloading (default: 32)
   
   ```

4. **ENJOY !**

   

## Todo（画大饼）

- @ZJC-GH 同学添加了批量下载功能
   - 有需要的同学可以到[这个仓库](https://github.com/ZJC-GH/YanHeKT_Downloader) release中下载使用
   - 目前已合并到dev分支
- 计划使用`argparse`完善命令行参数，优化下交互体验
- （超大饼）在参数写完后整个简单的gui


## 致谢

- [M3u8Download](https://github.com/anwenzen/M3u8Download)
