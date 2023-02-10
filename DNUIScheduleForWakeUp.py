import csv
import re
import tkinter
import requests
from tkinter import *
from bs4 import BeautifulSoup

page = None
num = {'一': 1,
       '二': 2,
       '三': 3,
       '四': 4,
       '五': 5,
       '六': 6,
       '日': 7}


# 获取页面
def get_page():
    global page
    url = 'http://wls16.webvpn.neusoft.edu.cn/sched/sched/stucourse.do'
    header = {'Cookie': entry.get()}
    request = requests.get(url=url, headers=header)
    page = BeautifulSoup(request.text, 'lxml')


# 获取课程表
def get_class():
    # 用于存储结果的列表
    class_list = []
    address_temp = ''
    for class_info in page.table.tbody.find_all('tr'):
        info_list = class_info.find_all('td')
        # 课程名称
        name = info_list[4].string
        # 上课时间
        time_info = info_list[9].string
        # 老师
        teacher = info_list[8].string.split('[')[0]
        # 按照星期几分类
        time_list = time_info.split(',')
        for time in time_list:
            time = re.split(r'[\[\]]', time)
            # 星期
            week = num[time[2]]
            # 节数数据处理
            section = time[3].replace('节', '').split('-')
            # 开始节数
            start = section[0]
            # 结束节数
            end = section[1]
            # 上课周数
            class_week = time[1].replace('周', '')
            # 地点
            if (add := info_list[10].string) is not None:
                address = add
            else:
                address = address_temp[1] if address_temp[0] == name else ''
            # 将地址暂时保存
            address_temp = (name, address)
            # 存入列表
            class_list.append((name, week, start, end, teacher, address, class_week))
    return class_list


def write_to_file():
    get_page()
    with open('schedule.csv', 'w', newline='', encoding='UTF-8') as schedule_file:
        writer = csv.writer(schedule_file)
        writer.writerow(['课程名称', '星期', '开始节数', '结束节数', '老师', '地点', '周数'])
        writer.writerows(get_class())
    exit()


if __name__ == '__main__':
    gui = Tk()
    gui.title("获取用于导入DNUI课程表到WakeUP的CSV格式文件")
    screen_width = gui.winfo_screenwidth()
    screen_height = gui.winfo_screenheight()
    width = 420
    height = 80
    gui_size = f'{width}x{height}+{round((screen_width - width) / 2)}+{round((screen_height - height) / 2)}'
    gui.geometry(gui_size)
    label = Label(gui, text="请登录http://wls16.webvpn.neusoft.edu.cn/sched，并将Cookie复制于此:")
    label.grid(row=0, column=0)
    entry = tkinter.Entry(gui)
    entry.grid(row=1, column=0)
    button = Button(gui, text="获取", command=write_to_file)
    button.grid(row=2, column=0)
    gui.mainloop()
