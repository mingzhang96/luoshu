# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^auth', views.auth, name='auth'), # ok
    url(r'^search', views.search, name='search'),   # ok
    url(r'^getborrowinfo', views.getborrowinfo, name='borrow'), # ok
    url(r'^getbookdetial', views.getbookdetial, name='getbookdetial'),  #
    url(r'^getborrowranking', views.getborrowranking, name='getborrowranking'), #
    url(r'^getsearchranking', views.getsearchranking, name='getsearchranking'), #
    url(r'^continueborrow', views.continueborrow, name='continueborrow'),   #
    url(r'^', views.index, name='index'),   # ok
]
