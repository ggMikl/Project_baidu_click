from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pyautogui
from Class.User import User
import info
from Class.Coordinate import Coordinate
import random

tween = pyautogui.easeInOutQuad
MODEL = 'ADVERTISEMENT'
scroll_radio = 3.6
SLEEP_1 = random.randint(2, 3)
SLEEP_2 = random.randint(2, 3)

search_content = '河源龙光城'  # 搜索内容
ignore_content = ['heyuan.loupan.com','广州楼盘网网络科技']  # 忽略对象
focus_content = ['heyuan.goufang.com']  # 特殊处理的对象 网址:对象
page_sum_num = 4  # 点到第几页


def process(id_list,browser,user,page_locaotion,page_num):
    # 一些构建参数
    top_height = browser.find_element_by_xpath('//*[@id="s_tab"]/div').location['y'] + 10
    change_height = 0
    # 构建网页坐标
    coordinate_BaiDu = Coordinate(browser, top_height)
    screen_start = coordinate_BaiDu.screen_start
    screen_end = coordinate_BaiDu.screen_end
    screen_mid = coordinate_BaiDu.screen_mid
    # 网页一打开浏览框在第一个
    current_screen = coordinate_BaiDu.screen_start
    xpath_pre, xpath_af = info.xpath_model(MODEL)
    ALT_Y = 0  # Y变动量
    scroll_tag = 0
    scroll_tag_mid = 0
    for target_id in id_list:
        #记录每次点击之前之后ID的位置
        target_xpath = xpath_pre + target_id + xpath_af
        id = browser.find_element_by_xpath(target_xpath)
        x, y = info.get_safe_location(id)
        SCREEN = info.classify(id, screen_start, screen_end, screen_mid)
        next_page = browser.find_element_by_xpath('//*[@id="page"]/a[' + page_locaotion + ']')
        print('pre_click')
        for my_id in id_list:
            target_xpath = xpath_pre + my_id + xpath_af
            myid = browser.find_element_by_xpath(target_xpath)
            print(my_id,': ',info.get_safe_location(myid))
        pre_next_page = browser.find_element_by_xpath('//*[@id="page"]/a[' + page_locaotion + ']')
        print('next_page_x, next_page_y :', info.get_safe_location(pre_next_page))
        if SCREEN['class'] == 'START':
            print('SCREEN:', SCREEN)
            # ALT_Y = ALT_Y + change_height  # 没有滚动，变动量为0
            # y = y - ALT_Y  # 没有滚动Y不变
            current_screen = screen_start  # 此时的浏览框
            user.move(x, y, 0.5, tween)
        elif SCREEN['class'] == 'END':
            print('SCREEN:', SCREEN)
            if scroll_tag == 0:  # 到底部之后只滚动一次
                scroll_tag = 1
                target_screen = screen_end  # 目标浏览框是最后一个
                distance = target_screen['end'] - current_screen['end'] + change_height  # 计算当前浏览框到目前浏览框的距离
                scroll_num = round(distance * scroll_radio)   # 计算滚动量
                user.scroll(-scroll_num)  # 滚动
                user.sleep(1)
                current_screen = screen_end  # 当前浏览框是最后一个
                ALT_Y = ALT_Y + distance - change_height # 滚动到底部，有变动量
            else:
                ALT_Y = ALT_Y + change_height
            y = y - ALT_Y
            user.move(x, y, 0.5, tween)
        elif SCREEN['class'] == 'MID':
            print('SCREEN:', SCREEN)
            if scroll_tag_mid == 0:  # 有复数的情况，先这样写
                scroll_tag_mid = 1
                target_screen = screen_mid[SCREEN['num']]
                distance = target_screen['start'] - current_screen['start'] + change_height
                scroll_num = round(distance * scroll_radio)  # 计算滚动量
                user.scroll(-scroll_num)  # 滚动
                user.sleep(1)
                current_screen = screen_mid[SCREEN['num']]
                ALT_Y = ALT_Y + distance
            y = y - ALT_Y
            user.move(x, y, 0.5, tween)
        pre_click_height = browser.execute_script('return document.body.scrollHeight ')
        user.sleep(1)
        user.click() #点这个广告
        print('af_click')
        for my_id in id_list:
            target_xpath = xpath_pre + my_id + xpath_af
            myid = browser.find_element_by_xpath(target_xpath)
            print(my_id,': ',info.get_safe_location(myid))
        af_next_page = browser.find_element_by_xpath('//*[@id="page"]/a[' + page_locaotion + ']')
        print('next_page_x, next_page_y :', info.get_safe_location(af_next_page))
        user.safe_random_Move(0.3, tween)
        user.sleep(1)
        loop = info.get_random_int(5, 10)
        user.random_scroll(loop, 300, 0.3)
        user.sleep(SLEEP_2)
        browser.switch_to.window(browser.window_handles[len(browser.window_handles) - 1]) #切换到当前打开的界面，即广告内页
        focus_op(target_id,user,browser)#点红包关闭
        if click_inner(browser, user) :#找到动态、户型、阅读全文的a标签,返回一个布尔值判断有没有这个标签
            user.sleep(1)
            user.click()  # 点击这个a标签
            user.safe_random_Move(0.3, tween)
            user.sleep(1)
            loop = info.get_random_int(5, 10)
            user.random_scroll(loop, 300, 0.3)
            if len(browser.window_handles) == 3:
                browser.switch_to.window(browser.window_handles[len(browser.window_handles) - 1])  # 此时打开了一个新的标签页 动态or户型
                user.sleep(5)
                user.close_window()  # 关闭当前标签
            browser.switch_to.window(browser.window_handles[len(browser.window_handles) - 1])  # 此时切换到广告内页
        user.sleep(5)
        user.close_window()
        browser.switch_to.window(browser.window_handles[len(browser.window_handles) - 1])
        click_height = browser.execute_script('return document.body.scrollHeight ')
        if click_height != pre_click_height:
            change_height = click_height - pre_click_height
        else:
            change_height = 0
        print('change_height:', change_height)
        coordinate_BaiDu = Coordinate(browser, top_height)
        screen_start = coordinate_BaiDu.screen_start
        screen_end = coordinate_BaiDu.screen_end
        screen_mid = coordinate_BaiDu.screen_mid
    if page_num < 5 :
        print('下一页')
        next_page_x, next_page_y = info.get_safe_location(next_page)
        print('next_page_x, next_page_y :', info.get_safe_location(next_page))
        if scroll_tag == 0:
            target_screen = screen_end  # 目标浏览框是最后一个
            distance = target_screen['start'] - current_screen['start'] + change_height  # 计算当前浏览框到目前浏览框的距离
            scroll_num = round(distance * scroll_radio)  # 计算滚动量
            user.scroll(-scroll_num)  # 滚动
            ALT_Y = ALT_Y + distance - change_height  # 滚动到底部，有变动量
        else:
            ALT_Y = ALT_Y + change_height
        next_page_y = next_page_y - ALT_Y
        print(next_page_y)
        user.sleep(2)
        user.move(next_page_x, next_page_y, 0.5, tween)
        pyautogui.click()
        user.sleep(5)
    else:
        browser.quit()


