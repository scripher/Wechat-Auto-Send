import time
import datetime
import struct
import win32clipboard
import win32con
import win32gui
import keyboard


# =======准备工作=======

# 遍历输出窗口名字，作为被win32gui.EnumWindows调用的函数，用于找到自己想要的窗口的class和title，确保能正确抓到句柄
def enum_window_name(hwnd, _):
    title_name = win32gui.GetWindowText(hwnd)
    class_name = win32gui.GetClassName(hwnd)
    print(f"{hwnd} | {class_name} | {title_name}")

# win32gui.EnumWindows(enum_window_name, None)

# =======准备工作=======




# 把文本txt复制到剪贴板
def copy_txt(txt):
    win32clipboard.OpenClipboard()  # 打开剪贴板
    win32clipboard.EmptyClipboard() # 清空剪贴板
    win32clipboard.SetClipboardData(win32con.CF_UNICODETEXT, txt) # 写入剪贴板，第一个是一个常量15，表示复制的东西是一系列文件
    win32clipboard.CloseClipboard() # 关闭剪贴板
    return

# 把指定的路径raw_path中的文件复制到剪贴板
def copy_file(raw_path):
    # DROPFILE格式，有20字节的header，可参考官方文档：https://learn.microsoft.com/en-us/windows/win32/api/shlobj_core/ns-shlobj_core-dropfiles
    # 在资源管理器中复制文件本质上就是在制作一个这样的格式，放到剪贴板里，这里相当于用代码模拟了这个过程
    header = struct.pack("<IiiII", 20, 0, 0, 0, 1)
    path = (raw_path + "\0\0").encode("utf-16-le")  # 需要以两个\0结尾，表示结束
    combine = header + path

    win32clipboard.OpenClipboard()  # 打开剪贴板
    win32clipboard.EmptyClipboard() # 清空剪贴板
    win32clipboard.SetClipboardData(win32con.CF_HDROP, combine) # 写入剪贴板，第一个是一个常量15，表示复制的东西是一系列文件
    win32clipboard.CloseClipboard() # 关闭剪贴板
    return

# 抓取微信窗口句柄，获取焦点
def get_wechat_window():
    hwnd = win32gui.FindWindow("WeChatMainWndForPC", "Weixin")  # 获取窗口的句柄
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW) # 从隐藏状态恢复到可见状态，如果本身就可见则什么都不做
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # 最小化状态恢复到非最大化的正常窗口状态，如果本身就是则什么都不做
    win32gui.SetForegroundWindow(hwnd)

# 指定微信名和文件路径，发送文件
def sent_file(usernames, raw_path, is_add_info = 0):
    sep_time = 0.5

    for name in usernames:
        get_wechat_window() # 获取焦点
        keyboard.send("ctrl+f") # 进入搜索框
        copy_txt(name)  # 把微信名复制到剪贴板
        time.sleep(sep_time)
        keyboard.send("ctrl+v") # 粘贴微信名
        time.sleep(sep_time)
        keyboard.send("enter")  # 回车进入这个人的聊天窗口
        copy_file(raw_path)
        time.sleep(sep_time)
        keyboard.send("ctrl+v") # 粘贴文件
        time.sleep(sep_time)
        keyboard.send("enter")  # 回车发送
        time.sleep(sep_time)

        if (is_add_info == 1):
            vtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            copy_txt(f"注：此消息由脚本于{vtime}自动发送. ---By Scripher")
            keyboard.send("ctrl+v")
            time.sleep(sep_time)
            keyboard.send("enter")
            time.sleep(sep_time)
        print(f"{name}'s file has been sent successfully.")
    return

names = ["张三", "李四"]
file_path = r"D:\XD\quiz-2.pdf"
sent_file(names, file_path, 1)




