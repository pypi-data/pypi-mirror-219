import time
import os
import sys
import argparse
import psutil
from pywinauto.application import Application
from pywinauto import timings
import datetime


def get_time():
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return now


def refresher(file_path):
    """
    用于刷新pbi文件
    需要传入pbi的文件路径
    pbi默认打开在“主页”选项卡，如果不是，则添加win['主页'].click_input()
    去掉win['刷新'].wait()明显加快速度
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh-timeout", help="等待刷新延时", default=480, type=int)
    parser.add_argument("--init-wait", help="等待启动时间", default=15, type=int)
    args = parser.parse_args()

    timings.after_clickinput_wait = 1
    wait = args.init_wait
    re_timeout = args.refresh_timeout

    procname = "PBIDesktop.exe"
    for proc in psutil.process_iter():
        if proc.name() == procname:
            proc.kill()
    time.sleep(1)

    # print(get_time(), "启动Powerbi")
    os.system('start "" "' + file_path + '"')
    time.sleep(wait)

    app = Application(backend='uia').connect(path=procname)
    win = app.window(title_re='.*Power BI Desktop')
    win.wait("enabled", timeout=120)
    # print(get_time(), "连接Powerbi")
    win.set_focus()
    # win['主页'].click_input()
    # win['刷新'].wait("enabled", timeout=120)
    time.sleep(2)
    win['刷新'].click_input()
    time.sleep(2)
    # print(get_time(), "执行刷新 (延时等待", re_timeout, "秒)")
    win.wait("enabled", timeout=re_timeout)

    win.type_keys("^s")
    time.sleep(2)
    win.wait("enabled", timeout=30)
    win.close()
    # print(get_time(), '已保存')

    for proc in psutil.process_iter():
        if proc.name() == procname:
            proc.kill()


if __name__ == '__main__':
    try:
        path = r'C:\111'
        refresher(path)
    except Exception as e:
        print(e)
        sys.exit(1)
