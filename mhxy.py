import threading
import win32con
import win32api, win32gui
import random
import time
import tkinter as tk
import pyautogui
import datetime

#from PyQt5.QtWidgets import QApplication
#from PyQt5.QtGui import *
#import sys
"""
from pydoc import text
from memory_pic import *
from PIL import ImageGrab, Image
import base64
"""

window_region=(0,0,800,600)

def resolution():  # 获取屏幕分辨率
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

# screen_resolution = resolution()

# 获取梦幻西游窗口信息吗，返回一个矩形窗口四个坐标
def get_window_info():
    global handle
    wdname = u'梦幻西游 - MuMu模拟器'
    handle = win32gui.FindWindow(0, wdname)  # 获取窗口句柄
    if handle == 0:
        # text.insert('end', '提示：请打开梦幻西游\n')
        # text.see('end')  # 自动显示底部
        return None
    else:
        return win32gui.GetWindowRect(handle)

# window_size = get_window_info()
 # 返回x相对坐标
def get_posx(x, window_size):
    return int((window_size[2] - window_size[0]) * x / 804)


 # 返回y相对坐标
def get_posy(y, window_size):
    return int((window_size[3] - window_size[1]) * y / 630)

# topx, topy = window_size[0], window_size[1]

# # 抓取游戏指定坐标的图像
# img_ready = ImageGrab.grab((topx + get_posx(500, window_size), topy + get_posy(480, window_size),
#                             topx + get_posx(540, window_size), topy + get_posy(500, window_size)))
# # 查看图片
# img_ready.show()

def move_click(x, y, t=0):  # 移动鼠标并点击左键
    win32api.SetCursorPos((x, y))  # 设置鼠标位置(x, y)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN |
                         win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)  # 点击鼠标左键
    if t == 0:
        time.sleep(random.random()*2+1)  # sleep一下
    else:
        time.sleep(t)
    return 0

# 找指定任务
def findpng(Pngfile):
    global window_region
    myConfidence = 0.85
    pyautogui.FAILSAFE = False
    result = pyautogui.locateOnScreen('images\\'+Pngfile, region=window_region, confidence=myConfidence)
    return result

# 单击指定位置
def click(x,y):
    move_click(x,y,0.1)
    pyautogui.FAILSAFE = False
    pyautogui.moveTo(x=window_size[0]+10,y=window_size[1]+10,duration=0.1)  #鼠标移至窗口左上角

# 接任务
def get_rw(rwm):
    pos=findpng(rwm+".png")
    print(rwm,pos)
    if pos is not None:
        click(pos[0]+pos[2]-6,pos[1]+pos[3]-6)
        time.sleep(0.5)
        return True
    else:
        return False

# 等待直到打开活动界面
def open_huodong():
    global is_start
    is_start = True
    time.sleep(1)   # 等待1秒
    print(window_region[0]+window_region[2]/2,window_region[1]+window_region[3]/2,window_region)
    click(window_region[0]+int(window_region[2]/2),window_region[1]+int(window_region[3]/2))  #移到窗口中间，点击以激活窗口
    while is_start:
        if get_rw("huodong"):
            break
        else:
            time.sleep(3)

