# -*- coding: utf-8 -*-
from django.conf.urls import url
from views import *

import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^list(\d+)_(\d+)_(\d+)/$', views.g_list),
    url(r'^(\d+)/$', views.detail),
    url(r'^search/', MySearchView()),



    # url(r'^test/$', views.test)   仅用于添加测试数据
]

