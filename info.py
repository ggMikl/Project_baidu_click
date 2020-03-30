from bs4 import BeautifulSoup
from bs4 import Comment,Tag,NavigableString
import random

def get_soup(browser):
    html = browser.page_source
    soup = BeautifulSoup(html, 'lxml')
    return soup

def get_target(soup):
    id_list = []
    target_list = []
    mark_comment = soup.new_string(" pc jieou new ", Comment)
    content_left = soup.find(id='content_left')
    for i in content_left:  # 定位到主要内容
        if i == mark_comment:  # 如果直接就找到了
            target_div = i.next_sibling  # 这里是该网页构造造成，comment下面有个没有任何内容的NavigableString，下一个才是有内容的Tag即广告本体
            target_list.append(target_div)
            id_list.append(target_div['id'])
        if isinstance(i, Tag):  # 只要Tag因为要的东西都在Tag里
            for j in i:  # 遍历这些Tag的内部
                if j == mark_comment:  # 找到这些Tag内部有关mark_comment的element
                    target_div = j.next_sibling  # 这里是该网页构造造成，comment下面有个没有任何内容的NavigableString，下一个才是有内容的Tag即广告本体
                    target_list.append(target_div)
                    id_list.append(target_div['id'])
    return id_list,target_list

def get_special_id(target_list,soup,ignore):
    ignore_id = []
    protect_String = soup.new_string(ignore, NavigableString)
    for target_div in target_list:
        for k in target_div.descendants:
            if k == protect_String:
                print('The special id is:' + target_div['id'])  # 获得需要关注的ID
                ignore_id.append(target_div['id'])
    return ignore_id

def ignore(id_list,ignore_id):
    id_list_ = id_list
    if ignore_id :
        for i in ignore_id:
            if i is not None:
                id_list_.remove(i)
            else:
                print('ignore_id is None:')
    return id_list_

def reduce_ID(browser,ignore_array,focus_array):
    focus_id = []
    soup = get_soup(browser)
    id_list, target_list = get_target(soup)
    for focus in focus_array:
        focus_id.append(get_special_id(target_list,soup,focus ))
    for id in ignore_array:
        ignore_id = get_special_id(target_list,soup,id)
        id_list = ignore(id_list,ignore_id)
    return id_list,focus_id

def get_random_int(star,end):
    return random.randint(star, end)

def xpath_model(MODEL):
    xpath_pre = ''
    xpath_af = ''
    if MODEL == 'COMMON':
        xpath_pre = '//*[@id="'
        xpath_af = '"]/h3/a'
    elif MODEL == 'ADVERTISEMENT':
        xpath_pre = '//*[@id="'
        xpath_af = '"]/div[1]/h3/a[1]'
    elif MODEL == 'INNER-LINK':
        xpath_pre = ''#
        xpath_af = ''
    return xpath_pre, xpath_af

def get_safe_location(id):
    random_x = random.randint(int(id.size['width'] * (1 / 5)), int(id.size['width'] * (4 / 5)))
    random_y = random.randint(int(id.size['height'] * (2 / 5)), int(id.size['height'] * (3 / 5)))
    x = id.location['x'] + random_x
    y = id.location['y'] + random_y
    return x,y

def classify(id,screen_start,screen_end,screen_mid):#分类id
    if id.location['y'] < screen_start['end']:
        print('第一浏览框')
        return {'class':'START'}
    elif id.location['y'] > screen_end['start']:
        print('最后一个浏览框')
        return {'class':'END'}
    elif screen_start['end'] < id.location['y'] < screen_end['start']:
        for k,v in screen_mid.items():
            if v['start'] < id.location['y'] < v['end']:
                print('第%d'%k + '个中间浏览框')
                # return '%d'%k
                return {'class':'MID','num':k}
    else:
        return {'id':id.location['y'] }
