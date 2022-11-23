from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
# Create your views here.
from cartapp.cartmanager import SessionCartManager
from userapp.models import UserInfo, Area, Address
import jsonpickle


class RegisterView(View):
    def get(self,request):

        return render(request,'register.html')


    def post(self,request):
        # 获取请求参数
        account = request.POST.get('account');
        pwd = request.POST.get('password');

        #将数据添加到数据库
        user = UserInfo.objects.create(uname=account,pwd=pwd)

        #判断是否注册成功
        if user:
            #将当前注册用户对象保存到session中
            request.session['user'] = jsonpickle.dumps(user)
            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/register/')


class CenterView(View):
    def get(self,request):
        return render(request,'center.html')

class LoginView(View):
    def get(self,request):

        return render(request,'login.html',{'redirect':request.GET.get('redirct',''),'cartitems':request.GET.get('cartitems','')})

    def post(self,request):
        # 获取请求参数
        uname = request.POST.get('account','')
        pwd = request.POST.get('password','')
        redirect = request.POST.get('redirect','')
        #数据库中查询当前用户是否存在
        userList = UserInfo.objects.filter(uname=uname,pwd=pwd)

        #判断是否登录成功
        if userList:
            request.session['user'] = jsonpickle.dumps(userList[0])

            if redirect == 'cart':
                # 将session中的购物项转移到数据库表中
                SessionCartManager(request.session).migrateSession2DB()
                return HttpResponseRedirect('/cart/queryAll/')
            elif redirect == 'order':
                SessionCartManager(request.session).migrateSession2DB()
                return HttpResponseRedirect('/order/toOrder/?cartitems'+request.POST.get('cartitems',''))
            return HttpResponseRedirect('/user/center/')
        return HttpResponseRedirect('/user/login/')

from utils.code import *
class LoadCodeView(View):
    def get(self,request):
        #调用工具包下的函数生成验证码
        img,txt = gene_code()

        #将txt保存到session
        request.session['sessionCode'] = txt

        #响应页面
        return HttpResponse(img,content_type='image/png')


class CheckCodeView(View):
    def get(self,request):
        # 获取请求参数
        code = request.GET.get('code','')
        #获取系统生成的验证码
        sessioncode = request.session.get('sessionCode')

        flag = code == sessioncode

        return JsonResponse({'flag':flag})


class Logout(View):
    def get(self,request):
        #清空session对象中的所有数据
        request.session.clear()

        return JsonResponse({'flag':True})


class AddressView(View):
    def get(self,request):
        user = jsonpickle.loads(request.session.get('user'))
        addrList = user.address_set.all()
        return render(request,'address.html',{'addrList':addrList})
    def post(self,request):
        # 获取请求参数
        params = request.POST.dict()

        params.pop('csrfmiddlewaretoken')
        # 获取当前登录用户对象
        user = jsonpickle.loads(request.session.get('user'))

        Address.objects.create(userinfo=user,
                               isdefault=(lambda count: True if count == 0 else False)(user.address_set.count()),
                               **params)

        return HttpResponseRedirect('/user/address/')


from django.core.serializers import serialize
def loadAddr(request):
    #获取请求参数
    pid = request.GET.get('pid',-1)
    pid = int(pid)


    #根据父Id查询区划信息
    areaList = Area.objects.filter(parentid=pid)

    #序列化arealist
    jareaList = serialize('json',areaList)
    return JsonResponse({'jareaList':jareaList})