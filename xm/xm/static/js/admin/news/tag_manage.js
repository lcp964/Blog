$( ()=> {

    //增加
    //拿添加按钮事件
    let $tagAdd=$('#btn-add-tag');
    $tagAdd.click(function () {
        fAlert.alertOneInput({
            title: '请输入文章标签',
            text: "长度限制在20字以内",
            placeholder: "请输入文章标签",
            confirmCallback: function confirmCallback(inputVal) {
                let sDataParams = {
                    "name": inputVal
                };
                $.ajax({
                    url:'/admin/tags/',
                    type :'POST',
                    data:JSON.stringify(sDataParams),
                    contentType:'application/json;charset=utf8',
                    dataType:'json',
                })
                .done(function (res) {
                        if(res.errno ==='0'){

                            fAlert.alertSuccessToast('分类添加成功');
                            setTimeout(function () {
                                window.location.reload()
                            },1000)

                        }
                        else {
                            swal.showInputError(res.errmsg);
                        }

                    })
                  .fail(function () {
                            message.showError('服务器超时请重试')
                        })
            }


        })


    });

    //修改

    let $tagedit=$('.btn-edit');

     //拿修改按钮事件
    $tagedit.click(function () {
    let _this = this;
    let sTagId = $(this).parents('tr').data('id');
    let sTagName = $(this).parents('tr').data('name');
         fAlert.alertOneInput({
             title:'编辑文章标签',
             text: "你在在编辑"+'【'+sTagName+'】'+'标签',
             placeholder:'请输入文章标签',
             value:sTagName,
              confirmCallback: function confirmCallback(inputVal) {
               if(inputVal===sTagName){
                   swal.showInputError('标签名称未变化');
                   return Flase
               }
               let sDataParams = {
                    "name": inputVal
                };



                $.ajax({
                    url:'/admin/tags/'+sTagId+'/',
                    type:"PUT",
                    data:JSON.stringify(sDataParams),
                    contentType:'application/json;charset:charset=utf8',
                    dataType:'json',
                })
                    .done(function (res) {
                        if(res.errno==='0'){
                            $(_this).parents('tr').find('td:nth-child(1)').text(inputVal);
                            swal.close();
                             message.showSuccess("标签修改成功");
                          setTimeout(function () {
                              window.location.reload()  //刷新页面
                          })
                        }
                        else {
                             swal.showInputError(res.errmsg);
                        }



                    })
                    .fail(function () {
                        message.showError('服务器超时请重试')
                    })
              }
         })

     });
      // get cookie using jQuery拿cookie值

    //删除标签
    let $tagdel=$('.btn-del');
    $tagdel.click(function () {
        let _this = this;
    let sTagId = $(this).parents('tr').data('id');
    let sTagName = $(this).parents('tr').data('name');
    fAlert.alertConfirm({
        title:'确定删除'+'【'+sTagName+'】'+'标签吗?',
        type:'error',
        confirmText: "确认删除",
        cancelText: "取消删除",
        confirmCallback: function confirmCallback() {

        $.ajax({
          // 请求地址
          url: "/admin/tags/" + sTagId + "/",  // url尾部需要添加/
          // 请求方式
          type: "DELETE",
          dataType: "json",
        })
          .done(function (res) {
            if (res.errno === "0") {
              // 更新标签成功
              message.showSuccess("标签删除成功");
              setTimeout(function () {
                  window.location.reload()
              });
              $(_this).parents('tr').remove();
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