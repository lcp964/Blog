$( () => {
    //编辑
    let $Hotedit=$('.btn-edit');
    $Hotedit.click(function () {
    let _this = this;
        let sHotNewsId = $(this).parents('tr').data('id');
        let sPriority = $(this).data('priority');
        fAlert.alertOneInput({
            title: "编辑热门文章优先级",
            text: "你正在编辑热门文章的优先级",
            placeholder: "请输入文章优先级",
            value: sPriority,
            confirmCallback: function confirmCallback(inputVal) {
                if (!inputVal.trim()) {
                    swal.showInputError('输入框不能为空！');
                    return false;
                } else if (inputVal === sPriority) {
                    swal.showInputError('优先级未修改');
                    return false;
                } else if(parseInt(inputVal)>3){
                swal.showInputError('优先级只能取1，2，3中的一个');
                return False
                }

                // } else if (!$.inArray(parseInt(inputVal), ['1', '2', '3'])){
                //   swal.showInputError('优先级只能取1，2，3中的一个');
                //    return false;

        let sDataParams = {
          "priority": inputVal
        };

        $.ajax({
          // 请求地址
          url: "/admin/hot/" + sHotNewsId + "/",  // url尾部需要添加/
          // 请求方式
          type: "PUT",
          data: JSON.stringify(sDataParams),
          // 请求内容的数据类型（前端发给后端的格式）
          contentType: "application/json; charset=utf-8",
          // 响应数据的格式（后端返回给前端的格式）
          dataType: "json",
        })
          .done(function (res) {
            if (res.errno === "0") {
              swal.close();
              message.showSuccess("标签修改成功");
              // $(_this).parents('tr').find('td:nth-child(3)').text(inputVal);

              setTimeout(function () {
                window.location.href = '/admin/hot/';
              }, 800)
            } else {
              swal.showInputError(res.errmsg);
            }
          })

          .fail(function () {
            message.showError('服务器超时，请重试！');
          });

      }
});
});

    //删除
    let $Hotdel=$('.btn-del');
    $Hotdel.click(function () {
        let _this=this;
        let hotnews_id=$(this).parents('tr').data('id');
        fAlert.alertConfirm({
          title: "确定删除热门文章吗？",
          type: "error",
          confirmText: "确认删除",
          cancelText: "取消删除",
          confirmCallback: function confirmCallback() {
               $.ajax({
                   url:'/admin/hot/'+hotnews_id+'/',
                   type:'DELETE',
                   dataType:'json',
               });
                   alert(8888)
               .done(function (res) {
                       if(res ==='0'){
                          message.showSuccess("删除热门文章成功");
                          swal.close();
                          $(_this).parents('tr').remove();
                          setTimeout(function () {
                              window.location.reload()
                     },1000)

                       }
                        else {
                            swal.showInputError(res.errmsg);
                       }
                   })
                     .fail(function () {
                     message.showError('服务器超时，请重试！');
          });

          }

    })
});







//拿cookie
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