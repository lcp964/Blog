from collections import OrderedDict
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Count
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.models import Group,Permission

from admin.forms import NewsPubForm, DocsPubForm, CoursesPubForm
from docs.models import Doc
from news.models import Banner,Tag,News,HotNews,Comment
from courses.models import Teacher,CourseCategory,Course
from xm.utils.res_code import Code,res_json,error_map
import json
from xm.utils.fiP.ip import blacks,func
from datetime import datetime
import logging
logger=logging.getLogger('django')
from.paginator import get_page_data
from urllib.parse import urlencode
from users.models import Users
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.decorators import method_decorator
from xm.settings import prod
# Create your views here.
parms_statues=res_json(errno=Code.PARAMERR,errmsg='参数错误')


# @blacks
# @func
#权限1
class LoginRequiredMixin(object):
        @method_decorator(login_required(login_url='/user/login/'))
        def dispatch(self,request, *args, **kwargs):
            return super(LoginRequiredMixin,self).dispatch(request, *args, **kwargs)

class admin(LoginRequiredMixin,View): #继承一定要在前面
    def get(self,request):
       return render(request,'admin/news/index.html')

#文章分类
@method_decorator(permission_required(('add_tag','change_tag','delete_tag','delete_tag'),login_url='/admin/',raise_exception=False),name='dispatch')
class TagManage(View):
    def get(self,request):
        tags = Tag.objects.values('id','name').annotate(num_news=Count('news')).filter(is_delete=False).order_by('num_news')
        return render(request,'admin/news/tag_Manger.html',context={'tag':tags})
    #添加标签
    def post(self,request):
        js_str=request.body
        if not js_str:
            return parms_statues
        tag_data=json.loads(js_str)
        name=tag_data.get('name')
        if name:
           name=name.strip()#去掉两个之间空白
            #入库,get_or_create就是一个判断有给你新对
           tag=Tag.objects.get_or_create(name=name)
           return (res_json(errno=Code.OK )if tag[-1] else res_json(errno=Code.DATAEXIST,errmsg='分类名已存在')) #三目云算符

           # if tag[-1]:
           #     return res_json(errno=Code.OK)
           # else:
           #     return res_json(errno=Code.DATAEXIST,errmsg='分类名已存在')
        else:
            return res_json(errno=Code.NODATA,errmsg=error_map[Code.NODATA])

     # 修改标签
    def put(self,request,tag_id):
        js_str=request.body
        if not js_str:
            return parms_statues
        dict_data=json.loads(js_str.decode('utf8'))
        tag_name=dict_data.get('name')
        #查数据
        tag=Tag.objects.only('id').filter(id=tag_id).first()
        if tag:
            if tag_name and tag_name.strip(): #消除数据空格问题
               if not Tag.objects.only('id').filter(name=tag_name).exists():
                   tag.name=tag_name
                   tag.save()
                   return res_json(errno=Code.OK)
               else:
                  return res_json(errno=Code.DATAEXIST,errmsg='分类名已重复')
            else:
                return parms_statues
        else:
         return parms_statues

     #删除分类
    def delete(self,request,tag_id):
        tag=Tag.objects.only('id').filter(id=tag_id).first()
        if tag:
            tag.delete()
            return res_json(errmsg='删除标签更新成功')
        else:
            return res_json(errno=Code.PARAMERR,errmsg='需要删除的标签不存在')

tags=TagManage.as_view()

#热门文章
class HotManager(PermissionRequiredMixin,View):
    permission_required=(('add_hotnews','change_hotnews'))
    raise_exception = True
    def handle_no_permission(self):
        if self.request.method.lower() != 'get':
            return res_json(errno=Code.PARAMERR,errmsg='没有权限')
        else:
            return super().handle_no_permission()

    def get(self,request):
         hotnews=HotNews.objects.only('news_id','news__title','news__tag__name','priority').filter(is_delete=False).order_by('-priority','-news__clicks')[0:3]
         return render(request,'admin/news/hotManager.html',context={'hot_news':hotnews})