# 执行任务操作
def do_action():
    flag = 0    # 执行标志
    if get_rw("choice_do"):  # 选择任务
        flag = 1
        time.sleep(0.1)
    elif get_rw("shiyong"):  # 使用物品
        flag = 1
        time.sleep(0.1)
    elif get_rw("goumai"):  # 购买物品
        flag = 1
        time.sleep(0.1)
    elif get_rw("juanxian"):  # 捐献
        flag = 1
        time.sleep(0.1)
    elif get_rw("jixu"):    #点击任意地方继续
        flag = 1
        time.sleep(0.1)
        while True:
            if get_rw("jixu"):
                time.sleep(0.1)
            else:
                break
    elif get_rw("tiaoguo"): #点击跳过
        flag = 1
    elif get_rw("lingqu"):  # 领取
        flag = 1
        time.sleep(0.1)
    elif get_rw("cuansong"):  # 传送
        flag = 1
        time.sleep(0.1)
        get_rw("guanbi")
    elif get_rw("shangjiao"):  # 上交
        flag = 1
        time.sleep(0.1)
    elif get_rw("guanbi") or get_rw("guanbi_1") or get_rw("guanbi_2") or get_rw("guanbi_3"):  # 关闭窗口
        flag = 1
        time.sleep(0.1)
    elif get_rw("queding"):  # 确定
        flag = 1
        time.sleep(0.1)
    elif get_rw("zidong"):  # 自动战斗
        flag = 1
        time.sleep(0.1)
    elif get_rw("denglu"):  # 登录游戏
        flag = 1
        time.sleep(0.1)
    elif get_rw("chongshi"):  # 重连失败重试
        flag = 1
        time.sleep(0.1)

    return flag


# 师门
def shi_men(window_size):
    global is_start
    is_start = True
    open_huodong()
    if not get_rw("shimen_rw"):
        print("师门任务已完成")
        button_shimen["text"] = "师门（已完成）"
        return
    button_shimen["text"] = "师门（执行中）"
    while is_start:
        flag = 0
        if get_rw("shimen"):    # 师门
            flag = 1
            time.sleep(1)

        result = do_action()
        if findpng("renwu.png") is True and result == 0 and flag == 0:
            break
        time.sleep(1)

# 抓鬼
def zhua_gui(window_size):
    global is_start
    is_start = True
    while is_start:
        if findpng("renwu.png") and not get_rw("zuogui"):
            open_huodong()
            get_rw("zuogui_rw")
            get_rw("zudui")     # 自动组队
            get_rw("guanbi")     # 关闭窗口
        time.sleep(60)
    return


#帮派任务
def bang_pai(window_size):
    global is_start
    is_start = True
    open_huodong()
    if not get_rw("bangpai_rw"):
        print("帮派任务已完成")
        button_bangpai["text"]="帮派（已完成）"
        return
    button_bangpai["text"]="帮派（执行中）"
    while is_start:
        if get_rw("bangpai_xw") or get_rw("bangpai_xw1"):    #玄武
            time.sleep(1)
        elif get_rw("bangpai_zq"):    #朱雀
            time.sleep(1)
        elif get_rw("bangpai_ql"):    #青龙
            time.sleep(1)
        #elif findpng("renwu.png"):   #在主界面，但以上任务都没找到，则任务已完成，退出
        #    button_bangpai["text"] = "帮派（已完成）"
        #    break

        do_action()

        time.sleep(3)
    return

# 宝图任务
def bao_tu(window_size):
    global is_start
    is_start = True
    open_huodong()
    if not get_rw("baotu_rw"):
        print("宝图任务已完成")
        button_baotu["text"] = "宝图（已完成）"
        return
    button_baotu["text"] = "宝图（执行中）"
    get_rw("choice_do")     # 选择任务
    time.sleep(1)
    get_rw("baotu_1")     # 查找并点击宝图任务
    time.sleep(1)
    button_baotu["text"] = "宝图（已完成）"

# 运镖任务
def yun_biao(window_size):
    global is_start
    is_start = True
    button_yunbiao["text"] = "运镖（进行中）"
    while is_start:
        open_huodong()
        if get_rw("yunbiao_rw"):
            time.sleep(1)
            get_rw("yasong")
            time.sleep(1)
        else:
            button_yunbiao["text"] = "运镖（已完成）"
            break
# 使用藏宝图
def cangbaotu():
    #打开包裹
    #找到并点击藏宝图
    do_action()