def inner_process(id,user,coordinate_Web):
    screen_start = coordinate_Web.screen_start
    screen_end = coordinate_Web.screen_end
    screen_mid = coordinate_Web.screen_mid
    current_screen = coordinate_Web.screen_start
    ALT_Y = 0  # Y变动量
    x, y = info.get_safe_location(id)
    SCREEN = info.classify(id, screen_start, screen_end, screen_mid)
    if SCREEN['class'] == 'START':
        print('SCREEN:', SCREEN)
        ALT_Y = 0  # 没有滚动，变动量为0
        y = y - ALT_Y  # 没有滚动Y不变
        user.move(x, y, 0.5, tween)
    elif SCREEN['class'] == 'END':
        print('SCREEN:', SCREEN)
        target_screen = screen_end  # 目标浏览框是最后一个
        distance = target_screen['start'] - current_screen['start']  # 计算当前浏览框到目前浏览框的距离
        scroll_num = round(distance * scroll_radio)  # 计算滚动量
        user.scroll(-scroll_num)  # 滚动
        user.sleep(1)
        ALT_Y = ALT_Y + distance  # 滚动到底部，有变动量
        y = y - ALT_Y
        user.move(x, y, 0.5, tween)
    elif SCREEN['class'] == 'MID':
        print('SCREEN:', SCREEN)
        target_screen = screen_mid[SCREEN['num']]
        distance = target_screen['start'] - current_screen['start']
        scroll_num = round(distance * scroll_radio)  # 计算滚动量
        user.scroll(-scroll_num)  # 滚动
        user.sleep(1)
        ALT_Y = ALT_Y + distance
        y = y - ALT_Y
        user.move(x, y, 0.5, tween)