hot=HotManager.as_view()
#热门文章
class Hotnewsedit(View):
    # 编辑部分
    def put(self, request, hotnews_id):
        js_str = request.body
        if not js_str:
            return parms_statues
        dict_data=json.loads(js_str.decode('utf8'))
        try:
            priority=int(dict_data.get('priority'))
            priority_list = [i for i, _ in HotNews.P_CHOICES]
        except Exception as e:
            logger.info('热门文章优先级异常：\n{}'.format(e))
            return res_json(errno=Code.PARAMERR, errmsg='热门文章的优先级设置错误')
        hotnews = HotNews.objects.only('id').filter(id=hotnews_id).first()
        if not hotnews:
                return res_json(errno=Code.PARAMERR, errmsg="需要更新的热门文章不存在")

        if hotnews.priority == priority:
            return res_json(errno=Code.PARAMERR, errmsg="热门文章的优先级未改变")
        if hotnews.priority == [1, 2, 3]:
            return res_json(errno=Code.PARAMERR,errmsg="热门文章的优先级只能为1,2,3")

        hotnews.priority = priority
        hotnews.save(update_fields=['priority'])
        return res_json(errmsg="热门文章更新成功")

    #删除部分
    def delete(self,request,hotnews_id):
        hot=HotNews.objects.only('id').filter(id=hotnews_id).first()
        if hot:
            hot.is_delete=True
            hot.save(update_fields=['is_delete'])
            return res_json(errmsg='热门文章删除成功')
        else:
            return res_json(errno=Code.PARAMERR, errmsg="需要删除的热门文章不存在")

#热门文章添加部分
class HotnewsAdd(View):
    #查页面
    def get(self,request):
        tags=Tag.objects.values('id','name').annotate(num_new=Count('news')).filter(is_delete=False).order_by('-num_new')
        priority_dict=OrderedDict(HotNews.P_CHOICES) #优先级在转字典
        return render(request,'admin/news/News_hot_add.html',context={'tags':tags,'priority_dict':priority_dict})
   #添加部分
    def post(self,request):
        json_data = request.body
        if not json_data:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        # 将json转化为dict
        dict_data = json.loads(json_data.decode('utf8'))

        try:
            news_id = int(dict_data.get('news_id'))
        except Exception as e:
            logger.info('前端传过来的文章id参数异常：\n{}'.format(e))
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')

        if not News.objects.filter(id=news_id).exists():
            return res_json(errno=Code.PARAMERR, errmsg='文章不存在')

        try:
            priority = int(dict_data.get('priority'))
            priority_list = [i for i, _ in HotNews.P_CHOICES]
            print(priority_list)
            if priority not in priority_list:
                return res_json(errno=Code.PARAMERR, errmsg='热门文章的优先级设置错误')
        except Exception as e:
            logger.info('热门文章优先级异常：\n{}'.format(e))
            return res_json(errno=Code.PARAMERR, errmsg='热门文章的优先级设置错误')

        # 创建热门新闻
        hotnews_tuple = HotNews.objects.get_or_create(news_id=news_id,priority=priority)
        hotnews, is_created = hotnews_tuple
        hotnews.priority = priority  # 修改优先级
        hotnews.save(update_fields=['priority'])
        return res_json(errmsg="热门文章创建成功")

#关联热门文章标题
class NewsTagView(View):
    def get(self,request,t_id):
        new=News.objects.values('id','title').filter(is_delete=False,tag_id=t_id)
        new_list=[i for i in new]
        return res_json(data={'news':new_list})


