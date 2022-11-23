#coding=utf-8
#数据表的插入
from goodsapp.models import *
from django.db.transaction import atomic  #事务

@atomic
def test_model():
    with open('utils/jiukuaijiu.json') as fr:
        import json
        datas = json.loads(fr.read())#将读取的文件反序列化
        for data in datas: # 遍历列表


            cate = Category.objects.create(cname=data['category'])#插入类别表

            _goods = data['goods'] #插入商品表

            for goods in _goods:
                good = Goods.objects.create(gname=goods['goodsname'], gdesc=goods['goods_desc'],
                                            price=goods['goods_price'], oldprice=goods['goods_oldprice'],
                                            category=cate)
                sizes = []
                for _size in goods['sizes']:
                    if Size.objects.filter(sname=_size[0]).count() == 1:
                        size = Size.objects.get(sname=_size[0])
                    else:
                        size = Size.objects.create(sname=_size[0])
                    sizes.append(size)

                colors = []
                for _color in goods['colors']:
                    color = Color.objects.create(colorname=_color[0], colorurl=_color[1])
                    colors.append(color)

                for _spec in goods['specs']:
                    goodsdetails = GoodsDetailName.objects.create(gdname=_spec[0])
                    for img in _spec[1]:
                        GoodsDetail.objects.create(goods=good,goodsdname=goodsdetails,gdurl=img)

                for c in colors:
                    for s in sizes:
                        Inventory.objects.create(count=100,goods=good, color=c, size=s)




def deleteall():
    Category.objects.filter().delete()
    Color.objects.filter().delete()
    Size.objects.filter().delete()

