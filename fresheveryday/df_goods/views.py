# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import *
from django.core.paginator import Paginator
from haystack.views import SearchView
from django.http import HttpResponse
from fresheveryday.settings import HAYSTACK_SEARCH_RESULTS_PER_PAGE
# from tests import test  仅用于添加测试数据


# 首页
def index(request):
    type_list = TypeInfo.objects.all()
    type0 = type_list[0].goodsinfo_set.order_by('-id')[0:4]
    type01 = type_list[0].goodsinfo_set.order_by('-gclick')[0:4]
    type1 = type_list[1].goodsinfo_set.order_by('-id')[0:4]
    type11 = type_list[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = type_list[2].goodsinfo_set.order_by('-id')[0:4]
    type21 = type_list[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = type_list[3].goodsinfo_set.order_by('-id')[0:4]
    type31 = type_list[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = type_list[4].goodsinfo_set.order_by('-id')[0:4]
    type41 = type_list[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = type_list[5].goodsinfo_set.order_by('-id')[0:4]
    type51 = type_list[5].goodsinfo_set.order_by('-gclick')[0:4]

    context = {'title': '首页', 'index': 1,
               'type0': type0, 'type01': type01,
               'type1': type1, 'type11': type11,
               'type2': type2, 'type21': type21,
               'type3': type3, 'type31': type31,
               'type4': type4, 'type41': type41,
               'type5': type5, 'type51': type51}
    return render(request, 'df_goods/index.html', context)


# 列表页
def g_list(request, tid, pindex, sort):
    typeinfo = TypeInfo.objects.get(pk=int(tid))
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    if sort == '1':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    if sort == '2':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('gprice')
    if sort == '3':
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')
    paginator = Paginator(goods_list, 10)
    page = paginator.page(int(pindex))
    context = {'title': typeinfo.title, 'index': 1,
               'page': page,
               'paginator': paginator,
               'typeinfo': typeinfo,
               'sort': sort,
               'news': news}
    return render(request, 'df_goods/list.html', context)


# 商品详情
def detail(request, gid):
    goods = GoodsInfo.objects.get(pk=int(gid))
    goods.gclick = goods.gclick+1
    goods.save()
    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {'title': goods.gtype.title,
               'index': 1,
               'g': goods,
               'news': news,
               'gid': gid}
    response = render(request, 'df_goods/detail.html', context)

    # # 记录最近浏览，在用户中心使用
    # goods_ids = request.COOKIES.get('goods_ids', '')
    # goods_id = '%d' % goods.id
    # # 判断是否有浏览记录，如果有则继续判断
    # if goods_ids != '':
    #     # 拆分为列表
    #     goods_ids1 = goods_ids.split(',')
    #     # 判断如果商品已经被记录，就删除掉
    #     if goods_ids1.count(goods_id) >= 1:
    #         goods_ids1.remove(goods_id)
    #     # 添加到第一个
    #     goods_ids1.insert(0, goods_id)
    #     # 如果超过5个就删除最后一个
    #     if len(goods_ids1) >= 6:
    #         del goods_ids1[5]
    #     # 拼接为字符串
    #     goods_ids = ','.join(goods_ids1)
    # else:
    #     # 如果没有浏览记录就直接加
    #     goods_ids = goods_id
    # response.set_cookie('goods_ids', goods_ids)

    if request.session.has_key('user_id'):
        goods_ids = request.session.get('goods_ids', '')
        goods_id = int(goods.id)
        if goods_ids != '':
            if goods_ids.count(goods_id) >= 1:
                goods_ids.remove(goods_id)
            goods_ids.insert(0, goods_id)
            if len(goods_ids) >= 6:
                del goods_ids[5]
        else:
            goods_ids = []
            goods_ids.append(goods_id)
        request.session['goods_ids'] = goods_ids
    return response


class MySearchView(SearchView):
    def build_page(self):
        # 分页重写
        context = super(MySearchView, self).extra_context()  # 继承自带的context
        try:
            page_no = int(self.request.GET.get('page', 1))
        except Exception:
            return HttpResponse("Not a valid number for page.")

        if page_no < 1:
            return HttpResponse("Pages should be 1 or greater.")
        a = []
        for i in self.results:
            a.append(i.object)
        paginator = Paginator(a, HAYSTACK_SEARCH_RESULTS_PER_PAGE)
        # print("--------")
        # print(page_no)
        page = paginator.page(page_no)
        return (paginator, page)

    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context['title'] = '搜索'
        context['index'] = 1
        return context