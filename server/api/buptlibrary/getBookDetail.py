# -*- coding: utf-8 -*-
# 图书详细信息
# Get the detail infomation of one book according to the book's sid

import json
import re
import requests
import http.cookiejar

def get_book_detail(sid):

    sid = str(sid)
    session = requests.Session()
    session.cookies = http.cookiejar.CookieJar()

    Url = 'http://opac.bupt.edu.cn:8080/opac_two/guancang.do?rec_ctrl_id=' + sid
    detailUrl = 'http://opac.bupt.edu.cn:8080/opac_two/bookdetail?rec_ctrl_id=' + sid

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Host': 'opac.bupt.edu.cn:8080',
        'Referer': detailUrl
    }

    # get ISBN/ISSN
    detail_header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'Host': 'opac.bupt.edu.cn:8080',
        'Referer': detailUrl
    }

    res = session.get(Url, headers=header)
    detail_res = session.post(detailUrl, headers=detail_header)
    detail_text = detail_res.text
    json_txt = detail_text[2:]
    # print(json_txt)
    bookTemp = json.loads(json_txt)
    result = {}
    ISBN_ISSN = ''
    for item in bookTemp:
        # print(item)
        try:
            if item['s0'] == 'ISBN/ISSN':
                ISBN_ISSN = item['s1']
                # print(ISBN_ISSN)
                break
        except:
            try:
                ISBN_ISSN = item['isbn']
                # print(ISBN_ISSN)
            except:
                ISBN_ISSN = ''

    result['ISBN_ISSN'] = str(ISBN_ISSN.replace('-', '')[0:13])

    # get guang cang xin xi
    postdata = { 'rec_ctrl_id':sid }
    res = session.post(Url, headers=header, data=postdata)

    pos = re.findall("\[\{\"A\":\[(.*)\]\}\]",res.text)
    pos = '{"A":[' + str(pos[0]) + ']}'
    # pos = res.text[1:-3]
    enjson = json.loads(pos)
    bookInfo = enjson['A']
    amount = len(bookInfo)
    result['amount'] = str(amount)
    booklist = []
    for i in range(0, amount):
        del bookInfo[i]['colorset']
        del bookInfo[i]['yidiyujie']
        booklist.append(bookInfo[i])

    result['booklist'] = booklist
    return json.dumps(result,ensure_ascii=False)
