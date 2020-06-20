app_name='verifications'#建议这种方法，方便在里面查找领命空间


from django.urls import path,re_path
from .import views

urlpatterns=[

    path('user/image_code/<uuid:img_id>/', views.Image_code, name='image_code'),
    re_path('username/(?P<username>[\u4e00-\u9fa5\w]{5,20})/',views.CheckUsernameView.as_view(),name='c_username'),
    re_path('mobiles/(?P<mobile>1[3-9]\d{9})/',views.CheckmobileView.as_view(),name='m_mobile'),
    # re_path('username/(?P<username>\w{5,20})/',views.CheckUsernameView.as_view(),name= 'c_username'),
    re_path('sms_code/',views.SmsCodesView.as_view(),name='sms_code'),

]