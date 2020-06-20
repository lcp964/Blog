
$(function () {
    let $login=$('.form-contain');//获取表单元素

    $login.submit(function (e) {
          e.preventDefault(); //阻止默认事件

    let sUsername=$('input[name=telephone]').val();//取手机号值
        if(sUsername ===''){
            message.showError('用户名不能为空');
            return
        }
        if(!(/^[\u4e00-\u9fa5\w]{5,20}$/).test(sUsername)) {
                // alert('请输入5-20位字符用户名')
                message.showError('请输入5-20位字符用户名');
                return
            }
           //密码验证
      let sPassword = $('input[name=password]').val();
             if(!sPassword){
                 message.showError('密码不能为空');
                 return
             }
             //验证密码长度

             if(sPassword.length<6 ||  sPassword.length>20)
             {
                 message.showError('请输入6到20位密码!');
                 return
             }
               //取标状态
        let status = $("input[type='checkbox']").is(':checked');//比对默认值 判断单选框是否被选中 判断选着标签呀

        //构造参数
        let sDate={
            'user_account':sUsername,//公司标准写法
            'password':sPassword,
            'remember':status
        };
        //发送ajax
        $.ajax({
            url : '/user/login/',
            type :'POST',
            data:JSON.stringify(sDate),
            contentType:'application/json; charset=utf-8',//不指定这个默认
            dataType:'json', //参数类型
        })
         //回调
         .done(function (res) {
                if(res.errno ==='0'){
                    message.showSuccess('贵宾登录成功!');
                    setTimeout(function () {
                        //跳转
                        window.location.href='/';
                    },1500)
                }else {
                    message.showError(res.errmsg)
                }
            })
            .fail(function () {
                message.showError('服务器超时请重试!')
            })
    })



});

