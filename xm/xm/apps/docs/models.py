from django.db import models

# Create your models here.
from xm.utils.model import baseModel

#创建模型
class Doc(baseModel):
    file_url=models.URLField(verbose_name='书籍路由')
    title=models.CharField(max_length=150,verbose_name='书籍标题')
    docs=models.TextField(verbose_name='书籍介绍')
    image_url=models.URLField(verbose_name='书籍图片地址',default='')
    author=models.ForeignKey('users.Users',on_delete=models.SET_NULL,verbose_name='作者',null=True)

    class Meta:
            db_table='tb_docs'
            verbose_name='书籍'
            verbose_name_plural=verbose_name

    def __str__(self):
        return self.title