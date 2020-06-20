from django.shortcuts import render
from xm.settings.ds import IP_FUNL
from django import http
import time


def func(fun):
    def mzitu(request):
        now_time=time.time()
        ip=request.META.get('REMOTE_ADDR')
        if ip not in IP_FUNL:
            IP_FUNL[ip]=[now_time]
        history=IP_FUNL.get(ip)
        while history and now_time - history[-1] > 1:
            history.pop()
        if(len(history))<3:
             history.insert(0,now_time)
             return fun(request)
        else:
            request.session['blockname'] = ip
            request.session.set_expiry(300)
            return http.HttpResponseForbidden()
    return mzitu
def blacks(fff):
    def wirtes(request):
        ip=request.META.get('REMOTE_ADDR')
        block=request.session.get('blockname')
        if ip == block:
            return render(request,'admin/news/ip.html')
        else:
            return fff(request)
    return wirtes
