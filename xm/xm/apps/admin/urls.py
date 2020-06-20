from django.urls import path
from .import views
app_name='admin'
urlpatterns = [
    path('',views.admin.as_view(),name='index' ),
    path('tags/',views.tags,name='tag' ),
    path('tags/<int:tag_id>/',views.tags,name='tags' ),
    path('hot/',views.hot,name='hot' ),
    path('hot/<int:hotnews_id>/',views.Hotnewsedit.as_view(),name='hotnews_id'),
    path('hot/add/',views.HotnewsAdd.as_view(),name='hotadd_id'),
    path('tag/<int:t_id>/news/',views.NewsTagView.as_view(),name='NewsTagView'),
    path('news/', views.NewsManage.as_view(), name='news_manage'),
    path('news/<int:news_id>/', views.edit, name='news_edit'),
    #文件上传FDFS
    path('news/images/', views.up_to, name='news_images'),
    path('mardown/', views.mardown_url, name='markdown_image'),

    #文章发布
    path('news/pub/',views.NewsPub.as_view(),name='news_pub'),

    #轮播图
    path('banners/',views.Newsbanner.as_view(),name='banner'),
    path('banners/<int:b_id>/', views.Banneredit.as_view(), name='banner_edit'),
    #轮播图添加
    path('banners/add/',views.Newsbanneradd.as_view(),name='admin_banner'),

    #文档管理
    path('docs/',views.Doc_Manage.as_view(),name='docs'),
    #文档编辑
    path('docs/<int:d_id>/',views.Doc_edit.as_view(),name='doc_edit'),
    #文档发表
    path('docs/pub/',views.docs_pub.as_view(),name='doc_pub'),

    #课程管理
    path('course/',views.course_manage.as_view(),name='course_manage'),
    # 课程编辑
    path('course/<int:c_id>/', views.course_edit.as_view(), name='course_edit'),
    #课程发布
    path('course/pub/',views.course_pub.as_view(),name='course_pub'),

    #用户组管理
    path('groups/',views.g),
    #用户添加
    path('groups/add/',views.Group_Add.as_view(),name='group_add'),
    #用户编辑
    path('groups/<int:g_id>/',views.Group_edit.as_view(),name='g_edit'),
    #用户管理
    path('users/',views.User_manage,name='user_manage'),

    #用户编辑
    path('users/<int:u_id>/',views.User_edit.as_view(),name='user_edit')

]