#文章管理
class NewsManage(View):
    def get(self,request):
        """
        title  作者   分类名字  更新时间

        :param request:
        :return:
        """
        #时间转化
        start_time=request.GET.get('start_time','')
        start_time = datetime.strptime(start_time, '%Y/%m/%d') if start_time else ''
        end_time=request.GET.get('end_time','')
        end_time = datetime.strptime(end_time, '%Y/%m/%d') if start_time else ''
        # 查询作者，标题，分类
        newss = News.objects.only('title', 'author__username', 'tag__name', 'update_time').filter(
            is_delete=False)
        # 时间验证
        if start_time and not end_time:
            newss=newss.filter(update_time__gte=start_time) #写了开始时间没有写结束时间，通过过滤器过滤时间
        if end_time and not start_time:
            newss=newss.filter(update_time__lte=end_time)
        if end_time and start_time:
            newss=newss.filter(update_time__range=(start_time,end_time)) #两个区间都写了展现区间

         #处理标题
        title=request.GET.get('title','')
        if title:
            newss=newss.filter(title__contains=title)#模糊查询
        # 处理作者
        author_name=request.GET.get('author__name','')
        if author_name:
            newss=newss.filter(author__username__icontains=author_name)
        #处理分类
        tags=Tag.objects.only('name').filter(is_delete=False)
        tag_id=request.GET.get('tag_id',0)
        newss=newss.filter(is_delete=False,tag_id=tag_id)or newss.filter(is_delete=False)

        #处理时间
        #处理分页
        page=request.GET.get('page',1) #默认第一页
        pt=Paginator(newss,6)#定义对象,展示6个
        try:
         news_info=pt.page(page)#传的对象返回对象
        except EmptyPage:
            logger.info('页码错误')
            news_info=pt.page(pt.num_pages)#获取最大数

        #页面分类处理
        page_data=get_page_data(pt,news_info)

        start_time=start_time.strftime('%Y/%m/%d')if start_time else ''
        end_time = end_time.strftime('%Y/%m/%d') if end_time else ''
        data={
            'news_info':news_info,
            'tags':tags,
            'paginator':pt,
            'start_time':start_time,
            'end_time':end_time,
            'title':title,
            'author_name':author_name,
            'tag_id':tag_id,
            'other_param':urlencode({
            'start_time': start_time,
            'end_time': end_time,
            'title': title,
            'author_name': author_name,
            })

        }
        data.update(page_data)

        return render(request,'admin/news/news_manage.html',context=data)



#文章编辑
class NewsEdit(View):
    def get(self, request, news_id):
        news=News.objects.filter(id=news_id,is_delete=False).first()
        if news:
             tags=Tag.objects.only('name').filter(is_delete=False)
             data={
                 'news':news,
                 'tags':tags,
             }

        return render(request,'admin/news/News_edit.html',context=data)


    # 文章更新
    def put(self, request, news_id):
        news = News.objects.filter(id=news_id, is_delete=False).first()
        if not news:
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')
        js_str = request.body
        if not js_str:
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')
        dict_data = json.loads(js_str)
        # 清洗数据
        form = NewsPubForm(data=dict_data)

        if form.is_valid():  # True False
            news.title = form.cleaned_data.get('title')
            news.digest = form.cleaned_data.get('digest')
            news.tag = form.cleaned_data.get('tag')
            news.image_url = form.cleaned_data.get('image_url')
            news.content = form.cleaned_data.get('content')
            news.save()
            return res_json(errmsg='文章更新成功')
        else:
            err_m_l = []
            for i in form.errors.values():
                err_m_l.append(i[0])
            err_msg_str = '/'.join(err_m_l)
            return res_json(errno=Code.PARAMERR, errmsg=err_msg_str)

        # 文章管理删除
    def delete(self, request, news_id):
            news = News.objects.only('id').filter(id=news_id).first()
            if news:
                news.delete()
                return res_json(errmsg='删除文章更新成功')
            else:
                return res_json(errno=Code.PARAMERR, errmsg='需要删除的文章不存在')

edit=NewsEdit.as_view()

#上传图片
from xm.settings import ds
from xm.utils.fastdfs.fdfs import FDFS_Client
class News_to_up(View):
    """
    图片地址images_file  文档地址text_files
    """
    def post(self,request):
        name=request.FILES
        images=name.get('images_file') if name.get('images_file') else name.get('text_file')
        if not images:
            return parms_statues
        if name.get('images_file'):
            if images.content_type not in('image/jpeg','image/gif','image/png','image/jpg','image/bmp'):
                return res_json(errno=Code.PARAMERR,errmsg='不要传非图片文件')

            if images.content_type not in('application/zip','application/zip','application/doc','application/pdf','application/plain','application/m3u8','application/mp4','image/jpeg','image/gif','image/png','image/jpg','image/bmp'):
                return res_json(errno=Code.PARAMERR,errmsg='不要传非文档文件')

        #上传图片到dfs
        ext_name = images.name.split('.')[-1]
        try:
            upload_img = FDFS_Client.upload_by_buffer(images.read(),file_ext_name=ext_name)  # 上传二进制文件
            # print(upload_img)
        except Exception as e:
            # logger.error('图片上传失败{}'.format(e))
           return res_json(errno=Code.UNKOWNERR,errmsg='文件上传失败{}'.format(e))
        #结合响应
        else:
            if upload_img.get('Status') !='Upload successed.':
                return res_json(errno=Code.UNKOWNERR,errmsg='文件上传失败')
            else:
                img_id= upload_img.get('Remote file_id')
                img_url=prod.FDFS_URL+img_id #拼接地址
                print(img_url)
                if name.get('images_file'):
                    return res_json(data={'image_url': img_url}, errmsg='图片上传成功')
                else:
                     return res_json(data={'text_url': img_url}, errmsg='文件上传成功')

