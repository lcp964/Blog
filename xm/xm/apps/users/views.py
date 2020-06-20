import json
import re
from django.http import HttpResponseForbidden  # 丑拒
from django.shortcuts import render, redirect,reverse
from django_redis import get_redis_connection
from django.contrib.auth import login, logout, authenticate
from users.models import Users
from utils.res_code import res_json, Code, error_map
from django.views import View
from users.forms import LoginForm #导包传值
from django.contrib.auth.hashers import check_password, make_password

# Create your views here.
# def index(request):
#     return HttpResponse('hello django')

# def register(request):
#     return render(request, 'users/register.html')

# def login(request):
#     return render(request, 'users/login.html')





import logging

logger = logging.getLogger('django')


# 注册
class RegisterView(View):
    def get(self, request):
        return render(request, "users/register.html")
    def post(self,request):
        js_str = request.body
        if not js_str:
            res_json(errno=Code.PARAMERR, errmsg=error_map[Code.PARAMERR])
        dict_data = json.loads(js_str)
        username = dict_data.get('username')
        password = dict_data.get('password')
        password1 = dict_data.get('password_repeat')
        mobile = dict_data.get('mobile')
        sms_code = dict_data.get('sms_code')
        if not all([username, password, password1, mobile, sms_code]):
            return HttpResponseForbidden('请输入正常的参数')
            # 用户名
        if not re.match(r'^[\u4e00-\u9fa5\w]{5,20}$', username):
            return HttpResponseForbidden('请输入正确的用户名')
        # 判断数据库是否存在用户名
        if Users.objects.filter(username=username).count() > 0:
            return HttpResponseForbidden('用户名已经存在，请重新输入')
        # 密码
        if not re.match(r'^[0-9A-Za-z]{6,20}$', password):
            return HttpResponseForbidden('请输入正确的密码')
        if password != password1:
            return res_json(errmsg='两次输入密码有错误')

        # 手机号验证
        if not re.match(r'^1[345789]\d{9}$',mobile):
            return HttpResponseForbidden('请输入正确的手机号')
        if Users.objects.filter(mobile=mobile).count() > 0:
            return HttpResponseForbidden('手机号已经存在，请重新输入')

        # 校验验证码
        redis_conn = get_redis_connection('verify_code')
        sms_code_server = redis_conn.get('sms_{}'.format(mobile) )

        # 判断是否过期
        if sms_code_server is None:
            return redis_conn(errno=Code.PARAMERR, errmsg='此验证码已过期')

        # 删除验证码
        redis_conn.delete('sms_{}'.format(mobile))
        # 删除标记
        redis_conn.delete('sms_flag_{}'.format(mobile))

        # 判断验证码是否跟数据库一直，数据库需要解码
        if sms_code != sms_code_server.decode():
            return HttpResponseForbidden('短信验证码错误，请重新输入')

        # 创建用户
        user=Users.objects.create_user(username=username, password=password, mobile=mobile)  # 注意用create_user,我们用USERmange管理系统

        # 保存连接
        login(request, user)  # user是保存对象
        return res_json(errmsg='恭喜你，注册成功！')
reg=RegisterView.as_view()




# 登录
class LogginView(View):
    def get(self, request):
        title='登录页面'
        return render(request, 'users/login.html',context={'title':title})
    #is_authenticated()判断用户名是否登录，登录成功为true
    def post(self, request):
        js_str = request.body
        if not js_str:
            return res_json(errno=Code.PARAMERR, errmsg='参数错误')
        dict_data = json.loads(js_str.decode())
        # 数据验证   使用form 表单验证
        form = LoginForm(data=dict_data, request=request)
        if form.is_valid():
            # 表单验证成工处理
            return res_json(errno=Code.OK)
        else:
            # 表单验证失败处理
            msg_list = []
            for i in form.errors.get_json_data().values():
                msg_list.append(i[0].get('message'))
            msg_str = '/'.join(msg_list)
        return res_json(errno=Code.PARAMERR, errmsg=msg_str)

lo = LogginView.as_view()

#退出登录

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse("users:login"))

#修改密码

class checkpwdView(View):
    def get(self,request):
        title='修改密码页面'
        return render(request, 'users/checked_pwq.html',context={'title':title})
    def post(self,request):
      mobile=request.POST.get('telphone')
      old=request.POST.get('old_password')
      new=request.POST.get('new_password')
      new1=request.POST.get('new1_password')
      if not all([mobile, old, new,new1]):
          return HttpResponseForbidden('参数问题')
      if not re.match(r'^1[3-9]\d{9}$',mobile) :
          return HttpResponseForbidden('输入手机号有误')
      user = Users.objects.get(mobile=mobile)
      if user:
          try:
             check_password(old,user.password)
          except Exception as e:
              logger.error(e)
              return HttpResponseForbidden('原始密码输入错误')
          # 密码验证
          if not re.match(r'^[0-9A-Za-z]{6,20}$', new):
              return HttpResponseForbidden('密码格式错误')
          # 密码对比
          if old == new:
              return HttpResponseForbidden('密码未修改')
          # 密码修改
          if new != new1:
              return HttpResponseForbidden('确认密码与新密码不一致')
          user.set_password(new)
          user.save()
          res = redirect(reverse('users:login'))
          return res
      else:
          return HttpResponseForbidden('用户账号不存在')


check=checkpwdView.as_view()

#忘记密码
class forgot_PasswordView(View):
    def get(self,request):
        title = '忘记密码页面'
        return render(request, 'users/forgot_Password.html', context={'title': title})
    def post(self,request):
        res_erro=res_json(errno=Code.PARAMERR, errmsg='参数错误')
        data = request.body
        data = json.loads(data).decode()
        if not data:
            return res_erro

        psd = data['password']
        qpsd = data['password_repeat']
        mobile = data['mobile']
        sms_num = data['sms_code']
        if not all([psd, mobile, sms_num,  qpsd]):
            return res_erro
        # 数据清洗  判断格式
        if not re.match(r'^[a-zA-Z0-9]{6,20}$', psd):
            return res_error
        if not re.match(r'^[a-zA-Z0-9]{6,20}$', qpsd):
            return res_error
        if psd != qpsd:
            return res_error
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return res_error
        # 处理验证码
        redis_conn = get_redis_connection('verify_code')
        # 取值
        # 构造一个键
        redis_key = 'sms_{}'.format(mobile)
        sms_code = redis_conn.get(redis_key).decode()
        redis_conn.delete(redis_key)
        redis_conn.delete('sms_flag_' + mobile)
        if sms_num != sms_code:
            return HttpResponseForbidden('验证码错误')
        try:
            user = Users.objects.get(mobile=mobile)
        except Exception as e:
            logger.error(e)
            return HttpResponseForbidden('参数错误')
        else:
            user.set_password(psd)
            user.save()
            return res_json(errmsg='密码已更新，请回去登录')
fp=forgot_PasswordView.as_view()