def focus_op(target_id,user,browser):
    for focus in user.focus_content:
        if target_id == focus:
            print(target_id)
            print(focus)
            user.sleep(0.5)
            close = browser.find_element_by_xpath('//*[@id="close"]')
            x = close.location['x'] + close.size['width'] / 2
            y = close.location['y'] + close.size['height'] / 2
            user.move(x, y, 0.5,pyautogui.easeInOutQuad)
            user.click()
            user.safe_random_Move(0.3, tween)
        else:
            print('没有')

def click_inner(browser,user):
    targets = browser.find_elements_by_partial_link_text('动态')
    if targets is None:
        targets = browser.find_elements_by_partial_link_text('户型')
    coordinate_Web = Coordinate(browser, 65)
    target = []
    if len(targets) > 0:
        for target_id in targets:
            if target_id.location['y'] > coordinate_Web.screen_start['end'] / 2 and target_id.size[
                'height'] > 0 and target_id.size['width'] > 0:
                target.append(target_id)
        if len(target) > 0:
            inner_id = target[0]
            print(inner_id.location)
            inner_process(inner_id, user,coordinate_Web)
        else:
            targets = browser.find_elements_by_partial_link_text('阅读全文')
            if len(targets) > 0:
                for target_id in targets:
                    if target_id.location['y'] > coordinate_Web.screen_start['end'] / 2 and target_id.size[
                        'height'] > 0 and target_id.size['width'] > 0:
                        target.append(target_id)
                inner_id = target[0]
                print(inner_id.location)
                inner_process(inner_id, user, coordinate_Web)
        return True
    else:
        print('没有直接走')
        return False




if __name__ == '__main__':
    user = User(search_content, ignore_content, focus_content, page_sum_num)
    chrome_options = Options()
    # 设置浏览器采用无痕方式
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    chrome_options.add_argument('--incognito')
    # 启动浏览器
    browser = webdriver.Chrome(options=chrome_options)
    browser.maximize_window()
    browser.implicitly_wait(3)  # 等待3秒
    browser.get("https://www.baidu.com")
    user.press('f11')
    btn_input = browser.find_element_by_xpath('//input[@id="kw"]')
    user.element_Move(btn_input, 0.5, tween)
    user.click()
    user.copy(user.search_content)
    user.paste()
    btn_search = browser.find_element_by_xpath('//input[@id="su"]')
    user.element_Move(btn_search, 0.5, tween)
    user.click()

    # 搜索页已经成功获取

    for i in range(1, user.page_sum_num + 1):
        user.safe_random_Move(0.5, tween)
        user.sleep(1)
        loop = info.get_random_int(5, 10)
        user.random_scroll(loop, 600, 0.3)
        user.scroll(SLEEP_1)
        page_locaotion = '10'
        browser.switch_to.window(browser.window_handles[len(browser.window_handles) - 1])
        id_list, focus_id = info.reduce_ID(browser, user.ignore_content, user.focus_content)
        # while len(id_list) > 3:
            # id_list.pop()
        print('需要遍历的ID列表:', id_list)
        print('需要注意的ID列表', focus_id)
        if i > 1:
            page_locaotion = '11'
        if id_list:
            process(id_list, browser, user, page_locaotion, i)
        else:
            print('没有广告下一页')
