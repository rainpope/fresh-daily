# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# 添加测试数据需要下载faker包    安装命令： pip install faker
from faker import Factory
from .models import *
import random


def test(request):
    TypeInfo_list = TypeInfo.objects.all()
    fake = Factory.create('zh_CN')   #测试数据生成器   可批量添加数据测试
    for i in range(0, 300):
        j = random.randint(0, 100)
        s1 = random.randint(0, 100)
        s2 = random.randint(0, 100)
        k = random.randint(0, 5)
        jpg_num = str(random.randint(1, 21))
        jpg_path = 'df_goods/goods00'+jpg_num+'.jpg'
        v = GoodsInfo(
            gtitle=fake.text(max_nb_chars=10),
            gpic=jpg_path,
            gprice=j,
            gunit='500g',
            gclick=0,
            isDelete=False,   #是否删除，我全部选择否，如果需要随机是否可以使用fake.pybool()
            gjianjie=fake.text(max_nb_chars=70),
            gkucun=s2,
            gcontent=fake.text(max_nb_chars=300),
            gtype=TypeInfo_list[k],   #所属类型
        )
        v.save()