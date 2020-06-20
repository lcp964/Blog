from django.shortcuts import render,redirect
from django.views import View
from django import http
from xm.utils.fiP.ip import blacks,func
from .import models
# Create your views here.

def login_req(f):

    def func(request):
        if request.user.is_authenticated:
            return f(request)
        else:
            return redirect('/user/login/')
    return func
#在线课堂
@blacks
@func
@login_req
def course(request):
    title='视频页面'
    courses=models.Course.objects.only('cover_url','title','teacher__name').select_related('teacher').filter(is_delete=False)
    return render(request, 'course/course.html',context={'title':title,'course':courses})

class course_detailView(View):
    def get(self,request,c_id):
     title='视频详情页面'
     course=models.Course.objects.only('title','cover_url','video_url','profile','outline','teacher__name','teacher__avatar_url','teacher__positional_title','teacher__profile').select_related('teacher').filter(is_delete=False,id=c_id).first()
     if course:
         return render(request,'course/course_detail.html',context={'title':title,'courses':course})
     else:
         return http.Http404('NOT FOUND PAGE')

courses=course_detailView.as_view()