up_to=News_to_up.as_view()
from django import http

#mardown上传图片
class NewMardown(View):
    """
           1, 获取参数
           2，验证类型
           3，判断响应
           4，返回
           :param request:
           :return:
           """
    def post(self,request):
        image_file = request.FILES.get('editormd-image-file')
        if not image_file:
            logger.info('从前端获取图片失败')
            return http.JsonResponse({'success': 0, 'message': '从前端获取图片失败'})

        if image_file.content_type not in ('image/jpeg', 'image/png', 'image/gif'):
            return http.JsonResponse({'success': 0, 'message': '不能上传非图片文件'})

        try:  # jpg
            image_ext_name = image_file.name.split('.')[-1]  # 切割后返回列表取最后一个元素尾缀
        except Exception as e:
            logger.info('图片拓展名异常：{}'.format(e))
            image_ext_name = 'jpg'
        try:
            upload_res = FDFS_Client.upload_by_buffer(image_file.read(), file_ext_name=image_ext_name)
        except Exception as e:
            logger.error('图片上传出现异常：{}'.format(e))
            return http.JsonResponse({'success': 0, 'message': '图片上传异常'})
        else:
            if upload_res.get('Status') != 'Upload successed.':
                logger.info('图片上传到FastDFS服务器失败')
                return http.JsonResponse({'success': 0, 'message': '图片上传到服务器失败'})
            else:
                image_name = upload_res.get('Remote file_id')
                image_url = prod.FDFS_URL + image_name
                return http.JsonResponse({'success': 1, 'message': '图片上传成功', 'url': image_url})
mardown_url=NewMardown.as_view()




#文章发布

class NewsPub(View):
    def get(self,request):
        tags=Tag.objects.only('name').filter(is_delete=False)
        return render(request,'admin/news/News_edit.html',context={'tags':tags})
    def post(self, request):
        """
        获取表单数据
        数据清洗/判断是否合法
        保存到数据库
        :param request:
        :return:
        """
        json_str = request.body
        if not json_str:
            res_json(errno=Code.PARAMERR, errmsg='参数错误')
        dict_data = json.loads(json_str)

        # 数据清洗
        form = NewsPubForm(data=dict_data)
        if form.is_valid():
            # 对于作者更新对于的新闻， 知道新闻是哪个作者发布的
            # 创建实例  不保存到数据库
            newss = form.save(commit=False)
            newss.author_id = request.user.id
            newss.save()
            return res_json(errmsg='文章发布成功')

        else:
            err_m_l = []
            for i in form.errors.values():
                err_m_l.append(i[0])
            err_msg_str = '/'.join(err_m_l)
            return res_json(errno=Code.PARAMERR, errmsg=err_msg_str)

#轮播图展示,修改
class Newsbanner(View):
    def get(self,request):
        banners = Banner.objects.only('id', 'image_url', 'priority').filter(is_delete=False)
        priority_dict = OrderedDict(Banner.B_CHOICES) #实现字典元素的排序
        return render(request,'admin/news/news_banner.html',context={'banners':banners,'priority_dict':priority_dict})

        # 更新轮播图
