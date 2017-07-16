# -*- coding: utf-8 -*-
# OK 检查用户认证

import requests
import http.cookiejar
from bs4 import BeautifulSoup as bs

header={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'
}

header_lib = {
    'Host':'opac.bupt.edu.cn:8080',
    'Referer':'http://opac.bupt.edu.cn:8080/opac_two/login/caslogin.jsp',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'Accept-Encoding':'utf8',
    'Accept-Language':'zh-CN,zh;q=0.8'
    # 'Host':'opac.bupt.edu.cn:8080',
    # 'Referer':'http://opac.bupt.edu.cn:8080/opac_two/login/caslogin.jsp'
}

header_lib_search = {
    'Host':'opac.bupt.edu.cn:8080',
    'Origin':'http://opac.bupt.edu.cn:8080',
    'Referer':'http://opac.bupt.edu.cn:8080/opac_two/search2/search_simple.jsp?search_no_type=Y&snumber_type=Y&show_type=A',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
}

url = 'http://auth.bupt.edu.cn/authserver/login?service=http%3A%2F%2Fopac.bupt.edu.cn%3A8080%2Fopac_two%2Flogin%2Fcaslogin.jsp'
lib_url = 'http://opac.bupt.edu.cn:8080/opac_two/reader/infoList.jsp#'


def getLt(str):
    lt=bs(str,'html.parser')
    dic={}
    for inp in lt.form.find_all('input'):
        if(inp.get('name'))!=None:
            dic[inp.get('name')]=inp.get('value')
    return dic


def checkauth(username, password):

    session=requests.Session()
    session.cookies=http.cookiejar.CookieJar()
    r=session.get(url,headers=header)
    dic=getLt(r.text)
    postdata={
        'username':username,
        'password':password,
        'lt':dic['lt'],
        'execution':'e1s1',
        '_eventId':'submit',
        'rmShown':'1'
    }

    response=session.post(url,data=postdata,headers=header)
    response_to_index = session.get(lib_url, headers=header_lib)
    response_to_index.encoding = 'gb2312'
    content = response_to_index.text
    auth_soup = bs(content, 'html.parser')
    checkLibdiv = auth_soup.find('div',{'id':'my_lib'})
    res = ''
    if not checkLibdiv:
        res = False
    else:
        res = True
        print('auth pass')
    return res, session

