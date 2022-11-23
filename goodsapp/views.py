import collections

from django.shortcuts import render

# Create your views here.
from django.views import View
from django.core.paginator import Paginator
from goodsapp.models import Category, Goods
import math

class IndexView(View):
    def get(self,request,cid=2,num=1):
        cid = int(cid)
        num = int(num)
        # 查询所有类别信息
        CategoryList = Category.objects.all()
        # 查询当前类别下的所有商品信息
        goodsList = Goods.objects.filter(category_id=cid).order_by('id')

        # 创建分页器对象
        paginator_obj = Paginator(goodsList,8)

        #获取某夜数据对象
        page_obj = paginator_obj.page(num)

        #获取每一页显示的页码范围
        begin = num - int(math.ceil(10.0/2))
        if begin < 1:
            begin = 1

        end = begin + 9
        if end > paginator_obj.num_pages:
            end = paginator_obj.num_pages
        if end < 10:
            begin =1
        else:
            begin = end - 9
        page_list = range(begin,end+1)


        return render(request,'index.html',{'categoryList':CategoryList,'cid':cid,'goodslist':page_obj,'page_list':page_list,'num':num})

class DetailView(View):
    def get(self,request,goodsid):
        goodsid = int(goodsid)

        # 根据商品id查询商品详情
        goods = Goods.objects.get(id=goodsid)

        return render(request,'detail.html',{'goods':goods})