class Banneredit(View):
    def put(self, request, b_id):
        """
        1.获取参数 Image pri id
        2.处理id
        3.数据清洗
        4验证优先级
        处理图片
        判断是否有修改 去数据库取参数 对比 前台的传参
        保存入库
        :param request:
        :param b_id:
        :return:
        """
        banners = Banner.objects.only('id').filter(is_delete=False, id=b_id).first()
        if not banners:
            return res_json(errno=Code.PARAMERR, errmsg='轮播图不存在')

        json_str = request.body
        if not json_str:
            return res_json(errno=Code.PARAMERR, errmsg='获取参数失败')
        dict_data = json.loads(json_str)

        # 获取参数  优先级
        priority = int(dict_data.get('priority'))  # 整形
        priority_list = [i for i, _ in Banner.B_CHOICES]  # 作用域

        if priority not in priority_list:
            return res_json(errno=Code.PARAMERR, errmsg='优先级不存在')

        image_url = dict_data['image_url']
        if not image_url:
            return res_json(errno=Code.PARAMERR, errmsg='图片数据为空')

        # 判断是否已修改

        if banners.priority == priority and banners.image_url == image_url:
            return res_json(errno=Code.PARAMERR, errmsg='数据没有修改')

        # 保存到数据库
        banners.priority = priority  # 1 2 3 4  5 6  看他的值
        banners.image_url = image_url

        banners.save(update_fields=['priority', 'image_url'])
        return res_json(errmsg='轮播图更新成功')

        # 轮播图删除

    def delete(self, request, b_id):
        banner = Banner.objects.filter(is_delete=False, id=b_id).first()
        if banner:
            banner.is_delete = True
            banner.save(update_fields=['is_delete'])
            return res_json(errno=Code.OK, errmsg='轮播图标签删除成功')
        else:
            return http.HttpResponseForbidden('轮播图不存在')


class up_to_Banner(View):
    def post(self,request):
        image_file=request.FILES('.banner-image')

#轮播图添加
class Newsbanneradd(View):
    """
    触发js路由，关联文章路由
    """
    def get(self,request):
        tags=Tag.objects.values('id','name').annotate(num_news=Count('news')).filter(is_delete=False)
        pri=OrderedDict(Banner.B_CHOICES)
        return render(request,'admin/news/banner_add.html',context={'tags':tags,'priority_dict':pri})
    #添加轮播图
    def post(self, request):

        json_str = request.body  # news_id   priority  image_url
        if not json_str:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])

        dict_data = json.loads(json_str)

        # 校验参数
        news_id = int(dict_data.get('news_id'))

        if not News.objects.filter(id=news_id).exists():
            return res_json(errno=Code.PARAMERR, errmsg='新闻不存在')
        try:
            priority = int(dict_data.get('priority'))

            priority_list = [i for i, _ in Banner.B_CHOICES]  # 作用域

            if priority not in priority_list:
                return res_json(errno=Code.PARAMERR, errmsg='轮播图优先级错误')
        except Exception as e:
            logger.info('轮播图优先级异常{}'.format(e))
            return res_json(errno=Code.PARAMERR, errmsg='轮播图优先级错误')

        image_url = dict_data.get('image_url')
        if not image_url:
            return res_json(errno=Code.PARAMERR, errmsg='轮播图优先级为空')

        # 创建轮播图  obj  true
        # 创建实例  保存到数据库
        banner = Banner.objects.get_or_create(news_id=news_id, priority=priority)

        banners, is_cre = banner
        banners.priority = priority
        banners.image_url = image_url
        banners.save(update_fields=['priority', 'image_url'])
        return res_json(errmsg='轮播图创建成功')



#文档管理
class Doc_Manage(View):
    def get(self,request):
        doc=Doc.objects.only('title','update_time').filter(is_delete=False)
        return render(request,'admin/doc/doc_manage.html',context={'docs':doc})

    def post(self, request):
        json_data = request.body
        if not json_data:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        # 将json转化为dict
        dict_data = json.loads(json_data.decode('utf8'))
        form = DocsPubForm(data=dict_data)
        if form.is_valid():
            docs_instance = form.save(commit=False)
            docs_instance.author_id = request.user.id
            docs_instance.save()
            return res_json(errmsg='文档创建成功')
        else:
            # 定义一个错误信息列表
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
            err_msg_str = '/'.join(err_msg_list)  # 拼接错误信息为一个字符串
            return res_json(errno=Code.PARAMERR, errmsg=err_msg_str)


