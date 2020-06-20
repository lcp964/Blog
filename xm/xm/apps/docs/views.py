from django.shortcuts import render,redirect
from django.views import View
from xm.utils.fiP.ip import blacks,func
from docs import models
import requests
# Create your views here.
#文档下载
def login_req(f):

    def func(request):
        if request.user.is_authenticated:
            return f(request)
        else:
            return redirect('/user/login/')
    return func
@blacks
@func
@login_req
def doc(request):
    docs=models.Doc.objects.only('title','image_url','docs').filter(is_delete=False)
    return render(request, 'doc/docDownload.html',context={'doc':docs})
from django import http
from xm.settings.ds import FILE_URL
from django.utils.encoding import escape_uri_path#处理格式方法
#文档下载
import requests
def ds(request,d_id):
        doc_file=models.Doc.objects.only('file_url').filter(is_delete=False,id=d_id).first()
        print(doc_file)
        if doc_file:
            doc_url=doc_file.file_url
            doc_url=FILE_URL+doc_url
            res=http.FileResponse(requests.get(doc_url,stream=True)) #分配下载方法
            ex_name=doc_url.split('.')[-1]
            if not ex_name:
                return http.Http404('文件异常')
            else:
                ex_name=ex_name.lower()
                if ex_name == 'pdf':
                    res['Content-type'] = 'application/pdf' #解码方式

                elif ex_name == 'doc':
                    res['Content-type'] = 'application/msword'  # 解码方式

                elif ex_name == 'ppt':
                    res['Content-type'] = 'application/powerpoint'

                else:
                    raise http.Http404('文件格式不正确')
                doc_filename=escape_uri_path(doc_url.split('/')[-1])
                # attachment  保存  inline 显示
                res["Content-Disposition"] = "attachment; filename*=UTF-8''{}".format(doc_filename)
                return res
        else:
            raise http.Http404('文档不存在')





