# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from models import *
from hashlib import sha1
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from df_goods.models import GoodsInfo
import user_decorator


# 用户注册页面的呈现
def register(request):
    # 显示title的文字
    context = {'title': '用户注册'}
    return render(request, 'df_user/register.html', context)


# 处理用户注册
def register_handle(request):
    # 获取用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码是否相等
    if upwd != ucpwd:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd)
    s1_upwd = s1.hexdigest()
    # 把用户输入的用户名、密码、邮箱保存到数据库
    user = UserInfo()
    user.uname = uname
    user.upwd = s1_upwd
    user.uemail = uemail
    user.save()
    return redirect('/user/login/')


# 判断用户输入的用户名是否存在
def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


# 呈现登陆页面
def login(request):
    # 如果用户有cookies信息就接受cookies
    uname = request.COOKIES.get('uname', '')
    # 创建上下文,给判断用户名和密码的js一个默认值不让他报错,有cookies就呈现出来
    context = {'title': '用户登录','error_name': 0, 'error_pwd':0, 'uname': uname}
    return render(request, 'df_user/login.html', context)


# 处理用户登陆
def login_handle(request):
    # 接受用户的输入信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)

    # 查询数据库取得这个用户的信息,如果没有就为一个[]
    users = UserInfo.objects.filter(uname=uname)

    # 判断时候存在这个用户名
    if len(users) == 1:
        # 把密码sha1加密,用于和数据库判断
        s1 = sha1()
        s1.update(upwd)
        # 判断用户输入的密码和数据库是否一致
        if s1.hexdigest() == users[0].upwd:
            # 构建重定向信息
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)

            # 判断用户是否勾选了记住用户名
            if jizhu != 0:
                # 用户记住用户名的话就设置一条cookies,保存用户名
                red.set_cookie('uname', uname)
            else:
                # 如果用户不记住用户名就设置把uname设置为'',设置为立即清除cookies
                red.set_cookie('uname', '', max_age=-1)

            # 在服务器保存用户信息
            request.session['user_id'] = users[0].id
            request.session['user_name'] = users[0].uname
            return red
        else:
            # 如果密码和数据库不一致就设置error_pwd为1给JS判断,
            # 并把名字和密码发回去,让文本框不清空
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1,
                       'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        # 如果密码和数据库不一致就设置error_name为1给JS判断,
        # 并把名字和密码发回去,让文本框不清空
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0,
                   'uname': uname, 'upwd': upwd}
        return render(request, 'df_user/login.html', context)


# 处理用户退出
@user_decorator.login
def logout(request):
    request.session.flush()
    # del request.session['user_id']
    # del request.session['user_name']
    return redirect('/')


# 用户中心
@user_decorator.login
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    user_name = request.session['user_name']
    # goods_ids = request.COOKIES.get('goods_ids', '')
    # goods_ids1 = goods_ids.split(',')
    goods_ids1 = request.session.get('goods_ids', '')
    goods_list = []
    if goods_ids1 != '':
        for goods_id in goods_ids1:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    context = {'user_name': user_name,
               'user_info': 1,
               'title': '用户中心',
               'user_email': user_email,
               'goods_list': goods_list}

    return render(request, 'df_user/user_center_info.html', context)


# 订单
@user_decorator.login
def order(request):
    context = {'title': '用户中心', 'user_info': 1}
    return render(request, 'df_user/user_center_order.html' , context)


# 收货地址
@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'user': user, 'user_info': 1, 'title': '用户中心'}
    return render(request, 'df_user/user_center_site.html', context)

