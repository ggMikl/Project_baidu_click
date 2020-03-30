def get_mid(screen_num,screen_size,screen_end):
    num_screen = screen_num - 2  # 中间浏览框的数量
    if num_screen > 0:  # 起码有3个浏览框
        screen_mid = {}
        for i in range(1,num_screen + 1):  #
            start_postion = screen_size['height'] * i
            end_postion = screen_size['height'] * (i + 1)
            if end_postion > screen_end['start']:
                screen_mid[i] = {'start': start_postion, 'end': screen_end['start']}
            else:
                screen_mid[i] = {'start': start_postion, 'end': end_postion}
        return screen_mid
    return None

class Coordinate():
    window_size = {}
    html_size = {}
    top_height = 0
    screen_size = {}
    html_effect_size = {}
    screen_num = 0
    screen_start = {}
    screen_end = {}
    html_screen_location = {}
    screen_mid = {}
    screen_mid = {}
    def __init__(self, browser,top_height):
        self.window_size = browser.get_window_size()  # 浏览器大小
        js = 'return document.body.scrollHeight '
        foot = browser.execute_script(js)
        self.html_size = {'width': self.window_size['width'],
                          'height': foot }  # 网页的整体大小
        # self.top_height = browser.find_element_by_xpath('//*[@id="s_tab"]/div').location[
        #                       'y'] + self.aj_start_num  # 顶部要忽略条
        self.top_height = top_height
        self.screen_size = {'width': self.window_size['width'],
                            'height': self.window_size['height'] - self.top_height}  # 浏览框大小
        self.html_effect_size = {'width': self.window_size['width'],
                                 'height': self.html_size['height'] - self.top_height}  # 网页整体有效大小
        self.screen_num = self.html_effect_size['height'] // self.screen_size['height']  # 浏览框数量
        if self.html_effect_size['height'] % self.screen_size['height']:  # 有余数要+1
            self.screen_num = self.screen_num + 1

        self.screen_start = {'start': self.top_height, 'end': self.window_size['height']}  # 第一个浏览框在网页上的定位
        self.screen_end = {'start': self.html_size['height'] - self.screen_size['height'],
                           'end': self.html_size['height']}  # 最后一个浏览框在网页上的定位
        self.html_screen_location = {'start': self.screen_start['start'],
                                     'end': self.screen_start['end']}  # 当前浏览框在网页上的定位
        self.screen_mid = get_mid(self.screen_num, self.screen_size, self.screen_end)  # 中间浏览框在网页上的定位
        # print('浏览器大小:', self.window_size)
        print('网页的整体大小:', self.html_size)
        # print('顶部要忽略条高度:', self.top_height)
        # print('浏览框大小:', self.screen_size)
        # print('网页整体有效大小:', self.html_effect_size)
        # print('浏览框数量:', self.screen_num)
        # print('第一个浏览框在网页上的定位:', self.screen_start)
        print('最后一个浏览框在网页上的定位:', self.screen_end)
        print('浏览框在网页上的初始定位:', self.html_screen_location)
        print('中间浏览框在网页上的定位:', self.screen_mid)

