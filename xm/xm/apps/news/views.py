import view as view
from django.db.models import F
from django.shortcuts import render,redirect
import logging
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage#分页包
from django.test import tag
from xm.utils.res_code import res_json,Code
logger=logging.getLogger('django')
from .models import News
from django.views import View
from . import models
from django.http import HttpResponseNotFound
import json
from news.models import Comment
import pytz
import datetime
from django.contrib.auth.decorators import login_required #一键登录才能访问新闻页面
from xm.utils.fiP.ip import blacks,func
def login_req(f):

    def func(request):
        if request.user.is_authenticated:
            return f(request)
        else:
            return redirect('/user/login/')
    return func



    #新闻首页面
# @login_required(login_url='/user/login/') #用auth系统实现访问页面必须登录才可以访问
@blacks
@func
@login_req
def index(request):
      tag = models.Tag.objects.only('name').filter(is_delete=False)
      news_click=News.objects.only('title','image_url','update_time','author__username','tag__name').select_related('tag','author').order_by('clicks')[0:2] #展示两条
     #展示热门新闻
      hot = models.HotNews.objects.only('news__title','news__image_url').select_related('news').order_by(
          'priority').filter(is_delete=False)[0:3]
      return render(request,'news/index.html',context={'tags':tag,'click':news_click,'hot':hot})
# hot = models.HotNews.objects.select_related('news').only('news__title', 'news__image_url').order_by('priority').filter(is_delete=False)[0:3]


#新闻列表

class NewsView(View):
   def get(self,request):
             #验证数据
             try:
                 tag=int(request.GET.get('tag_id',0))  #分类
             except Exception as e:
                   logger.error('页面分类错误'.format(e))
                   tag=0 #默认页面分类为零
             try:
               page=int(request.GET.get('page'))
             except Exception as e:
                   logger.error('页码错误'.format(e))
                   page=1 #默认页码为1
            #数据库里面拿数据 annotate 方法在底层调用了数据库的数据聚合函数
             # news_list=News.objects.values('title','digest','image_url','update_time','id').annotate(tag_name=F('tag__name'),author=F('author__username'))
             news_list=News.objects.select_related('tag','author').only('title','digest','image_url','update_time','author__username','tag__name').filter(is_delete=False)
             news_info=news_list.filter(is_delete=False,tag_id=tag) or news_list.filter(is_delete=False)
             #分页
             pages=Paginator(news_info,5) #展示第五页
             try:
               news= pages.page(page)  #拿到当前返回页
             except Exception as e:
                  logger.error(e)
                  news=pages.page(pages.num_pages)  #获取页面总数
             news_list_info=[]
             for i in news:
                  news_list_info.append(
                      i.to_put(),

                  )

             data={
               'news':news_list_info,
               'total_pages':pages.num_pages,
             }
             return res_json(data=data)
news=NewsView.as_view()

#详情页

class Newsdetail(View):
    def get(self,request,news_id):
        title='详情页面'
        #点击页面
        news_click = News.objects.only('title', 'image_url', 'author__username', 'tag__name',
                                              'update_time').select_related('tag', 'author').order_by('clicks')[0:2]
        news=News.objects.select_related('author','tag').only('title','update_time','content','author__username','tag__name').filter(is_delete=False,id=news_id).first()
        models.News.increase_clicks(news)
        a = news.clicks
        #评论        你这里筛选了二级评论，唉！  #关联的作者查询有问题
        comm=models.Comment.objects.select_related('author').only('author__username','update_time','parent__update_time').filter(is_delete=False,news_id=news_id)

        #那条文章评论那条
        #数据清洗
        # 热门推荐
        # 根据点击量排名

        # print(a)
        # news.clicks += 1
        # news.save(update_fields=['clicks'])  # 保存更新字段
        comm_info = []
        for i in comm:
         comm_info.append(i.to_dict())
        if news:
            return render(request, 'news/news_detail.html',
                          context={'news': news, 'title': title, 'click': news_click, 'commss': comm_info})
        else:
               return HttpResponseNotFound('PAGE NOT Found')
detail=Newsdetail.as_view()

#轮播图

class BannerView(View):
    def get(self,request):
        banner= models.Banner.objects.select_related('news').only('image_url', 'news__title').filter(is_delete=False).order_by('priority')
        b_info = []
        for i in banner:
            b_info.append({
                'image_url': i.image_url,
                'news_title': i.news.title,
                'news_id': i.news.id
            })
            data={
                'banner':b_info
            }
        return res_json(data=data)

banner=BannerView.as_view()




#百度云上传图片在web展示

def demo(request):
    title='百度图片展示页面'
    return render(request,'demo.html',context={'title':title})

d=demo


#评论
class Newscommit(View):
    def post(self,request,news_id):
        res_error= res_json(errno=Code.PARAMERR,errmsg='参数错误')
        if not request.user.is_authenticated:  #判断用户未登录
            return res_json(Code.SESSIONERR,errmsg='用户未登录')
        #判断用户是否存在
        if not models.News.objects.filter(is_delete=False,id=news_id).exists():
            return res_error

        #获取参数
        js_data=request.body
        if not js_data:
            return res_error
        dict_data= json.loads(js_data)

       #一级评论
        content = dict_data.get('content')
        if not dict_data['content']:
            return res_error

         #回复评论
        parent_id = dict_data.get('parent_id')

        if parent_id:
            if not models.Comment.objects.filter(is_delete=False,id=parent_id,news_id=news_id).exists():
             return res_error

        # 保存数据库

        news = models.Comment()
        news.content = content
        news.news_id = news_id
        news.author = request.user
        news.parent_id = parent_id if parent_id else None
        news.save()
        return res_json(data=news.to_dict())


comment=Newscommit.as_view()


#搜索
# def search(request):
#     return render(request, 'news/search.html')
from django.http import HttpResponseRedirect
from haystack.views import SearchView
class Search(SearchView):
        template = 'news/search.html'
        def create_response(self):  # 创建响应
            query = self.request.GET.get('q', '')  # q方式查询 在查询框里面的name 没有查到展示热门新闻
            if not query:
                show = True
                hots_news = models.HotNews.objects.select_related('news').only('news_id', 'news__title',
                                                                               'news__image_url').filter(
                    is_delete=False).order_by('priority')
                pages = Paginator(hots_news, 5)  # 展示五条热门新闻
                try:
                    page = pages.page(int(self.request.GET.get('page', 1)))  # # 假如传的不是整数
                except PageNotAnInteger:
                    page = pages.page(int(1))  # 如果不是整数返回第一页
                except EmptyPage:
                    page = pages.page(pages.num_pages)  # 拿取总页数
                    return render(self.request, self.template, locals())  # local局部变量全部返回
            else:
                show = False
            return super().create_response()






# #在线课堂
# def course(request):
#     title='视频页面'
#     return render(request, 'course/video_test.html',context={'title':title})