#文档管理编辑
class Doc_edit(View):
    def get(self,request,d_id):
        docs=Doc.objects.filter(is_delete=False,id=d_id).first()
        if docs:
           return render(request,'admin/doc/doc_edit.html',context={'doc':docs})
        else:
            return http.HttpResponseNotFound('NOT PAGE FOUND')
        #上传文件
    def put(self,request,d_id):
         docs = Doc.objects.filter(is_delete=False, id=d_id).first()
         js_str=request.body
         if not js_str:
             return res_json(errno=Code.PARAMERR,errmsg='参数错误')

         js_str=json.loads(js_str)

         form = DocsPubForm(data=js_str)
         if form.is_valid():
           for k,v in form.cleaned_data.items():
                 setattr(docs,k,v)     #v是值，k是键
                 docs.save()
                 return res_json(errno=Code.OK,errmsg='文档编辑成功')
           else:
               # 定义一个错误信息列表
               err_msg_list = []
               for item in form.errors.get_json_data().values():
                   err_msg_list.append(item[0].get('message'))
               err_msg_str = '/'.join(err_msg_list)  # 拼接错误信息为一个字符串
               return res_json(errno=Code.PARAMERR, errmsg=err_msg_str)
         # 删除文件

    def delete(self, request, d_id):
        docs = Doc.objects.filter(id=d_id).first()
        if docs:
            docs.is_delete = True
            docs.save(update_fields=['is_delete'])
            return res_json(errno=Code.OK, errmsg='文档删除成功')
        else:
            return http.HttpResponseForbidden('文档不存在')

#文档添加

class docs_pub(View):
    def get(self,request):
        return render(request, 'admin/doc/doc_edit.html')

    def post(self, request):
        json_data = request.body
        if not json_data:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        # 将json转化为dict
        dict_data = json.loads(json_data.decode('utf8'))
        form = DocsPubForm(data=dict_data)
        if form.is_valid():
            docs_instance = form.save(commit=False)
            docs_instance.author_id = request.user.id
            docs_instance.save()
            return res_json(errmsg='文档创建成功')
        else:
            # 定义一个错误信息列表
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
            err_msg_str = '/'.join(err_msg_list)  # 拼接错误信息为一个字符串
            return res_json(errno=Code.PARAMERR, errmsg=err_msg_str)
#课程管理
# setattr(self,k,v) 是相当于self.k = v
#item()遍历字典
# 官方文档内容：
# setattr(object, name, value)


#课程管理#
class course_manage(View):
    def get(self,request):
        course=Course.objects.only('id','title','category__name','teacher__name').select_related('category','teacher').filter(is_delete=False)
        return render(request,'admin/course/course_manage.html',context={'courses':course})


#课程编辑
class course_edit(View):

    def get(self,request,c_id):
        course = Course.objects.filter(is_delete=False, id=c_id).first()
        if course:
            teacher=Teacher.objects.only('name').filter(is_delete=False,id=c_id)
            contal=CourseCategory.objects.only('name').filter(is_delete=False,id=c_id)
            return render(request,'admin/course/course_pub.html',context={'course':course,'teachers':teacher,'categories':contal})
        else:
             return http.HttpResponseForbidden('NOT PAGE FOUND')
    #编辑视频
    def put(self, request,c_id):
        json_data = request.body
        if not json_data:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        dict_data = json.loads(json_data.decode('utf8'))

        form = CoursesPubForm(data=dict_data)
        if form.is_valid():
            courses_instance = form.save()
            return  res_json(errmsg='课程发布成功')
        else:
            # 定义一个错误信息列表
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
            err_msg_str = '/'.join(err_msg_list)  # 拼接错误信息为一个字符串

            return  res_json(errno=Code.PARAMERR, errmsg=err_msg_str)

    def delete(self, request, c_id):
            course = Course.objects.only('id').filter(is_delete=False).first()
            if course:
                course.is_delete = True
                course.save(update_fields=['is_delete'])
                return res_json(errno=Code.OK, errmsg='视频删除成功')
            else:
                return http.HttpResponseForbidden('视频不存在')


