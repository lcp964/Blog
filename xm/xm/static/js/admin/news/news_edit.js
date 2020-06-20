
$( ()  =>{
    //文件上传
    let $up_to_server=$('#upload-news-thumbnail');
    let $img=$('#news-thumbnail-url');
    $up_to_server.change(function () {
        let file = this.files[0]; //获取当前里面的文件
         let sFormData = new FormData(); //new一个对象把数据添加到里面去
         sFormData.append('images_file',file);
         $.ajax({
        url:'/admin/news/images/',
        method:'POST',  //请求方法o
        data:sFormData,
        processData:false, //是否异步
        contentType:false ,//响应类型
    })
        .done(function (res) {
            if(res.errno==='0'){
            message.showSuccess(res.errmsg);
            let sImgurl=res['data']['image_url'];//拿后台响应的value值
            $img.val(sImgurl) //拿value值
            }
            else {
                message.showError(res.errmsg)
            }


        })
             .fail(function () {
                 message.showError('服务器超时请重试')
             });

    });

   let $newsBtn = $("#btn-pub-news");
  $newsBtn.click(function () {

    // 判断文章标题是否为空
    let sTitle = $("#news-title").val();  // 获取文章标题
    if (!sTitle) {
        message.showError('请填写文章标题！');
        return
    }
    // 判断文章摘要是否为空
    let sDesc = $("#news-desc").val();  // 获取文章摘要
    if (!sDesc) {
        message.showError('请填写文章摘要！');
        return
    }

    let sTagId = $("#news-category").val();
    if (!sTagId || sTagId === '0') {
      message.showError('请选择文章标签');
      return
    }

    let sThumbnailUrl = $img.val();
    if (!sThumbnailUrl) {
      message.showError('请上传文章缩略图');
      return
    }
    let sContentHtml = $(".markdown-body").html();
    console.log(sContentHtml);
    // let sContentHtml = $("#content").val();
    if (!sContentHtml || sContentHtml === '<p><br></p>') {
        message.showError('请填写文章内容！');
        return
    }
 // 获取news_id 存在表示更新 不存在表示发表
    let newsId = $(this).data("news-id");
    let url = newsId ? '/admin/news/' + newsId + '/' : '/admin/news/pub/';


    let data = {
      "title": sTitle,
      "digest": sDesc,
      "tag": sTagId,
      "image_url": sThumbnailUrl,
      "content": sContentHtml,
    };

    $.ajax({
      // 请求地址
      url: url,
      // 请求方式
      type: newsId ? 'PUT' : 'POST',
      data: JSON.stringify(data),
      // 请求内容的数据类型（前端发给后端的格式）
      contentType: "application/json; charset=utf-8",
      // 响应数据的格式（后端返回给前端的格式）
      dataType: "json",
    })
      .done(function (res) {
        if (res.errno === "0") {
          if (newsId) {
              message.showSuccess("文章更新成功");
              setTimeout(function () {
                window.location.href='/admin/news/';
                }, 1000)

          } else {
              message.showSuccess("文章添加成功");
              setTimeout(function () {
                window.location.reload();
                }, 1000)
          }

        } else {
          fAlert.alertErrorToast(res.errmsg);
        }
      })
      .fail(function () {
        message.showError('服务器超时，请重试！');
      });
  });


});