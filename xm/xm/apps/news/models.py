from django.db import models
from news.templatetags.data_files import time_filter
# Create your models here.
from django.db.models import Model
from utils.model import baseModel
import pytz
import datetime
'''
1.分类导航
2.轮播图 图片 优先级
3.热门新闻，关联news ，优先级
4.图片 标题 重点 点击量 时间 内容 关联【作者,分类】 ,详情页，评论
5.评论，客服，收藏，等
'''
class Tag(baseModel): #model的作用是定义出对象模型，一般都是和数据库里表对应，一个表一个model类，表里面的字段对应model类的属性，这其实是MVC思想中的M的model层
    name=models.CharField(max_length=60,verbose_name='分类名字')
    class Meta:
        ordering = ['-update_time', '-id']  # 排序，-降序，+升序，里面是对象
        db_table='news_tag'
        verbose_name='新闻分类'
        verbose_name_plural=verbose_name #verbose_name指定在admin管理界面中显示中文；verbose_name表示单数形式的显示，verbose_name_plural表示复数形式的显示；中文的单数和复数一般不作区别。
#轮播图
class Banner(baseModel):
        B_CHOICES=[
            (1, '第一级'),
            (2, '第二级'),
            (3, '第三级'),
            (4, '第四级'),
            (5, '第五级'),
            (6, '第六级'),

        ]
        image_url =models.URLField(verbose_name='图片地址')
        priority=models.IntegerField(verbose_name='优先级',choices=B_CHOICES,default=6)
        news=models.OneToOneField('News',on_delete=models.CASCADE)
        class Meta:
                ordering=['-update_time','id'] #排序，-降序，+升序，里面是对象
                db_table = 'tb_banner'
                verbose_name = '轮播图'
                verbose_name_plural = verbose_name

        def __str__(self):
                 return '<轮播图{}>'.format(self.id) #拼接
# 新闻
class News(baseModel):
    title=models.CharField(verbose_name='标题',max_length=150)
    digest=models.CharField(verbose_name='摘要',max_length=200)
    content=models.TextField(verbose_name='内容')
    clicks=models.IntegerField(verbose_name='点击率',default=0)
    image_url=models.URLField(verbose_name='图片地址',default='')
    tag=models.ForeignKey('Tag',verbose_name='分类',on_delete=models.SET_NULL,null=True)
    author=models.ForeignKey('users.Users',verbose_name='作者',on_delete=models.SET_NULL,null=True)
    #点击量排名

    class Meta:
        ordering = ['-update_time', '-id']  # 排序，-降序，+升序，里面是对象
        db_table = 'tb_news'
        verbose_name = '新闻'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title  # 拼接

    def increase_clicks(self):
        self.clicks += 1
        self.save(update_fields=['clicks'])

    def to_put(self):
        l_dict={
            'id':self.id,
            'title':self.title,
            'digest':self.digest,
            'image_url':self.image_url,
            'tag_name':self.tag.name,
            'update_time':time_filter(self.update_time),
            'author':self.author.username,
        }
        return l_dict
# #热门新闻
class  HotNews(baseModel):
    P_CHOICES=[(1,'第一级'),
               (2, '第二级'),
               (3, '第三级'),
               ]
    news=models.OneToOneField('News',on_delete=models.CASCADE) #级联删除
    priority=models.IntegerField(verbose_name='优先级',choices=P_CHOICES)

    class Meta:
        ordering = ['-update_time', '-id']  # 排序，-降序，+升序，里面是对象
        db_table = 'tb_hotnews'
        verbose_name = '热门新闻'
        verbose_name_plural = verbose_name

    def __str__(self):
            return '<热门新闻{}>'.format(self.id) # 拼接


#评论去
class Comment(baseModel):
    content=models.TextField(verbose_name='评论内容')
    author=models.ForeignKey('users.Users',on_delete=models.SET_NULL,null=True) #关联用户，设置为空
    news=models.ForeignKey('News',on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE,blank=True)

    class Meta:
        ordering = ['-update_time', '-id']
        db_table = 'tb_comment'
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        # 初始化
   #自定义模型
    def to_dict(self):
         # a=pytz.country_timezones('cn') #拿到中国时间
         # s=pytz.timezone(a[0]) #拿到上海时间
         # news_time=s.normalize(self.update_time) #转化亚洲时间

         comment_dict = {
            'news_id': self.news.id,
            'content_id': self.id,
            'content': self.content,
            'author': self.author.username,
            'update_time': time_filter(self.update_time),
             # 'update_time': news_time.strftime('%Y年%m月%d日 %H:%M'),
            'parent': self.parent.to_dict() if self.parent_id else None,
         }
         return comment_dict

    def __str__(self):  #返回上面对应消息
            return '<评论 {}>'.format(self.id) # 拼接

