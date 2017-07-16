# -*- coding: utf-8 -*-
# OK 借阅信息

# 保存借书信息的类
import json

from api.buptlibrary.checkAuth import checkauth
from bs4 import BeautifulSoup

lib_jieshuxinxi_url = 'http://opac.bupt.edu.cn:8080/opac_two/reader/jieshuxinxi.jsp'

header_libinfo = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Host':'opac.bupt.edu.cn:8080',
    'Referer':'http://opac.bupt.edu.cn:8080/opac_two/reader/infoList.jsp'
}



class jieshu_info(object):
    def __init__(self, number, name, book_barcode, department_name, liutong, date):
        self.number = number
        self.name = name
        self.book_barcode = book_barcode
        self.department_name = department_name
        self.liutong = liutong
        self.date = date

    def getNumber(self):
        return self.number

    def getName(self):
        return self.name

    def getBook_barcode(self):
        return self.book_barcode

    def getDepartment_name(self):
        return self.department_name

    def getLiutong(self):
        return self.liutong

    def getDate(self):
        return self.date

    def getAll(self):
        output = {}
        output['book_xuhao'] = self.number.strip()
        output['book_title'] = self.name.strip()
        output['book_barcode'] = self.book_barcode.strip()
        output['department_name'] = self.department_name.strip()
        output['liutong'] =self.liutong.strip()
        output['should_return_date'] = self.date.strip()

        # return 'number:'+self.number+', name:'+self.name+', book_barcode:'+self.book_barcode+', department_name:'+self.department_name+', liutong:'+self.liutong+', date:'+self.date
        return output


# 爬虫获取借书信息
def jieshuxinxi(soup):
    # print(soup)
    jieshu_table_items = soup.find_all('table')[0]
    jieshu_tr_items = jieshu_table_items.find_all('tr', class_=["td_color_1", "td_color_2"])
    i = 0
    jieshu_infs = []
    for jieshu_tr_item in jieshu_tr_items:
        jieshu_td_item = jieshu_tr_item.find_all('td')
        jieshu_inf = jieshu_info(jieshu_td_item[1].text, jieshu_td_item[2].text, jieshu_td_item[3].text,
                                 jieshu_td_item[4].text, jieshu_td_item[5].text, jieshu_td_item[6].text)
        jieshu_infs.append(jieshu_inf)
        i = i + 1
    return jieshu_infs


# 返回json格式的借书信息
def get_borrow_info(username, password):
    auth_status, session  = checkauth(username, password)
    if not auth_status:
        return False

    response_to_jieshuxinxi = session.get(lib_jieshuxinxi_url, headers=header_libinfo)
    response_to_jieshuxinxi.encoding = 'gb2312'
    content = response_to_jieshuxinxi.text
    soup = BeautifulSoup(content, "html.parser")
    # xujie(1, soup, session)
    jieshu_infs = jieshuxinxi(soup)
    res = {}
    booklist = []
    res['amount'] = str(len(jieshu_infs))
    for j_index, jieshu_inf in enumerate(jieshu_infs):
        booklist.append(jieshu_inf.getAll())
    res['booklist'] = booklist
    # print(res)
    return json.dumps(res, ensure_ascii=False)