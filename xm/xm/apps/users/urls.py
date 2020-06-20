app_name='users'#建议这种方法，方便在里面查找领命空间
from apps.verifications.views import send_sms
from django.urls import path
from .import views

urlpatterns = [
    path('register/', views.reg, name='register'),
    # path('register', views.register, name='register'),
    path('login/', views.lo, name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('check/', views.check,name='check'),
    path('forgot/', views.fp,name='forgot'),
    path('send_sms/', send_sms)
    # uuid:img_id
]