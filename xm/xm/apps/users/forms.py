from django import forms  #django自带的form表单
from django.db.models import Q #是与或非的包
from .import constants #设置过期时间包
from.models import Users
from django.contrib.auth import login
import re
class LoginForm(forms.Form):
    user_account=forms.CharField() #用户名或者手机号不方便写约束
    password=forms.CharField(min_length=6,max_length=20,
                             error_messages={'min_length':'密码长度大于6',
                                              'max_length':'密码长度小于20',
                                              'required':'密码不能为空'                              } )
    remember=forms.BooleanField(required=False)#布尔值来判断

    def __init__ (self,*a,**k): #初始化
        self.request = k.pop('request') #删除request
        super().__init__(*a,**k)   #重写

    def clean_user_account(self): # #针对单个字段预留的方法（也就是该字段通过form验证以后就会触发该对应名字的自定义方法）
       user_info=self.cleaned_data.get('user_account') #cleaned_data中的值类型与字段定义的Field类型一致
      #清洗拿到数据
       if not user_info:
           raise forms.ValidationError('用户名不能为空') #form里面异常报错
       if not re.match(r'^1[3-9]\d{9}$]',user_info) and (len(user_info)<5 or len(user_info)>20):
           raise forms.ValidationError('输入的用户名格式错误,请重新输入!')
       return user_info
    #重写clean方法
    def clean(self):
        clean_date=super().clean() #super重写的意思 继承父类的方法
        user_info=clean_date.get('user_account')
        pass_wd=clean_date.get('password')
        rmber=clean_date['remember']
    #判断是否是用户名还是手机号
        user_qs=Users.objects.filter(Q(mobile=user_info) | Q(username=user_info))
        if user_qs:
          user=user_qs.first() #如果为真返回第一个数据
          if user.check_password(pass_wd):
            if rmber:
                # self.request.session.set_expiry(None) #None为14天  写法一
                self.request.session.set_expiry(constants.SESSION_EXPIRY_TIME) #None为14天 写法二

            else:
                # self.request.session.set_expiry(0) #一次交易 写法一
                self.request.session.set_expiry(constants.SESSION_TIME)
            login(self.request, user)
                #一次交易 写法二
          else:
            raise  forms.ValidationError('用户名或密码错误，请重新输入')

        else:
            raise forms.ValidationError('用户名不存在，请重新输入')

