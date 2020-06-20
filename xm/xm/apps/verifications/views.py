import users
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound,JsonResponse
from celery_tasks.sms import tasks as sms_tasks
from celery_tasks.sms.tasks import send_sms_code
from users.views import logger
from utils.res_code import Code,error_map
from utils.res_code import res_json
from utils.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.views import View
from users.models import Users
from utils.yuntongxun.sms import CCP

import json
import  random

# Create your views here.
#图形验证
def Image_code(request,img_id):
    text, image = captcha.generate_captcha()
    redis_conn=get_redis_connection('verify_code') #连接数据库
    #保存
    redis_conn.setex('img_{}'.format(img_id).encode('utf-8'),300,text)

    logger.info('图形验证码是:{}'.format(text))
    request.session['image_code']=text
    #设置过期时间
    request.session.set_expiry(60)
    print(request.session.keys)
    print(request.session.get('image_code'))
    return HttpResponse(content=image,content_type='image/jpg')#加s代表下载

#用户名验证
class CheckUsernameView(View):
    """
    验证用户名
    route:username/(?P<username>\w{5,20})/
    :param username:
    """
    def get(self,request,username):
        """
        统计数量 如果用户名重复 ，他的数量变成1
        :param request:
        :param username:
        :return:count
        """
        count=users.models.Users.objects.filter(username=username).count() #检查重复的数据
        #返回json格式
        data={
            'username':username,
            'count':count,
        }


        return res_json(data=data)

#手机号验证
class CheckmobileView(View):

    def get(self,request,mobile):
        """

        :param request:
        :param mobile:
        :return:
        """
        count=users.models.Users.objects.filter(mobile=mobile).count()
        data={
            'mobile':mobile,
            'count':count,
        }
        return res_json(data=data)


class SmsCodesView(View):

    def post(self,request):
        """
        手机号，图形验证码 ，uuid
        :param request:
        :return:
        """
        #接受参数
        json_str=request.body
        if not  json_str:
            return res_json(errno=Code.PARAMERR,errmsg='参数错误') #4013参数错误
        dict_date=json.loads(json_str)
        #获取前台传过来的参数
        image_code_client=dict_date.get('text')
        uuid=dict_date.get('image_code_id')
        mobile=dict_date.get('mobile')
        #参数验证
        if not all([image_code_client,uuid,mobile]):
            return res_json(errno=Code.PARAMERR,errmsg='参数错误')
        #连接数据库
        redis_conn=get_redis_connection('verify_code')
        image_code_server=redis_conn.get('img_%s' % uuid)
        if image_code_server is None:
            return  res_json(errno=Code.PARAMERR,errmsg=error_map[Code.PARAMERR])
        #删除数据库的验证码，防止重复测试
        try:
         redis_conn.delete('img_{}'.format(uuid))
        except Exception as e:
            logger.error(e)
        #比对
        #解码
        image_code_server=image_code_server.decode()
        if image_code_client.lower() != image_code_server.lower(): #强转大小写
            return  res_json(errno=Code.PARAMERR,errmsg='图形验证码输入有误')

        #生成短信验证码,补全
        sms_code='%06d' % random.randint(0,999999)

        #存数据库，下次使用
        redis_conn.setex('sms_{}'.format(mobile),300,sms_code)
        seng_flag =redis_conn.get('sms_flag_{}'.format(mobile))
        if seng_flag:
            return res_json(errno=Code.DATAEXIST,errmsg='短信发送频繁')
        # 标记手机号在60秒内有发送过短信
        redis_conn.setex('sms_flag_{}'.format(mobile),60,1)
        logger.info('短信验证码是:{}'.format(sms_code))
        logger.info('发送短信验证成功[mobile:{}sms_code:{}]'.format(mobile,sms_code))
        # #调用接口发短信
        # ccp=CCP()
        # ccp.send_template_sms(mobile,[sms_code,5],1)
        send_sms_code.delay(mobile,sms_code) #触发短信模块
        return res_json(errmsg='短信验证码发送成功')

send_sms=SmsCodesView.as_view()
