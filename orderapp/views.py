import jsonpickle
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from cartapp.cartmanager import getCartManger


def order_view(request):
    #获取请求参数
    cartitems = request.GET.get('cartitems','')
    #获取当前用户登录信息
    user = request.session.get('user','')
    #判断用户是否登录
    if not user:
        return HttpResponseRedirect('/user/login/?redirct=order&cartitems='+cartitems)

    return HttpResponseRedirect('/order/toOrder/?cartitems='+cartitems)


def toOrder(request):
    #接受请求参数
    cartitems = request.GET.get('cartitems','')
    #将cartitems进行反序列化
    cartitemsList = jsonpickle.loads(cartitems)
    cartItemObjList = [getCartManger(request).get_cartitems(**ci) for ci in cartitemsList if ci]

    # 获取用户的默认收件地址
    user = jsonpickle.loads(request.session.get('user'))
    addr = user.address_set.get(isdefault=True)
    # 支付总金额
    totalPrice = 0
    for cio in cartItemObjList:
        totalPrice += cio.getTotalPrice()

    return render(request,'order.html',{'cartitemList':cartItemObjList,'addr':addr,'totalPrice':totalPrice})
