# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import *
from df_user import user_decorator


# Create your views here.
# 呈现购物车的页面
@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    if request.is_ajax():
        count = carts.count()
        return JsonResponse({'count': count})
    context = {
        'title': '购物车',
        'user_info': 1,
        'carts': carts
    }
    return render(request, 'df_cart/cart.html', context)


# 当用户添加商品到购物车
@user_decorator.login
def add(request, gid, count):
    # 用来返回购物车页面的商品的总数
    if int(gid) == 0 and request.is_ajax() and int(count) == 0:
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        return JsonResponse({'count': count})
    # 获得用户的ID，商品的ID和添加的数量
    uid = request.session['user_id']
    gid = int(gid)
    count = int(count)
    # 获取这个用户的这件商品的购物车信息
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)
    # 如果购物车表里有这件商品的记录那么数量就加1
    if len(carts) >= 1:
        cart = carts[0]
        cart.count += count
    # 如果购物车表里没有这件商品那么就添加一条记录
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    # 不管上面两个的情况如果都保存信息
    cart.save()
    # 如果请求是ajax就返回商品的的数量，用户商品详情页面
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        return JsonResponse({'count': count})
    else:
        return redirect('/cart/')


def edit(request, cart_id, count):
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.count = count
        cart.save()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': int(count)}
    return JsonResponse(data)


def delete(request, cart_id):
    try:
        cart = CartInfo.objects.get(pk=cart_id)
        cart.delete()
        data = {'ok': 1}
    except Exception as e:
        data = {'ok': 0, 'e': e}
    return JsonResponse(data)

