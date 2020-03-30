from Class.Action import Action
class User(Action):
    #username
    #password
    search_content = '' #搜索内容
    ignore_content = [] #忽略对象
    focus_content = [] #特殊处理的对象 网址:对象
    page_sum_num = 0 #点到第几页

    def __init__(self,search_content,ignore_content,focus_content,page_sum_num):
        self.search_content = search_content
        self.ignore_content = ignore_content
        self.focus_content = focus_content
        self.page_sum_num = page_sum_num
        print('初始化用户')

    def random_scroll(self,loop,scroll,sec):
        #loop滚动次数
        #scroll滚动量
        #sec间隔时间
        print('随机滚动')
        for loop_num in range(1, loop + 1):
            self.scroll(-scroll)
            self.sleep(sec)
        for loop_num in range(1, loop + 1):
            self.scroll(scroll)
            self.sleep(sec)

    def my_scroll(self,scroll):
        self.scroll(scroll)
