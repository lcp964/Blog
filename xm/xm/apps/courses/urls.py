from django.urls import path
from .import views
app_name='video'
urlpatterns=[
path('course/',views.course,name='course'),
path('course/<int:c_id>/',views.courses,name='course_detail')

]
