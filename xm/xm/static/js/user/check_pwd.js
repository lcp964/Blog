$(function () {
    let $check=$('.form-contain');//获取表单元素

    $check.submit(function (e) {
          e.preventDefault(); //阻止默认事件

        let sUsername=$('input[name=telphone]').val();//取手机号值
        if(sUsername ===''){
       message.showError('账号不能为空');
            return
        }
        if(!(/^[\u4e00-\u9fa5\w]{5,20}$/).test(sUsername)) {
                // alert('请输入5-20位字符用户名')
            message.showError('请输入5-20位字符账号');
                return
            }
           //密码验证
      let sPassword = $('input[name=old_password]').val();
             if(!sPassword){
                 message.showError('旧密码不能为空');
                 return
             }
             //验证密码长度

             if(sPassword.length<6 ||  sPassword.length>20)
             {
                 message.showError('请输入6到20位旧密码!');

                 return
             }
             let sPassword1 = $('input[name=new_password]').val();
             if(!sPassword1){
                 message.showError('新密码不能为空');
                 return
             }
             //验证密码长度

             if(sPassword1.length<6 ||  sPassword.length>20)
             {
                 message.showError('请输入6到20位新密码!');
                 return
             }
             if(sPassword === sPassword1){
                message.showError('新密码与旧密码不能一致');
                 return
             }
             let sPassword2 = $('input[name=new1_password]').val();
             if(!sPassword2){
                 message.showError('确认密码不能为空');
                 return
             }
             //验证密码长度

             if(sPassword2.length<6 ||  sPassword.length>20)
             {
                 message.showError('请输入6到20位确认密码!');
                 return
             }
             if(sPassword1 !== sPassword2){
                 message.showError('新密码与确认密码不一致');
                 return
             }


        //构造参数
        let sData={
            'user_account':sUsername,//公司标准写法
            'old_password':sPassword,
            'new_password':sPassword1,
            'check_password':sPassword2,

        };
        //发送ajax
        $.ajax({
            url : '/user/check/',
            type :'POST',
            data:JSON.stringify(sData),
            contentType:'application/json; charset=utf-8',//不指定这个默认
            dataType:'json', //参数类型
        })
         //回调
         .done(function (res) {
                if(res.errno ==='0'){
                    message.showSuccess('密码修改成功');
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

