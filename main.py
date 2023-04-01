'''
Project      : 
FilePath     : \FINAL\main.py
Descripttion : 
Author       : GDDG08
Date         : 2022-11-08 02:07:44
LastEditors  : GDDG08
LastEditTime : 2022-12-03 22:17:30
'''
import requests
import m3u8dl
import sys
import os
headers = {
    'Origin': 'https://www.yanhekt.cn',
    "xdomain-client": "web_user",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26'
}


if __name__ == '__main__':
    courseID = sys.argv[1]

    course = requests.get(
        f'https://cbiz.yanhekt.cn/v1/course?id={courseID}&with_professor_badges=true', headers=headers)
    req = requests.get(f'https://cbiz.yanhekt.cn/v2/course/session/list?course_id={courseID}', headers=headers)
    # print(course.json())
    print(course.json()['data']['name_zh'])

    videoList = req.json()['data']
    for i, c in enumerate(videoList):
        print(i, c['section_group_title'])


    # index = eval('[' + input('select(split by \',\'):') + ']')
    index = eval(input())
    vga = input('video or vga?(default video):')
    dirName = r'./'+course.json()['data']['name_zh'] + '-' + course.json()['data']['professors'][0]['name']

    if not os.path.exists(dirName):
        os.makedirs(dirName)

    for i in index:
        c = videoList[i]
        fileName = str(courseID) + '-' + c['section_group_title']
        print(fileName)
        if vga == "vga":
            m3u8dl.M3u8Download(c['videos'][0]['vga'], dirName, fileName + '-VGA', max_workers=4)
        else:
            m3u8dl.M3u8Download(c['videos'][0]['main'], dirName, fileName+'-Video', max_workers=4)
