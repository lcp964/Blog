from django.db import models
from django.contrib.auth.models import AbstractUser,UserManager as _UserManager

# Create your models here.





class UserManager(_UserManager):
    def create_superuser(self, username, password, email=None, **extra_fields):
         return super(UserManager,self).create_superuser(username=username,password=password,email=email,**extra_fields)
        # return self._create_user(username, email, password, **extra_fields)

class Users(AbstractUser):
    object = UserManager()
    REQUIRED_FIELDS = ['mobile']
    mobile = models.CharField(max_length=11, unique=True, verbose_name="手机号",
                              error_messages={'unique': "此手机号已注册"}  # 指定报错的中文信息
                              )
    email_ac=models.BooleanField(default=False,verbose_name='邮箱状态')
    class Meta:
        db_table='tb_users'
        verbose_name='用户'
        verbose_name_plural=verbose_name #指定负数s没有加

    def __str__(self):
        return  self.username

    def get_groups_name(self):
        g_name=(i.name for i in self.groups.all()) #获取组名
        return '/'.join(g_name)

