from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from api.buptlibrary.bookSearch import searchbook
from api.buptlibrary.checkAuth import checkauth
from api.buptlibrary.continueBorrow import continue_borrow
from api.buptlibrary.getBookDetail import get_book_detail
from api.buptlibrary.getBorrowInfo import get_borrow_info
from api.buptlibrary.getBorrowRanking import get_borrow_ranking
from api.buptlibrary.getSearchRanking import get_search_ranking


def index(request):
    return HttpResponse("Welcom 你好！")


# @csrf_exempt
def auth(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    else:
        return HttpResponse("{'Method':'error'}")
    # print(username, password)
    auth_status, session = checkauth(username, password)
    res = ''
    if auth_status:
        res = '{"auth":"true"}'
    else:
        res = '{"auth":"false"}'
    print('[Success] Link to authority:')
    return HttpResponse(res)


def search(request):
    # /api/search?searchword=Python&page=1
    searchword = request.GET['searchword']
    page = request.GET['page']
    # print('[Begin] Search: ' + searchword, '[Page]: ' + page)
    res = searchbook(searchword, page)
    # print('[Success] Search: ' + searchword, '[Page]: ' + page)
    return HttpResponse(res)


# @csrf_exempt
def getborrowinfo(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
    else:
        return HttpResponse("{'Method':'error'}")

    res = get_borrow_info(username, password)
    if res:
        print('[Success] Get borrow information')
        return HttpResponse(res)
    else:
        print('[Fail] Auth error')
        return HttpResponse('{"auth":"false"}')


# @csrf_exempt
def continueborrow(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        book_number = int(request.POST['number']) - 1
        # print(username, password, book_number)
        if book_number < 0:
            return HttpResponse("{'book_number':'error'}")
    else:
        return HttpResponse("{'Method':'error'}")
    auth_status, session = checkauth(username, password)
    if not auth_status:
        return HttpResponse('{"auth":"false"}')
    else:
        # print('book_number:' + str(book_number))
        borrow_status = continue_borrow(book_number, session)
        if borrow_status:
            return HttpResponse('{"xujie":"true"}')
        else:
            return HttpResponse('{"xujie":"false"}')


def getbookdetial(request):
    sid = request.GET['sid']
    res = get_book_detail(sid)
    # print('[Success] Look the detail infomation of sid:' + sid)
    return HttpResponse(res)


def getborrowranking(request):
    res = get_borrow_ranking()
    return HttpResponse(res)


def getsearchranking(request):
    res = get_search_ranking()
    return HttpResponse(res)