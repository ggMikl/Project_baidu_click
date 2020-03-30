import pyautogui
import random
import time
import pyperclip

class Action(object):
    def move(self,x, y, duration, tween):
        pyautogui.moveTo(x=x, y=y, duration=duration, tween=tween)
        print('鼠标移动')

    def scroll(self,scroll_num):
        pyautogui.scroll(scroll_num)

    def click(self):
        pyautogui.click()
        print('点击')

    def close_window(self):
        pyautogui.hotkey('ctrlleft', 'w')  # 关闭当前页面
        print('关闭当前页面')

    def sleep(self,sec):
        time.sleep(sec)

    def press(self,key):
        print('点击:',key)
        pyautogui.press(key)

    def safe_random_Move(self,duration,tween):
        print('鼠标移动:安全位置随机')
        x = random.randint(1550, 1800)
        y = random.randint(250, 600)
        pyautogui.moveTo(x=x, y=y, duration=duration, tween=tween)

    def element_Move(self,id,duration,tween):
        print('鼠标移动:指定元素')
        random_x = random.randint(int(id.size['width'] * (1 / 5)), int(id.size['width'] * (4 / 5)))
        random_y = random.randint(int(id.size['height'] * (2 / 5)), int(id.size['height'] * (3 / 5)))
        x = id.location['x'] + random_x
        y = id.location['y'] + random_y
        pyautogui.moveTo(x=x, y=y, duration=duration, tween=tween)

    def copy(self,words):
        print('复制',words)
        pyperclip.copy(words)

    def paste(self):
        print('粘贴')
        pyautogui.hotkey('ctrlleft', 'v')





