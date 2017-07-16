# -*- coding: utf-8 -*-
# 借阅排行榜

import datetime
import json

import re
import requests
import http.cookiejar
from bs4 import BeautifulSoup

bookDetailBaseUrl = 'http://opac.bupt.edu.cn:8080/opac_two/search2/'

borrowRankingUrl = 'http://opac.bupt.edu.cn:8080/opac_two/top/top_detail.jsp?type=circul.circulog_A&cname=%C2%BD%C3%A8%C3%94%C3%84%C3%85%C3%85%C3%90%C3%90%C2%B0%C3%B1'
searchRankingUrl = 'http://opac.bupt.edu.cn:8080/opac_two/top/top_detail.jsp?type=opac.n_search_log&cname=%C2%BC%C3%AC%C3%8B%C3%B7%C3%85%C3%85%C3%90%C3%90%C2%B0%C3%B1'
collectRankingUrl = 'http://opac.bupt.edu.cn:8080/opac_two/top/top_detail.jsp?type=opac.n_collection&cname=%C3%8A%C3%95%C2%B2%C3%98%C3%85%C3%85%C3%90%C3%90%C2%B0%C3%B1'
reviewRankingUrl = 'http://opac.bupt.edu.cn:8080/opac_two/top/top_detail.jsp?type=opac.n_review&cname=%C3%8A%C3%A9%C3%86%C3%80%C3%85%C3%85%C3%90%C3%90%C2%B0%C3%B1'
lookRankingUrl = 'http://opac.bupt.edu.cn:8080/opac_two/top/top_detail.jsp?type=opac.n_look_log&cname=%C2%B2%C3%A9%C2%BF%C2%B4%C3%85%C3%85%C3%90%C3%90%C2%B0%C3%B1'

def url_to_sid(url):
    return re.findall('sid=(.*)&', url)[0]

def get_borrow_ranking():

    header_search = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Host': 'opac.bupt.edu.cn:8080',
        'Referer': borrowRankingUrl
    }

    starttime = datetime.datetime.now()

    session = requests.Session()
    session.cookies = http.cookiejar.CookieJar()

    # 借阅排行榜
    res = session.get(borrowRankingUrl, headers=header_search)
    res.encoding = 'gb2312'
    content = res.text
    rankingSoup = BeautifulSoup(content,'html.parser')
    rankDiv = rankingSoup.find('form',{'id':'paihang_detail'})
    r_trs = rankDiv.find_all('tr')
    result = {}
    result['amount'] = len(r_trs)
    booklist = []

    for r_index, r_tr in enumerate(r_trs):
        if r_index == 0:
            continue
        booktds = r_tr.find_all('td')
        rank_book_ranking = booktds[0].text
        rank_book_title = booktds[1].text
        rank_book_link = bookDetailBaseUrl + booktds[1].find('a')['href']
        rank_book_clc = booktds[2].text
        rank_book_times = booktds[3].text
        single_book = {}
        single_book['book_ranking'] = rank_book_ranking
        single_book['book_title'] = rank_book_title
        single_book['book_sid'] = url_to_sid(rank_book_link)
        single_book['book_clc'] = rank_book_clc
        single_book['book_times'] = rank_book_times
        booklist.append(single_book)


        # print(rank_book_ranking,rank_book_times,rank_book_title,rank_book_clc, rank_book_link)
    result['booklist'] = booklist

    endtime = datetime.datetime.now()
    print('[Time] [Get Borrow Ranking] Using ' + str((endtime - starttime).seconds) + 's')

    return json.dumps(result, ensure_ascii=False)
