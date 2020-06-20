from django import template
from datetime import  datetime
import pytz

register = template.Library()

@register.filter()
def time_filter(data):
    if isinstance(data,datetime): #在什么范围内
        now=datetime.now()
        now=now.replace(tzinfo=pytz.timezone('UTC'))
        timestamp = (now-data).total_seconds() #获取时间戳，当前时间减去发布时间统计
        if timestamp<60:
            return '刚刚'

        if timestamp>=60 and timestamp<60*60:
            mim=int(timestamp//(60))
            return '{}分钟前'.format(mim)

        elif  timestamp >= 60*60 and timestamp < 60 * 60*24:
            hour = int(timestamp // (60*60))
            return '{}小时前'.format(hour)
        elif timestamp >= 60*60*24*30 and timestamp < 60 * 60*24*7*52*24:
            month = int(timestamp // (60*60*24*30))
            return '{}月前'.format(month)
        elif timestamp >= 60 * 60*24*7*52*24 and timestamp < 60 * 60*24*7*52*24*2:
            year = int(timestamp // (60 * 60*24*7*52*24))
            return '{}年前'.format(year)
        elif timestamp >= (60 * 60*24*7*52*24*2):
            return '凉凉'
    else:
        return data.strftime('%Y-%m-%d %H-%M' )
