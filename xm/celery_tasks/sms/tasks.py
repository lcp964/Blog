
#实现异步处理短信
from celery_tasks.main import celery_app


from xm.utils.yuntongxun.sms import CCP
from users.views import logger
#注册celeryapp #bind指定第一个任务，name指定下面的执行任务
@celery_app.task(bind=True,name='send_sms_code',retery_backoff=3) #bind保证task对象执行第一个参数，name是任务的名字 # retry_backoff   间隔时间
def send_sms_code(self,mobile,sms_code):
    """
    手机号
    短信
    短信验证码
    :param self:
    :param mobile:
    :param sms_code:
    :return:
    """
    try:
        send_res=CCP().send_template_sms(mobile,[sms_code,5],1) #1是模板，sms_code对象，5是分钟

    except Exception as e: #记录发送短信的异常
         logger.error(e)
         raise self.retry(exc=e,max_retries=3)#max_retries最大
    if send_res !=0:
        raise self.retry(exc=Exception('短信发送失败'),max_retries=3)
    return send_res

