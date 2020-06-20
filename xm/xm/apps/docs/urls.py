from django.urls import path
from .import views
app_name='doc'
urlpatterns=[

    path('docs/',views.doc,name='docs'),
    path('docs/<int:d_id>/',views.ds,name='download')


]