#课程发布
class course_pub(View):
    def get(self,request):
            teacher = Teacher.objects.only('name').filter(is_delete=False)
            contal = CourseCategory.objects.only('name').filter(is_delete=False)
            return render(request,'admin/course/course_pub.html',context={'teachers':teacher,'categories':contal})

    def post(self,request):
        json_data = request.body
        if not json_data:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        dict_data = json.loads(json_data.decode('utf8'))

        form = CoursesPubForm(data=dict_data)
        if form.is_valid():
            courses_instance = form.save()
            return res_json(errmsg='课程发布成功')
        else:
            # 定义一个错误信息列表
            err_msg_list = []
            for item in form.errors.get_json_data().values():
                err_msg_list.append(item[0].get('message'))
            err_msg_str = '/'.join(err_msg_list)  # 拼接错误信息为一个字符串

            return res_json(errno=Code.PARAMERR, errmsg=err_msg_str)



#组管理
class Group_Manager(View):
    def get(self,request):
        group_manager=Group.objects.values('id','name').annotate(num_users=Count('user')).order_by('-num_users','-id')
        return render(request,'admin/users/group_manager.html',context={'groups':group_manager})

g=Group_Manager.as_view()

#用户添加
class Group_Add(View):
    def get(self,request):
        per=Permission.objects.all()
        return render(request,'admin/users/group_add.html',context={'permissions':per})
    #创建用户组
    def post(self,request):
        json_data = request.body
        if not json_data:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        dict_data = json.loads(json_data.decode('utf8'))

        # 取出组名，进行判断
        group_name = dict_data.get('name', '').strip()
        if not group_name:
            return res_json(errno=Code.PARAMERR, errmsg='组名为空')

        one_group, is_created = Group.objects.get_or_create(name=group_name)
        if not is_created:
            return res_json(errno=Code.DATAEXIST, errmsg='组名已存在')

        # 取出权限
        group_permissions = dict_data.get('group_permissions')
        if not group_permissions:
            return res_json(errno=Code.PARAMERR, errmsg='权限参数为空')

        try:
            # [10, 2, 3, 10, 3, 2, 4]
            permissions_set = set(int(i) for i in group_permissions)
        except Exception as e:
            logger.info('传的权限参数异常：\n{}'.format(e))
            return res_json(errno=Code.PARAMERR, errmsg='权限参数异常')

        all_permissions_set = set(i.id for i in Permission.objects.only('id'))
        if not permissions_set.issubset(all_permissions_set):
            return res_json(errno=Code.PARAMERR, errmsg='有不存在的权限参数')

        # 设置权限
        for perm_id in permissions_set:
            p = Permission.objects.get(id=perm_id)
            one_group.permissions.add(p)

        one_group.save()
        return res_json(errmsg='组创建成功！')
#用户编辑
class Group_edit(View):
    permission_required = ('auth.change_group', 'auth.delete_group')
    raise_exception = True

    def handle_no_permission(self):
        if self.request.method.lower() != 'get':
            return res_json(errno=Code.ROLEERR, errmsg='没有操作权限')
        else:
            return super(Group_edit, self).handle_no_permission()
    def get(self,request,g_id):
        group=Group.objects.filter(id=g_id).first()
        if group:
            per = Permission.objects.all()
            return render(request,'admin/users/group_add.html',context={'permissions':per,'group':group})
        else:
            return http.HttpResponseNotFound('NOT PAGE FOUND')
 #修改用户及传限
    def put(self,request,g_id):
        group = Group.objects.filter(id=g_id).first()
        if not group:
            return res_json(errno=Code.NODATA, errmsg='需要更新的用户组不存在')

        json_data = request.body
        if not json_data:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        # 将json转化为dict
        dict_data = json.loads(json_data.decode('utf8'))

        # 取出组名，进行判断
        group_name = dict_data.get('name', '').strip()
        if not group_name:
            return res_json(errno=Code.PARAMERR, errmsg='组名为空')

        if group_name != group.name and Group.objects.filter(name=group_name).exists():
            return res_json(errno=Code.DATAEXIST, errmsg='组名已存在')

        # 取出权限
        group_permissions = dict_data.get('group_permissions')
        if not group_permissions:
            return res_json(errno=Code.PARAMERR, errmsg='权限参数为空')

        try:
            permissions_set = set(int(i) for i in group_permissions)
        except Exception as e:
            logger.info('传的权限参数异常：\n{}'.format(e))
            return res_json(errno=Code.PARAMERR, errmsg='权限参数异常')

        all_permissions_set = set(i.id for i in Permission.objects.only('id'))
        if not permissions_set.issubset(all_permissions_set):
            return res_json(errno=Code.PARAMERR, errmsg='有不存在的权限参数')

        existed_permissions_set = set(i.id for i in group.permissions.all())
        if group_name == group.name and permissions_set == existed_permissions_set:
            return res_json(errno=Code.DATAEXIST, errmsg='用户组信息未修改')
        group_permissions.clear() #清除之前的数据 保存之前清除旧的传限
        # 设置权限
        for perm_id in permissions_set:
            p = Permission.objects.get(id=perm_id)
            group.permissions.add(p)
        group.name = group_name
        group.save()
        return res_json(errmsg='组更新成功！')
