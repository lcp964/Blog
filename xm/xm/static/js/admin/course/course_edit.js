$(function () {

  let $thumbnailUrl = $("#news-thumbnail-url");   // 获取缩略图输入框元素
  let $courseFileUrl = $("#docs-file-url");    // 获取课程地址输入框元素

  // ================== 上传图片文件至服务器 ================
  let $upload_image_server = $("#upload-image-server");
  $upload_image_server.change(function () {
    // let _this = this;
    let file = this.files[0];   // 获取文件
    let oFormData = new FormData();  // 创建一个 FormData
    oFormData.append("images_file", file); // 把文件添加进去
    // 发送请求
    $.ajax({
      url: "/admin/news/images/",
      method: "POST",
      data: oFormData,
      processData: false,   // 定义文件的传输
      contentType: false,
    })
      .done(function (res) {
        if (res.errno === "0") {
          message.showSuccess("图片上传成功");
          let sImageUrl = res.data.image_url;
          $thumbnailUrl.val('');
          $thumbnailUrl.val(sImageUrl);

        } else {
          message.showError(res.errmsg)
        }
      })
      .fail(function () {
        message.showError('服务器超时，请重试！');
      });

  });
  // ================== 上传文件至服务器 ================
  let $upload_file_server = $("#upload-file-server");
  $upload_file_server.change(function () {
    // let _this = this;
    let file = this.files[0];   // 获取文件
    let oFormData = new FormData();  // 创建一个 FormData
    oFormData.append("text_file", file); // 把文件添加进去
    // 发送请求
    $.ajax({
      url: "/admin/news/images/",
      method: "POST",
      data: oFormData,
      processData: false,   // 定义文件的传输
      contentType: false,
    })
      .done(function (res) {
        if (res.errno === "0") {
          message.showSuccess("文件上传成功");
          let sTextFileUrl = res.data.text_url;
          $courseFileUrl.val('');
          $courseFileUrl.val(sTextFileUrl);

        } else {
          message.showError(res.errmsg)
        }
      })
      .fail(function () {
        message.showError('服务器超时，请重试！');
      });

  });


  // ================== 发布课程 ================
  let $docsBtn = $("#btn-pub-news");
  $docsBtn.click(function () {
    // 判断课程标题是否为空
    let sTitle = $("#news-title").val();  // 获取文件标题
    if (!sTitle) {
      message.showError('请填写课程标题！');
      return
    }

    // 判断课程简介是否为空
    let sDesc = $("#news-desc").val();  // 获取课程简介
    if (!sDesc) {
      message.showError('请填写课程描述！');
      return
    }

    // 判断课程缩略图url是否为空
    let sThumbnailUrl = $thumbnailUrl.val();
    if (!sThumbnailUrl) {
      message.showError('请上传课程缩略图');
      return
    }

    // 判断课程url是否为空
    let sCourseFileUrl = $courseFileUrl.val();
    if (!sCourseFileUrl) {
      message.showError('请上传视频或输入视频地址');
      return
    }

    // 判断视频时长是否为空
    let sCourseTime = $('#course-time').val();  // 获取视频时长
    if (!sCourseTime) {
      message.showError('请填写视频时长！');
      return
    }

    // 判断是否选择讲师
    let sTeacherId = $("#course-teacher").val();
    if (!sTeacherId || sTeacherId === '0') {
      message.showError('请选择讲师');
      return
    }

    // 判断是否选择课程分类
    let sCategoryId = $("#course-category").val();
    if (!sCategoryId || sCategoryId === '0') {
      message.showError('请选择课程分类');
      return
    }

    // // 判断课程大纲是否为空
    // let sContentHtml = window.editor.txt.html();
    // // let sContentText = window.editor.txt.text();
    // if (!sContentHtml || sContentHtml === '<p><br></p>') {
    //     message.showError('请填写课程大纲！');
    //     return
    // }

    // 获取coursesId 存在表示更新 不存在表示发表
    let coursesId = $(this).data("news-id");
    let url = coursesId ? '/admin/course/' + coursesId + '/' : '/admin/course/pub/';
    let data = {
      "title": sTitle,
      "profile": sDesc,
      "cover_url": sThumbnailUrl,
      "video_url": sCourseFileUrl,
      "duration": sCourseTime,
      "teacher": sTeacherId,
      "category": sCategoryId

    };

    $.ajax({
      // 请求地址
      url: url,
      // 请求方式
      type: coursesId ? 'PUT' : 'POST',
      data: JSON.stringify(data),
      // 请求内容的数据类型（前端发给后端的格式）
      contentType: "application/json; charset=utf-8",
      // 响应数据的格式（后端返回给前端的格式）
      dataType: "json",
    })
      .done(function (res) {
        if (res.errno === "0") {
          if (coursesId) {
            fAlert.alertNewsSuccessCallback("课程更新成功", '跳到课程管理页', function () {
              window.location.href = '/admin/course/'
            });

          } else {
            fAlert.alertNewsSuccessCallback("课程发表成功", '跳到课程管理页', function () {
              window.location.href = '/admin/course/'
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