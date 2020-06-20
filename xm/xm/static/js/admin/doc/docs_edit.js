$(function () {
    // 上传图片到服务器
    let $thumUrl = $('#news-thumbnail-url');   // 获取图片地址
    let $upload_image_server =$('#upload-image-server');  //获取图片按钮
    $upload_image_server.change(function () {
       alert('1');
        let file = this.files[0]; // 获取文件
        let oFormData = new FormData();
       // console.log(file);
        oFormData.append("images_file",file);
        // 发送请求
        $.ajax({
            url:'/admin/news/images/',
            method:"POST",
            data:oFormData,
            processData:false,
            contentType:false,
        })
            .done(function (res) {
                if (res.errno==='0'){
                    message.showSuccess('图片上传成功');
                    let sImageUrl = res['data']['image_url'];

                    $thumUrl.val(sImageUrl)

                }else {
                    message.showError(res.errmsg)
                }
            })
            .fail(function () {
                message.showError('服务器超时，请重试！！')
            })




});


    // 上传文件到服务器
    let $up_file_server = $('#upload-file-server');  // 获取文件按钮
    let $doc_file_url = $('#docs-file-url');   // 获取文件地址
    //console.log(doc_file_url)
    $up_file_server.change(function () {
         let file = this.files[0]; // 获取文件
         console.log(file);
        let oFormData = new FormData();
       // console.log(file);
        oFormData.append("text_file",file);
        // 发送请求
        $.ajax({
            url:'/admin/news/images/',
            method:"POST",
            data:oFormData,
            processData:false,
            contentType:false,
        })
            .done(function (res) {
                if (res.errno==='0'){
                    message.showSuccess('文档上传成功');
                    let sTextUrl = res.data.text_url;
                    $doc_file_url.val(sTextUrl)
                }else {
                    message.showError(res.errmsg)
                }
            })
            .fail(function () {
                message.showError('服务器超时，请重试！！')
            })




    });


    // 点击按钮实现保存
    let $docBtn = $('#btn-pub-news');
    $docBtn.click(function () {
        let doc_id = $(this).data('news-id');
       // alert(doc_id)
         // 判断文档标题是否为空
    let sTitle = $("#news-title").val();  // 获取文件标题
    if (!sTitle) {
        message.showError('请填写文档标题！');
        return
    }

    // 判断文档缩略图url是否为空
    let sThumbnailUrl = $thumUrl.val();
    if (!sThumbnailUrl) {
      message.showError('请上传文档缩略图');
      return
    }

    // 判断文档描述是否为空
    let sDesc = $("#news-desc").val();  // 获取文档描述
    if (!sDesc) {
        message.showError('请填写文档描述！');
        return
    }

    // 判断文档url是否为空
    let sDocFileUrl = $doc_file_url.val();
    if (!sDocFileUrl) {
      message.showError('请上传文档或输入文档地址');
      return
    }

    let url = doc_id ? '/admin/docs/' + doc_id + '/' : '/admin/docs/pub/';
    let data = {
      "title": sTitle,
      "docs": sDesc,
      "image_url": sThumbnailUrl,
      "file_url": sDocFileUrl,
    };

    $.ajax({
      // 请求地址
      url: url,
      // 请求方式
      type: doc_id ? 'PUT' : 'POST',
      data: JSON.stringify(data),
      // 请求内容的数据类型（前端发给后端的格式）
      contentType: "application/json; charset=utf-8",
      // 响应数据的格式（后端返回给前端的格式）
      dataType: "json",
    })
      .done(function (res) {
        if (res.errno === "0") {
          if (doc_id) {
            fAlert.alertNewsSuccessCallback("文档更新成功", '跳到文档管理页', function () {
              window.location.href = '/admin/docs/'
            });

          } else {
            fAlert.alertNewsSuccessCallback("文档发布成功", '跳到文档管理页', function () {
              window.location.href = '/admin/docs/'
            });
          }
        } else {
          fAlert.alertErrorToast(res.errmsg);
        }
      })
      .fail(function () {
        message.showError('服务器超时，请重试！');
      });

  });
 // get cookie using jQuery
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      let cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        let cookie = jQuery.trim(cookies[i]);
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  }

  // Setting the token on the AJAX request
  $.ajaxSetup({
    beforeSend: function (xhr, settings) {
      if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
  });


});
