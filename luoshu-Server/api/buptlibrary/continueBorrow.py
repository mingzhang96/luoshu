# -*- coding: utf-8 -*-
# 续借
from bs4 import BeautifulSoup

lib_xujie_url = 'http://opac.bupt.edu.cn:8080/opac_two/reader/jieshuxinxi.jsp'
lib_jieshuxinxi_url = 'http://opac.bupt.edu.cn:8080/opac_two/reader/jieshuxinxi.jsp'

header_lib_xujie = {
    'Host':'opac.bupt.edu.cn:8080',
    'Origin':'http://opac.bupt.edu.cn:8080',
    'Referer':'http://opac.bupt.edu.cn:8080/opac_two/reader/jieshuxinxi.jsp',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}

header_libinfo = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Host':'opac.bupt.edu.cn:8080',
    'Referer':'http://opac.bupt.edu.cn:8080/opac_two/reader/infoList.jsp'
}

xujie_data = {
    'action':'Renew',
    'book_barcode':'',
    'department_id':'',
    'library_id':'',
    'reader_barcode':'',
    'status':''
}


# 续借（第几本书（从0开始算起），soup，session）
def continue_borrow(number, session):

    # print('Enter xujie')
    response_to_jieshuxinxi = session.get(lib_jieshuxinxi_url, headers=header_libinfo)
    response_to_jieshuxinxi.encoding = 'gb2312'
    content = response_to_jieshuxinxi.text

    soup = BeautifulSoup(content, 'html.parser')

    xujie_items = soup.find_all('input', class_="copy")
    xujie_item = xujie_items[number]
    # print(xujie_item)
    xujie_info = xujie_item['onclick'].split("'")
    xujie_data['book_barcode'] = xujie_info[3]
    xujie_data['department_id'] = xujie_info[5]
    xujie_data['library_id'] = xujie_info[7]
    xujie_data['reader_barcode'] = xujie_info[9]
    xujie_data['status'] = xujie_info[11]
    response_to_xujie_jieshuxinxi = session.post(lib_xujie_url, headers=header_lib_xujie, data=xujie_data)
    response_to_xujie_jieshuxinxi.encoding = 'gb2312'
    content = response_to_xujie_jieshuxinxi.text
    print('[success] xujie')
    return True