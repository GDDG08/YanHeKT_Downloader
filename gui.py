import re
import threading
from yanhekt import YanHeKT
import PySimpleGUI as sg


class GUI:
    def __init__(self):
        self.window = None
        self.init_ui()
        self.yanhekt = None
        self.td = None

    def init_ui(self):
        # sg.theme('DarkAmber')  # Set a theme for the GUI
        sg.theme('DarkTeal7')

        frame_course_info = [

            [
                sg.Column([
                            [sg.Text('Web Link:', expand_x=True), sg.Input(key='WEB_LINK',
                                                                           default_text="https://www.yanhekt.cn/course/11111", enable_events=True, size=(35, 2), expand_x=True)],
                            [sg.Text('Course ID:', expand_x=True), sg.Input(key='COURSE_ID', enable_events=True, size=(35, 2), expand_x=True)]
                ]),
                sg.Column([
                    # [sg.Button('Get Course ID', expand_x=True, disabled=True)],
                    [sg.Button('Get Course Info', expand_x=True, disabled=True)]
                ])
            ],
            [sg.HorizontalSeparator()],
            [
                sg.Column([
                    [sg.Text('Course Name:'), sg.Text('', key='COURSE_NAME'),  sg.Text('Professor:'), sg.Text('', key='PROFESSOR')],
                    [sg.Listbox(values=[], size=(50, 8), expand_x=True, key='LESSON_LIST',
                                enable_events=True, select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)],
                    [sg.Text('use Ctrl or Shift or Drag to select multiple')],
                    [sg.Text('Ctrl + A to select all')],
                ], pad=(25, 0), expand_x=True, element_justification='center')],
        ]

        # frame_lesson_selection = [
        #     [sg.Radio('All', group_id="Selection", key='ALL', default=True)],
        #     [sg.Radio('List', group_id="Selection", key='LIST')],
        #     [sg.Checkbox('Lesson 1', key='LESSON_1'), sg.Checkbox('Lesson 2', key='LESSON_2'), sg.Checkbox('Lesson 3', key='LESSON_3')],
        #     [sg.Radio('Range', group_id="Selection", key='RANGE')],
        #     [sg.Text('from'), sg.Spin([i for i in range(1, 10)], initial_value=0, key='RANGE_START'),
        #      sg.Text('to'), sg.Spin([i for i in range(1, 10)], initial_value=1, key='RANGE_END')],

        # ]

        frame_settings = [
            [sg.Text('Video Type:'), sg.Radio('Dual', group_id="RADIO_VIDEO_TYPE", key='DUAL', default=True), sg.Radio(
                'VGA', group_id="RADIO_VIDEO_TYPE", key='VGA'), sg.Radio('Video', group_id="RADIO_VIDEO_TYPE", key='VIDEO')],
            [sg.Text('Output Directory:'), sg.Input("./temp", size=(30, 2), key="OUTPUT_DIR", expand_x=True),
             sg.FolderBrowse(key='OUTPUT_DIR_BROWSE', initial_folder="./")],
            [sg.Checkbox('Skip Existing', default=True, key='SKIP_EXISTING')],
        ]

        # Layout definition
        layout = [
            [sg.Frame('Course Information', frame_course_info)],
            # [sg.Frame('Lesson Selection', frame_lesson_selection)],
            [sg.Frame('Settings', frame_settings, expand_x=True)],

            [sg.Button('Download Lessons', disabled=True)],
            [sg.Output(size=(40, 10), expand_x=True, key='OUTPUT')],
            [sg.ProgressBar(100, orientation='h', size=(40, 10), expand_x=True, key='PROGRESS_BAR')],
        ]

        # Create the Window
        self.window = sg.Window('YanHeKT Downloader', layout)

    def event_loop(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED:  # If user closes window
                if self.td:
                    self.td.stop()
                break
            try:
                # if event == 'Get Course ID':
                #     courseID = values['WEB_LINK'].split('/')[-1]
                #     if (courseID.isdigit()):
                #         self.window['COURSE_ID'].update(courseID)
                #         self.window['Get Course Info'].update(disabled=False)
                if event == 'Get Course Info':
                    if not values['COURSE_ID'].isdigit():
                        sg.popup_error("Invalid Course ID")
                        continue
                    else:
                        self.window['Download Lessons'].update(disabled=True)

                        self.yanhekt = YanHeKT(values['COURSE_ID'])
                        courseInfo, lessonList = self.yanhekt.getCourseInfo()
                        self.window['COURSE_NAME'].update(courseInfo['name_zh'])
                        self.window['PROFESSOR'].update(courseInfo['professors'][0]['name'])

                        lessonTitles = [lesson['title'] for lesson in lessonList]
                        self.window['LESSON_LIST'].update(values=[tittle for tittle in lessonTitles])
                elif event == 'Download Lessons':
                    self.window['Download Lessons'].update(disabled=True)
                    self.window['PROGRESS_BAR'].update(0)

                    self.window['OUTPUT'].update("Downloading...\n\n")
                    # print(values)
                    lessonTitles = [lesson['title'] for lesson in self.yanhekt.lessonList]

                    selected_lessons = [i for i, tittle in enumerate(lessonTitles) if tittle in values['LESSON_LIST']]
                    self.yanhekt.updateArgs(_all=False, _list=selected_lessons, _range=False,
                                            _dual=values['DUAL'], _vga=values['VGA'], _video=values['VIDEO'], _skip=values['SKIP_EXISTING'], _dir=values['OUTPUT_DIR'])
                    self.do_download()
                elif event == 'WEB_LINK':
                    # print(values['WEB_LINK'])
                    if values['WEB_LINK']:
                        # self.window['Get Course ID'].update(disabled=False)

                        rex = re.search(r'(?<=course/)(\d+)', values['WEB_LINK'])

                        if (rex):
                            self.window['COURSE_ID'].update(rex.group(0))
                            self.window['Get Course Info'].update(disabled=False)
                        else:
                            self.window['COURSE_ID'].update("")
                            self.window['Get Course Info'].update(disabled=True)
                    # else:
                    #     self.window['Get Course ID'].update(disabled=True)
                elif event == 'COURSE_ID':
                    if values['COURSE_ID']:
                        self.window['Get Course Info'].update(disabled=False)
                    else:
                        self.window['Get Course Info'].update(disabled=True)
                elif event == 'LESSON_LIST':
                    if (len(values['LESSON_LIST']) > 0):
                        self.window['Download Lessons'].update(disabled=False)
                    else:
                        self.window['Download Lessons'].update(disabled=True)

            except Exception as e:
                sg.popup_error(f'An error occurred: {str(e)}')

        self.window.close()

    def do_download(self):
        # new thread
        self.td = threading.Thread(target=self.yanhekt.download, args=(self.callback_download, self.callback_progress))
        self.td.start()

    def callback_download(self, isFinished):
        self.window['Download Lessons'].update(disabled=False)
        # self.window['OUTPUT'].update(f"Download success? {isFinished}\n\n")

    def callback_progress(self, current, total):
        self.window['PROGRESS_BAR'].update(current/total*100)
