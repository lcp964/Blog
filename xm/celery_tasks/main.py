from celery import Celery
import os
# 初始化
if not os.getenv('DJANGO_SETTINGS_MODULE'):
 os.environ['DJANGO_SETTINGS_MODULE'] = 'xm.settings.ds'
 os.environ['DJANGO_SETTINGS_MODULE'] = 'xm.settings.ds'

# 创建实例

celery_app= Celery('sms_code')
##加载配置

celery_app.config_from_object('celery_tasks.config')
#注册任务

celery_app.autodiscover_tasks(['celery_tasks.sms'])