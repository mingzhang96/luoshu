# -*- coding: utf-8 -*-
# OK 书籍检索

import http.cookiejar
import json
import re
import string
import requests
from urllib.parse import *
from bs4 import BeautifulSoup

header_search = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Host': 'opac.bupt.edu.cn:8080',
    'Referer': 'http://lib.bupt.edu.cn/index.html'
}

bookSearchBaseUrl = 'http://opac.bupt.edu.cn:8080/opac_two/search2/'
baseUrl = 'http://opac.bupt.edu.cn:8080'
search_params = '/opac_two/search2/searchout.jsp?srctop=top2&suchen_match=qx&recordtype=all&suchen_type=1&\
snumber_type=Y&search_no_type=Y&library_id=all&show_type=wenzi&client_id=web_search&suchen_word=%20'


# 搜索结果每本书的信息
def get_every_book_info(books_soup):
    booklist = []
    booksDiv = books_soup.find('div', {'id': 'searchout_tuwen'})
    bookItems = booksDiv.find_all('tr')
    for index, item in enumerate(bookItems):
        if index == 0:
            continue
        tds = item.find_all('td')
        bookNum = tds[0].text.strip()
        bookTitle = tds[1].text.strip()
        bookTempLink = tds[1].a['href']
        bookSid = re.findall('sid=(.*)', bookTempLink)[0]  # 图书馆中书的的编号
        bookAuthors = tds[2].text.strip()
        # bookPublishing = tds[3].text.strip()
        # bookISBN = tds[4].text.strip()
        # bookYear = tds[5].text.strip()
        # bookCallno = tds[6].text.strip()  # 索书号
        bookUsage = tds[7].text.strip()
        tempbookUsage = bookUsage.split()
        # bookCollectionNum = int(tempbookUsage[0].split('：')[1])
        bookAvailable = int(tempbookUsage[1].split('：')[1])

        bookInfo = {}
        bookInfo['book_num'] = bookNum
        bookInfo['book_title'] = bookTitle
        bookInfo['book_sid'] = bookSid
        bookInfo['book_authors'] = bookAuthors
        if bookAvailable > 0:
            bookInfo['book_available'] = '可借'
        else:
            bookInfo['book_available'] = '不可借'
        booklist.append(bookInfo)
    return booklist


def searchbook(keyWord, targetPage):

    resultDict = {}
    booklist = []

    if not keyWord:
        resultDict['amount'] = str(0)
        resultDict['booklist'] = ['none']
        return json.dumps(resultDict, ensure_ascii=False)

    urlKeyWord_utf = str(quote(keyWord, safe=string.printable, encoding='utf8'))

    searchUrl = baseUrl + search_params + keyWord

    # Search
    session = requests.Session()
    session.cookies = http.cookiejar.CookieJar()

    if str(targetPage) == str(0):
        res = session.get(searchUrl, headers=header_search)
        res.encoding = 'gb2312'
        content = res.text

        books_soup = BeautifulSoup(content, 'html.parser')

        # 搜索结果信息
        tempResultInfo = books_soup.find_all('span', {'class':'opac_red'})

        bookCount = 0
        if len(tempResultInfo) < 4:
            resultDict['amount'] = str(0)
            resultDict['booklist'] = ['none']
            return json.dumps(resultDict, ensure_ascii=False)
            # print('none')

        searchResultNum = tempResultInfo[0].text.strip()
        resultDict['amount'] = str(searchResultNum)
        # searchResultInfo = tempResultInfo[1].text.strip()
        # currentPage = tempResultInfo[2].text.strip()
        totalPage = tempResultInfo[3].text.strip()

        resultDict['totalpage'] = totalPage

        booklist = get_every_book_info(books_soup)
        # # 搜索结果详细信息
        # booksDiv = books_soup.find('div', { 'id':'searchout_tuwen'})
        # bookItems = booksDiv.find_all('tr')
        # for index,item in enumerate(bookItems):
        #     if index == 0:
        #         continue
        #     tds = item.find_all('td')
        #     bookCount += 1
        #     bookNum = tds[0].text.strip()
        #     bookTitle = tds[1].text.strip()
        #     bookTempLink = tds[1].a['href']
        #     bookSid = re.findall('sid=(.*)', bookTempLink)[0] # 图书馆中书的的编号
        #     bookAuthors = tds[2].text.strip()
        #     # bookPublishing = tds[3].text.strip()
        #     # bookISBN = tds[4].text.strip()
        #     # bookYear = tds[5].text.strip()
        #     # bookCallno = tds[6].text.strip()  # 索书号
        #     bookUsage = tds[7].text.strip()
        #     tempbookUsage = bookUsage.split()
        #     # bookCollectionNum = int(tempbookUsage[0].split('：')[1])
        #     bookAvailable = int(tempbookUsage[1].split('：')[1])
        #
        #     bookInfo = {}
        #     # bookInfo['bookNum'] = bookNum
        #     bookInfo['bookTitle'] = bookTitle
        #     bookInfo['bookSid'] = bookSid
        #     bookInfo['bookAuthors'] = bookAuthors
        #     if bookAvailable > 0:
        #         bookInfo['bookAvailable'] = '可借'
        #     else:
        #         bookInfo['bookAvailable'] = '不可借'
        #
        #     booklist.append(bookInfo)

        resultDict['booklist'] = booklist
        return json.dumps(resultDict, ensure_ascii=False)

    else:
        # 搜索结果翻页，表单提交数据
        postData = {
            'campus_code': 'all',
            'recordtype': 'all',
            'kind': 'simple',
            'suchen_word': keyWord,
            'suchen_type': '1',
            'suchen_match': 'qx',
            'kind': 'simple',
            'show_type': 'wenzi',
            'snumber_type': 'Y',
            'search_no_type': 'Y',
            'searchtimes': '1',
            'size': '20',
            'curpage': str(targetPage),
            'orderby': 'pubdate_date',
            'ordersc': 'desc',
            'page': str(targetPage),
            'pagesize': '20'
        }

        header_change_page = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
            'Host': 'opac.bupt.edu.cn:8080',
            'Upgrade-Insecure-Requests':'1',
            'Referer': 'http://opac.bupt.edu.cn:8080/opac_two/search2/searchout.jsp?srctop=top2&suchen_match=qx\
            &recordtype=all&suchen_type=1&snumber_type=Y&search_no_type=Y&library_id=all&show_type=wenzi&client_id=web_search&suchen_word=' + urlKeyWord_utf
        }
        res = session.post(searchUrl, headers=header_change_page, data=postData)
        res.encoding = 'gb18030' # gb2312
        content = res.text
        books_soup = BeautifulSoup(content, 'html.parser')

        tempResultInfo = books_soup.find_all('span', {'class': 'opac_red'})

        bookCount = 0
        if len(tempResultInfo) < 4:
            resultDict['amount'] = str(0)
            resultDict['booklist'] = ['none']
            return json.dumps(resultDict, ensure_ascii=False)
            # print('none')

        searchResultNum = tempResultInfo[0].text.strip()
        resultDict['amount'] = str(searchResultNum)
        # searchResultInfo = tempResultInfo[1].text.strip()
        # currentPage = tempResultInfo[2].text.strip()
        totalPage = tempResultInfo[3].text.strip()

        resultDict['totalpage'] = totalPage

        booklist = get_every_book_info(books_soup)
        resultDict['booklist'] = booklist
        return json.dumps(resultDict, ensure_ascii=False)