#删除
    def delete(self,request,g_id):
        g=Group.objects.filter(id=g_id).first()
        if g:
            g.permissions.clear()
            g.delete()
            return res_json(errmsg='组删除成功')
        else:
            return http.HttpResponseForbidden()


#用户管理
def User_manage(request):
    users=Users.objects.only('username','is_staff','is_superuser').filter(is_active=True)
    return render(request,'admin/users/users_manage.html',context={'users':users})


#用户编辑
class User_edit(View):
    def get(self,request,u_id):
         template_name = 'admin/users/users_edit.html'
         users=Users.objects.filter(id=u_id).first()
         groups = Group.objects.only('name').all()
         if users:
             return render(request, template_name=template_name, context={'user_instance':users,'groups': groups})
         else:
             return http.HttpResponseForbidden()
   #修改用户
    def put(self, request, u_id):
        user_instance = Users.objects.filter(id=u_id).first()
        if not user_instance:
            return res_json(errno=Code.NODATA, errmsg='需要更新的用户不存在')

        json_data = request.body
        if not json_data:
            return res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        # 将json转化为dict
        dict_data = json.loads(json_data.decode('utf8'))

        # 取出参数，进行判断
        try:
            groups = dict_data.get('groups')  # 取出用户组列表

            is_staff = int(dict_data.get('is_staff'))
            is_superuser = int(dict_data.get('is_superuser'))
            is_active = int(dict_data.get('is_active'))
            params = [is_staff, is_superuser, is_active]
            if not all([p in (0, 1) for p in params]):
                return res_json(errno=Code.PARAMERR, errmsg='参数错误')
        except Exception as e:
            logger.info('从前端获取参数出现异常：\n{}'.format(e))
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')

        try:
            groups_set = set(int(i) for i in groups) if groups else set()
        except Exception as e:
            logger.info('传的用户组参数异常：\n{}'.format(e))
            return res_json(errno=Code.PARAMERR, errmsg='用户组参数异常')

        all_groups_set = set(i.id for i in Group.objects.only('id'))
        if not groups_set.issubset(all_groups_set):
            return res_json(errno=Code.PARAMERR, errmsg='有不存在的用户组参数')

        gs = Group.objects.filter(id__in=groups_set)
        # 先清除组
        user_instance.groups.clear()
        user_instance.groups.set(gs)

        user_instance.is_staff = bool(is_staff)
        user_instance.is_superuser = bool(is_superuser)
        user_instance.is_active = bool(is_active)
        user_instance.save()
        return res_json(errmsg='用户信息更新成功！')


  #删除用户
    def delete(self, request, u_id):
        user_instance = Users.objects.filter(id=u_id).first()
        if user_instance:
            user_instance.groups.clear()  # 清除用户组
            user_instance.user_permissions.clear()  # 清除用户权限
            user_instance.is_active = False  # 设置为不激活状态
            user_instance.save()
            return res_json(errmsg="用户删除成功")
        else:
            return res_json(errno=Code.PARAMERR, errmsg="需要删除的用户不存在")
