'''
Project      : 
FilePath     : \OPENSOURCE\main.py
Descripttion : 
Author       : GDDG08
Date         : 2022-11-08 02:07:44
LastEditors  : GDDG08
LastEditTime : 2024-04-03 16:10:23
'''
import sys
import argparse
from gui import GUI
from yanhekt import YanHeKT


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


def progressPrint(current, total):
    sys.stdout.write('\r[%-25s](%d/%d)' % ("*" * (100 * current // total // 4),
                                           current, total))
    sys.stdout.flush()


def runCli():
    parser = configArgs()
    args = parseArgs(parser)
    printArgs(args)

    yanhekt = YanHeKT(args.courseID, args.all, args.list, args.range, args.dual, args.vga, args.video, args.skip, args.dir, args.max_workers)
    yanhekt.download(callback_prog=progressPrint)


def runGui():
    gui = GUI()
    gui.event_loop()


def main():
    # judge whether to run in GUI mode
    if len(sys.argv) > 1 and sys.argv[1] == 'gui':
        runGui()
    else:
        runCli()


if __name__ == "__main__":
    main()
