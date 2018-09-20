# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from df_user import user_decorator
from df_cart.models import CartInfo
from df_user.models import UserInfo
from df_goods.models import GoodsInfo
from .models import *
from django.http import JsonResponse
from django.db import transaction
from datetime import datetime
from decimal import Decimal
# Create your views here.


# 订单
@user_decorator.login
def order(request):
    user_id = request.session['user_id']
    user = UserInfo.objects.get(pk=user_id)

    cart_ids = request.GET.getlist('cart_id')
    carts = []
    for c in cart_ids:
        carts.append(CartInfo.objects.get(pk=c.encode('utf-8')))
    context = {'user_info': 1,
               'title': '提交订单',
               'carts': carts,
               'user': user}
    return render(request, 'df_order/place_order.html', context)


# 创建订单
@transaction.atomic()
@user_decorator.login
def order_handle(request):
    # 保存事物点
    tran_id = transaction.savepoint()

    try:
        post = request.POST
        cart_list = post.getlist('cid[]')
        print('-' *40)
        print(cart_list)
        total = post.get('total')
        address = post.get('address')

        # 创建订单
        order = OrderInfo()
        now = datetime.now()
        uid = request.session.get('user_id')
        order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid
        order.odata = now
        order.ototal = Decimal(total)
        order.oaddress = address
        order.save()

        # 创建详表
        for cart_id in cart_list:
            cart_one = CartInfo.objects.get(pk=cart_id)
            goods_one = GoodsInfo.objects.get(pk=cart_one.goods_id)
            # 判断商品的库存是否足够
            if int(goods_one.gkucun) >= int(cart_one.count):
                # 足够就减少商品表的库存
                goods_one.gkucun -= int(cart_one.count)
                goods_one.save()

                # 创建订单详情表
                detail_info = OrderDetailInfo()
                detail_info.goods_id = int(goods_one.id)
                detail_info.order_id = int(order.oid)
                detail_info.price = Decimal(int(goods_one.gprice))
                detail_info.count = int(cart_one.count)
                detail_info.save()

                cart_one.delete()
            else:
                # 库存不够事件回滚
                transaction.savepoint_rollback(tran_id)
                return JsonResponse({'status': 2})
    except Exception as e:
        # 异常提示
        print '==================%s' % e
        transaction.savepoint_rollback(tran_id)
    # 返回一个数据到前端
    return JsonResponse({'status': 1})