# 一键执行全部任务
def do_all():
    global is_start
    is_start = True
    # 自动点击
    button_quanbu["text"] = "全部执行(执行中)"
    times = 0   # 连续无任何操作的次数
    while is_start:
        if do_action():
            times = 0
            time.sleep(1)
        elif findpng("renwu.png"):
            x = window_size[0]+840
            y = window_size[1]+200
            xy = findpng("qidai.png")
            if xy is not None and xy[1] < y:
                y = y + 70
            click(x, y)
            times = 0
            time.sleep(2)
        else:
            time.sleep(2)
    button_quanbu["text"] = "全部执行(已完成)"
    return



def stop():
    global  is_start
    is_start = False
    button_baotu["text"] = "宝图"
    button_bangpai["text"] = "帮派"
    button_shimen["text"] = "师门"
    button_zhuagui["text"] = "带队抓鬼"
    button_quanbu["text"] = "全部执行"
    print("停止")

def SavePic():
    global window_region
    pyautogui.FAILSAFE = False
    img=pyautogui.screenshot(region=window_region)
    FileName = "./images/" + datetime.datetime.now().strftime('%H%M%S')
    img.save(FileName + ".png")
    """
    #后台截图
    hwnd = win32gui.FindWindow(None, "梦幻西游 - MuMu模拟器")
    app = QApplication(sys.argv)
    screen = QApplication.primaryScreen()
    img = screen.grabWindow(hwnd).toImage()
    img.save("./images/new.png")
    """


class MyThread(threading.Thread):
    def __init__(self, func, *args):
        super().__init__()

        self.func = func
        self.args = args

        self.setDaemon(True)
        self.start()  # 在这里开始

    def run(self):
        self.func(*self.args)


# 启动
if __name__ == "__main__":
    #global window_region
    screen_resolution = resolution()
    print(screen_resolution)
    window_size = get_window_info()
    print(window_size)
    if window_size is None:
        widow_region = (0,0,800,600)
    else:
        window_region = (window_size[0], window_size[1], window_size[2] - window_size[0], window_size[3] - window_size[1])
    global is_start
    # shimen(window_size)
    # zhua_gui(window_size)
    # bang_pai(window_size)
    # baotu(window_size)

    # 创建主窗口
    root = tk.Tk()
    root.title("梦幻西游手游辅助")
    root.minsize(300, 600)
    root.maxsize(300, 600)
    root.wm_attributes('-topmost', 1)
    # 创建按钮
    button_shimen = tk.Button(root, text=u"师门", command=lambda: MyThread(shi_men, window_size), width = 15,height = 2)
    button_shimen.place(relx=0.2, rely=0.15, width=100)
    button_shimen.pack()

    button_bangpai = tk.Button(root, text="帮派", command=lambda: MyThread(bang_pai, window_size), width = 15,height = 2)
    button_bangpai.place(relx=0.2, rely=0.35, width=200)
    button_bangpai.pack()

    button_baotu = tk.Button(root, text="宝图", command=lambda: MyThread(bao_tu,window_size), width = 15,height = 2)
    button_baotu.place(relx=0.4, rely=0.55, width=200)
    button_baotu.pack()

    button_zhuagui = tk.Button(root, text="带队抓鬼", command=lambda: MyThread(zhua_gui, window_size), width = 15,height = 2)
    button_zhuagui.place(relx=0.4, rely=0.65, width=100)
    button_zhuagui.pack()

    button_quanbu = tk.Button(root, text="全部执行", command=lambda: MyThread(do_all), width = 15,height = 2)
    button_quanbu.place(relx=0.4, rely=0.65, width=100)
    button_quanbu.pack()

    button_tingzhi = tk.Button(root,text=u"停止", command=lambda: MyThread(stop), width = 15,height = 2)
    button_tingzhi.place(relx=0.4, rely=0.85, width=200)
    button_tingzhi.pack()

    button_jietu = tk.Button(root,text=u"截图", command=lambda: MyThread(SavePic), width = 15,height = 2)
    button_jietu.place(relx=0.4, rely=0.95, width=200)
    button_jietu.pack()

    root.mainloop()
