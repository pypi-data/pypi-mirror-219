import os
import random
import sys
from time import sleep

# Add the path to the Rust library to the sys.path list
rust_lib_path = os.path.abspath(r'C:\Users\Administrator\Desktop\rust_lib\target\debug')
sys.path.append(rust_lib_path)

# Import the Rust library for testing
opencv_lib_path = os.path.abspath(r'C:\tools\opencv\build\x64\vc16\bin')
sys.path.append(opencv_lib_path)

import windows_control
from windows_control import keyboard, mouse, window


def test_keyboard(input_key):
    # Test press_key
    keyboard.press(input_key)

    # Test release_key
    keyboard.release(input_key)

    # Test tap_key
    keyboard.tap(input_key)

    # Test press and release combination
    keyboard.press(input_key)
    keyboard.release(input_key)

    # Test press and tap combination
    keyboard.press(input_key)
    keyboard.tap(input_key)

    # Test release and tap combination
    keyboard.release(input_key)
    keyboard.tap(input_key)

    # Test press and release and tap combination
    keyboard.press(input_key)
    keyboard.release(input_key)
    keyboard.tap(input_key)
if __name__ == "__main__":
    # 0.test opencv

    # windows_control.test_opencv()
    # exit()

    # 1.test keyboard
    # test_keyboard('up')
    # test_keyboard('down')
    # test_keyboard('left')
    # test_keyboard('right')
    # test_keyboard('a')
    # test_keyboard('B')
    # test_keyboard('capslock')
    # exit()

    # test_keyboard('CTRL')
    # test_keyboard('CtRL')
    # test_keyboard('shift')
    # test_keyboard('z')
    # test_keyboard('Wc')
    # test_keyboard('C')
    # test_keyboard('F1')
    # test_keyboard('win')

    # keyboard.press('.')
    # keyboard.press('SHIFT')
    # # keyboard.press('CTRL')
    # keyboard.press('capslock')
    # # keyboard.release('capslock')
    # keyboard.press('c')
    # keyboard.press('w')
    # r = keyboard.get_pressed_key_index()
    # print(r)
    # r = keyboard.get_pressed_key_strs(r)
    # print(r)
    # print("================================================")
    # keyboard.release_all()
    # r = keyboard.get_pressed_key_index()
    # print(r)

    # exit()


    # 2.test mouse
    # mouse.move_to(400, 400)
    # mouse.left_click()
    # mouse.right_click()

    # 3.test window
    # window.open_app(r'C:\Windows\System32\calc.exe',True)
    # window.open_app(r'C:\Windows\System32\calc.exe',False)
    # window.open_app(r'D:\GAME\WinKawaks148+KOF97Plus\WinKawaks.exe',True)
    # window.open_app(r'D:\SOFTWARE\AB抓抓.exe',True)
    # exit()
    # win = window.Window('计算器','Windows.UI.Core.CoreWindow')
    # win = window.Window('计算器',None)
    # win = window.Window('计算器',"")
    # win = window.Window(None,'Windows.UI.Core.CoreWindow')
    # win = window.Window("",'Windows.UI.Core.CoreWindow')

    # win = window.Window("Kawaks 1.48 - Lost focus, paused","Afx:400000:0")
    # win = window.Window(None,"地下城与勇士")
    win = window.Window(None,"Afx:400000:0")
    win.activate()
    win.repos(200,200)
    win.resize(500,400)

    mouse.move_to(300,300)
    mouse.left_click()

    keyboard.tap("enter")
    sleep(1)


    win.record(False)
    # win.record(True)
    print("================================================")
    exit()
    # keys = ["w","a","s","d","j","k","u","i"]

    # while True:
    #     # sleep(0.01)
    #     win.capture_screen()

    #     random_key = random.choice(keys)
    #     print(f"selected key:{random_key}")
    #     key_strs = keyboard.get_pressed_key_strs()
    #     if random_key in key_strs:
    #         keyboard.release(random_key)
    #     else:
    #         keyboard.press(random_key)

    # win.capture_screen()

    # win = window.Window("","Afx:400000:0")
    # win = window.Window("Kawaks 1.48 - Lost focus, paused",None)
    # win = window.Window("Kawaks 1.48 - Lost focus, paused","")
    # win.repos(-50,None)
    # win.repos(None,10)
    # win.resize(800,300)
    # win.resize(0,400)
    # win.maximize()
    # print(f"is minimized:{win.is_minimized()}")
    # sleep(1)
    # win.minimize()
    # print(f"is minimized:{win.is_minimized()}")
    # print(f"is activated:{win.is_activated()}")

    # win.maximize()
    # print(f"is minimized:{win.is_minimized()}")
    # print(f"is activated:{win.is_activated()}")

    win.activate()
    print(f"is activated:{win.is_activated()}")



    print(win.handle)
