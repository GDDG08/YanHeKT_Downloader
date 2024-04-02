'''
Project      :
FilePath     : \OPENSOURCE\main.py
Descripttion :
Author       : GDDG08
Date         : 2022-11-08 02:07:44
LastEditors  : GDDG08
LastEditTime : 2024-04-02 16:05:25
'''
import requests
import m3u8dl
import sys
import os
import argparse

headers = {
    'Origin': 'https://www.yanhekt.cn',
    "xdomain-client": "web_user",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26'
}


def configArgs():
    parser = argparse.ArgumentParser(description='GDDG08/YanHeKT_Downloader')
    parser.add_argument('courseID', type=int, help='Course ID of YanHeKT')

    group_lession = parser.add_argument_group('Lesson Selection', 'IF NONE, PRINT LESSON LIST AND EXIT.')
    group_lession_exc = group_lession.add_mutually_exclusive_group()
    group_lession_exc.add_argument('-A', '--all', action='store_true', help='Download all lessons')
    group_lession_exc.add_argument('-L', '--list', type=int, nargs='+', metavar='i', help='Select of lesson index (e.g., --list 1 2 4)')
    group_lession_exc.add_argument('-R', '--range', type=int, nargs=2, action='append', metavar='i',
                                   help='Select range of lessons (e.g., --range 3 5 for [3,5))')

    group_video = parser.add_argument_group('Video Type')
    group_video_exc = group_video.add_mutually_exclusive_group()
    group_video_exc.add_argument('-D', '--dual', action='store_true', help='Download both VGA(PC) and Video (default)')
    group_video_exc.add_argument('-G', '--vga', action='store_true', help='Download VGA(PC) only')
    group_video_exc.add_argument('-V', '--video', action='store_true', help='Download Video only')

    group_config = parser.add_argument_group('Configurations')
    group_config.add_argument('-S', '--skip', action='store_true', help='Skip existing files')
    group_config.add_argument('--dir', type=str, default='./', help='Output directory (e.g., --dir ./output)')
    group_config.add_argument('--max-workers', type=int, default=32, metavar='num', help='Max workers for downloading (default: 32)')

    return parser


def parseArgs(parser):
    # force to show help message if no arguments provided
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    else:
        args = parser.parse_args()
        # merge list and range arguments
        if not (args.vga or args.video):
            args.dual = True

        return args


def printArgs(args):
    print("="*10+" YanHeKT_Downloader "+"="*10)
    print(f"Course ID: {args.courseID}")
    print(f"Lesson Selection: {'ALL' if args.all else args.list or args.range}")
    print(f"Video Type: {'VGA & Video' if args.dual else 'VGA' if args.vga else 'Video'}")
    print(f"Skip existing files: {args.skip}")
    print(f"Output Directory: {args.dir}")

    print("="*40+"\n")


if __name__ == '__main__':

    parser = configArgs()
    args = parseArgs(parser)
    printArgs(args)

    print("----Getting Course Information----")

    rqt_course = requests.get(f'https://cbiz.yanhekt.cn/v1/course?id={args.courseID}&with_professor_badges=true', headers=headers)
    courseInfo = rqt_course.json()['data']

    print(courseInfo['name_zh'])

    print("-----Getting Lesson List-----")
    rqt_list = requests.get(f'https://cbiz.yanhekt.cn/v2/course/session/list?course_id={args.courseID}', headers=headers)
    lessonList = rqt_list.json()['data']
    for i, lesson in enumerate(lessonList):
        print(i, lesson['title'])

    print("------Start Downloading------")

    selectList = []
    if args.all:
        selectList = list(range(len(lessonList)))
    elif args.list:
        selectList = args.list
    elif args.range:
        selectList += list(range(args.range[0][0], args.range[0][1]))
    else:
        print("[Error] No lesson selected in args.")
        print("Please use -A/--all, -L/--list, or -R/--range to select lessons.")
        print("Example:")
        print(f"\tpython main.py {args.courseID} --all")
        print(f"\tpython main.py {args.courseID} --list 0 2 4")
        print(f"\tpython main.py {args.courseID} --range 3 5")
        sys.exit(0)

    courseFullName = '-'.join([str(args.courseID), courseInfo['name_zh'], courseInfo['professors'][0]['name']])
    dirName = os.path.join(args.dir, courseFullName)

    if not os.path.exists(dirName):
        os.makedirs(dirName)

    for i in selectList:
        video = lessonList[i]
        fileName = video['title'].replace("/", "-")  # 防止文件名中的/导致路径错误

        print(f"Downloading {fileName} --->")

        videos = video['videos'][0]
        # 下载投影录屏
        if args.vga or args.dual:
            if 'vga' in videos:  # 检查是否存在vga链接
                if args.skip and os.path.exists(f"{dirName}/{fileName}-VGA.mp4"):
                    print(f"VGA seems already done. Skipping...")
                else:
                    print("VGA -->")
                    m3u8dl.M3u8Download(videos['vga'], dirName, fileName + '-VGA', max_workers=args.max_workers)
            else:
                print(f"No VGA found.")

        # 下载视频
        if args.video or args.dual:
            if 'main' in videos:  # 检查是否存在main链接
                if args.skip and os.path.exists(f"{dirName}/{fileName}-Video.mp4"):
                    print(f"Video seems already done. Skipping...")
                else:
                    print("Video -->")
                    m3u8dl.M3u8Download(videos['main'], dirName, fileName + '-Video', max_workers=args.max_workers)
            else:
                print(f"No Video found.")
