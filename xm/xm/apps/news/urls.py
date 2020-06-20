#
from django.urls import path
from . import views
app_name = 'index'

urlpatterns = [
    # path('', views.index, name='index'),   # 将这条路由命名为index
    path('', views.index, name='index'),  # 将这条路由命名为index
    path('news/', views.news, name='news'),  # 将这条路由命名为index
    path('news/<int:news_id>/', views.detail, name='n_detail'),  # 详情页面
    path('news/banners/', views.banner, name='banner'),  # 详情页面
    path('d/', views.d),  # 百度存储图片测试
    path('news/<int:news_id>/comments/', views.comment,name='comments'),  # 百度存储图片测试
    path('search/', views.Search(), name='search'),
    # path('course/', views.course, name='course'),


]