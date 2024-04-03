'''
Project      :
FilePath     : \OPENSOURCE\yanhekt.py
Descripttion :
Author       : GDDG08
Date         : 2022-11-08 02:07:44
LastEditors  : GDDG08
LastEditTime : 2024-04-03 16:03:17
'''
import requests
from m3u8dl import M3u8Download
import os

headers = {
    'Origin': 'https://www.yanhekt.cn',
    "xdomain-client": "web_user",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26'
}


class YanHeKT():
    def __init__(self, _courseID, _all=False, _list=None, _range=None, _dual=True, _vga=False, _video=False, _skip=False, _dir='./',  _max_workers=32) -> None:
        self.courseID = _courseID
        self.lessonList = None
        self.courseInfo = None

        self.updateArgs(_all, _list, _range, _dual, _vga, _video, _skip, _dir, _max_workers)

    def updateArgs(self, _all=False, _list=None, _range=None, _dual=True, _vga=False, _video=False, _skip=False, _dir='./',  _max_workers=32):
        self.all = _all
        self.list = _list
        self.range = _range
        self.dual = _dual
        self.vga = _vga
        self.video = _video
        self.skip = _skip
        self.dir = _dir
        self.max_workers = _max_workers

    def getCourseInfo(self):
        print("----Getting Course Information----")

        rqt_course = requests.get(f'https://cbiz.yanhekt.cn/v1/course?id={self.courseID}&with_professor_badges=true', headers=headers)
        courseInfo = rqt_course.json()['data']

        print(courseInfo['name_zh'])

        print("-----Getting Lesson List-----")
        rqt_list = requests.get(f'https://cbiz.yanhekt.cn/v2/course/session/list?course_id={self.courseID}', headers=headers)
        lessonList = rqt_list.json()['data']

        for i, lesson in enumerate(lessonList):
            print(f"[{i}] ", lesson['title'])

        self.courseInfo = courseInfo
        self.lessonList = lessonList
        return courseInfo, lessonList

    def download(self, callback=None, callback_prog=None):
        if not self.lessonList or not self.courseInfo:
            self.getCourseInfo()

        print("------Start Downloading------")

        selectList = []
        if self.all:
            selectList = list(range(len(self.lessonList)))
        elif self.list:
            selectList = self.list
        elif self.range:
            selectList += list(range(self.range[0][0], self.range[0][1]))
        else:
            print("[Error] No lesson selected in args.")
            print("Please use -A/--all, -L/--list, or -R/--range to select lessons.")
            print("Example:")
            print(f"\tpython main.py {self.courseID} --all")
            print(f"\tpython main.py {self.courseID} --list 0 2 4")
            print(f"\tpython main.py {self.courseID} --range 3 5")

            if callback:
                callback(False)
            return

        courseFullName = '-'.join([str(self.courseID), self.courseInfo['name_zh'], self.courseInfo['professors'][0]['name']])
        dirName = os.path.join(self.dir, courseFullName)

        if not os.path.exists(dirName):
            os.makedirs(dirName)

        for i in selectList:
            video = self.lessonList[i]
            fileName = video['title'].replace("/", "-")  # 防止文件名中的/导致路径错误

            print(f"Downloading {fileName} --->")

            videos = video['videos'][0]
            # 下载投影录屏
            if self.vga or self.dual:
                if 'vga' in videos:  # 检查是否存在vga链接
                    if self.skip and os.path.exists(f"{dirName}/{fileName}-VGA.mp4"):
                        print(f"VGA seems already done. Skipping...")
                    else:
                        print("VGA -->")
                        M3u8Download(videos['vga'], dirName, fileName + '-VGA', max_workers=self.max_workers, callback_progress=callback_prog)
                else:
                    print(f"No VGA found.")

            # 下载视频
            if self.video or self.dual:
                if 'main' in videos:  # 检查是否存在main链接
                    if self.skip and os.path.exists(f"{dirName}/{fileName}-Video.mp4"):
                        print(f"Video seems already done. Skipping...")
                    else:
                        print("Video -->")
                        M3u8Download(videos['main'], dirName, fileName + '-Video', max_workers=self.max_workers, callback_progress=callback_prog)
                else:
                    print(f"No Video found.")

        if callback:
            callback(True)
        return


if __name__ == '__main__':
    # main()
    # yanhekt = YanHeKT(12345, _all=True, _dir='./')
    # yanhekt.download(callback_prog=progressPrint)
    pass
