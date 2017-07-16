# -*- coding: utf-8 -*-
# 搜索排行榜

import datetime
import json
import requests
import http.cookiejar
from bs4 import BeautifulSoup
from api.buptlibrary.terminalColors import TerminalColors

bookDetailBaseUrl = 'http://opac.bupt.edu.cn:8080/opac_two/search2/'

borrowRankingUrl = 'http://opac.bupt.edu.cn:8080/opac_two/top/top_detail.jsp?type=circul.circulog_A&cname=%C2%BD%C3%A8%C3%94%C3%84%C3%85%C3%85%C3%90%C3%90%C2%B0%C3%B1'
searchRankingUrl = 'http://opac.bupt.edu.cn:8080/opac_two/top/top_detail.jsp?type=opac.n_search_log&cname=%C2%BC%C3%AC%C3%8B%C3%B7%C3%85%C3%85%C3%90%C3%90%C2%B0%C3%B1'
collectRankingUrl = 'http://opac.bupt.edu.cn:8080/opac_two/top/top_detail.jsp?type=opac.n_collection&cname=%C3%8A%C3%95%C2%B2%C3%98%C3%85%C3%85%C3%90%C3%90%C2%B0%C3%B1'
reviewRankingUrl = 'http://opac.bupt.edu.cn:8080/opac_two/top/top_detail.jsp?type=opac.n_review&cname=%C3%8A%C3%A9%C3%86%C3%80%C3%85%C3%85%C3%90%C3%90%C2%B0%C3%B1'
lookRankingUrl = 'http://opac.bupt.edu.cn:8080/opac_two/top/top_detail.jsp?type=opac.n_look_log&cname=%C2%B2%C3%A9%C2%BF%C2%B4%C3%85%C3%85%C3%90%C3%90%C2%B0%C3%B1'


def get_search_ranking():

    header_search = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Host': 'opac.bupt.edu.cn:8080',
        'Referer': borrowRankingUrl
    }

    starttime = datetime.datetime.now()

    session = requests.Session()
    session.cookies = http.cookiejar.CookieJar()

    # 检索排行榜
    res = session.get(searchRankingUrl, headers=header_search)
    res.encoding = 'gb2312'
    content = res.text
    rankingSoup = BeautifulSoup(content,'html.parser')
    rankDiv = rankingSoup.find('form',{'id':'paihang_detail'})
    r_trs = rankDiv.find_all('tr')
    result = {}
    result['amount'] = len(r_trs)
    keylist = []
    for r_index, r_tr in enumerate(r_trs):
        if r_index == 0:
            continue
        booktds = r_tr.find_all('td')
        search_ranking = booktds[0].text
        search_key = booktds[1].text
        # search_key_url = bookDetailBaseUrl + booktds[1].find('a')['href']
        search_times = booktds[2].text
        single_key = {}
        single_key['key'] = search_key
        # single_key['url'] = search_key_url
        single_key['times'] = search_times
        keylist.append(single_key)

        # print(search_ranking,search_times,search_word,search_word_url)

    result['keylist'] = keylist

    endtime = datetime.datetime.now()
    print(TerminalColors.OKGREEN + '[Success]' + TerminalColors.ENDC + ' [Get Search Ranking] Using: ' + TerminalColors.OKGREEN + str((endtime - starttime).seconds) + TerminalColors.ENDC + ' s')

    return json.dumps(result, ensure_ascii=False)