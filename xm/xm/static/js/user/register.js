$(function () {
 let $mobile = $('#mobile');
 let $username=$('#user_name');//获取用户地址
 let img_code_uuid='';//设置为空
 let isMobileFlag =false, //标记为flase
      isUserFlag=false,
      send_flag= true;

 let $img = $('.form-item .captcha-graph-img img');//#获取图像
         genre();//声明一个函数
         $img.click(genre);
          function genre() {
          img_code_uuid=generateUUID();
          // let imageCodeUrl = '/image_code/'+Math.floor(Math.random());
          let imageCodeUrl ='/user/'+'image_code/'+img_code_uuid+'/';
          $img.attr('src',imageCodeUrl) //attr拿到什么属性
         }

            // 生成图片UUID验证码
        function generateUUID() {
           let d = new Date().getTime();
          if (window.performance && typeof window.performance.now === "function") {
              d += performance.now(); //use high-precision timer if available
          }
        let uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
            let r = (d + Math.random() * 16) % 16 | 0;
               d = Math.floor(d / 16);
              return (c == 'x' ? r : (r & 0x3 | 0x8)).toString(16);
          });
          return uuid;
         }
        //用户名获取,blur是焦点事件
        $username.blur(fn_check_username);

        function fn_check_username() {
            isUsernameFlag=false;

        let sUsername = $username.val();
        // console.log(sUsername);
        if (sUsername === '') {
            message.showError('请输入您的用户名');
            return
            }
            if (!(/^[\u4e00-\u9fa5\w]{5,20}$/).test(sUsername)) {
                // alert('请输入5-20位字符用户名')
                message.showError('请输入5-20位字符用户名');
                return
            }
            $.ajax({
                url: '/username/' + sUsername + '/',
                type: 'GET',
                dataType: 'json',


                // success:function () {
                //    //回调
                // }

            })
            //回调
                .done(function (res) {
                    // console.log(res);
                    if (res.data.count !== 0) {
                        // alert('用户名已经注册，请重新输入')
                        message.showError('【' + res.data.username + '】' + '用户名已经注册，请重新输入')

                    }
                    else {
                        message.showSuccess('【' + res.data.username + '】' + '用户名可以能正常用');
                        isUsernameFlag = true;
                        send_flag= true;

                    }


                })
                //服务器异常
                .fail(function () {
                    message.showError('服务器超时，请重试!');

                })
        }

        //正则匹配，校验用户名是否合法


        //手机号验证
            $mobile.blur(fn_check_mobile);
            function fn_check_mobile() {
                isMobileFlag = false; //标记从这开始
                let sMobile = $mobile.val();
                if (sMobile === '') {
                    // alert('手机号不能为空！');
                    message.showError('手机号不能为空！');
                return
            }
        //用正则匹配校验手机号是否合格
        if (!(/^1[345789]\d{9}$/).test(sMobile)) {
            message.showError('手机号格式不对，请重新输入!');
            return
            // alert('手机号格式不对，请重新输入!')
        }
        $.ajax({
            url: '/mobiles/' + sMobile + '/',
            type: 'GET',
            dataType: 'json',
            async: false
        })
            .done(function (res) {
                if (res.data.count !== 0) {
                    message.showError('【' + res.data.mobile + '】' + '手机号已经注册,请重新输入！');


                    // alert('手机号已经注册,请重新输入！')
                } else {

                    message.showSuccess('【' + res.data.mobile + '】' + '手机号可以使用');
                    isMobileFlag = true ;//标记执行通过
                    send_flag= true;
                    // alert('手机号可以使用')
                }
            })
            .fail(function () {

                message.showError('服务器超时请重试！');

                // alert('服务器超时请重试！')
            });
        //短信验证
    }

           let $smsCodeBtn = $('.sms-captcha');
            //获取按钮验证
           let $imgCodeText= $('#input_captcha');//图形码


            $smsCodeBtn.click(function () {
               if(send_flag){
                    send_flag=false;

                if(!isMobileFlag){

                    fn_check_mobile();
                    return
                }
                //验证图形
                let text = $imgCodeText.val(); //拿到图形验证码的值
                if(!text){
                    message.showError('请输入图形验证码!');
                    return
                }
               if(!img_code_uuid){
                    message.showError('图形uuid为空');
                    return
               }
               //发送ajax
                //声明参数
                let DataParams={
                    'mobile':$mobile.val(),
                    'text':text,
                    'image_code_id': img_code_uuid,

                };
                $.ajax({
                    url:'/sms_code/',
                    type:'POST',
                    data:JSON.stringify(DataParams),//把后台传过来的视图转化为json字符串
                    // headers:{
                    //    'X-CSRFToken':getCookie('csrftoken')
                    // },
                    contentType:'application/json;charset=utf-8',
                    // 响应数据的格式（后端返回给前端的格式）
                    // 响应数据的格式（后端返回给前端的格式）
                    dataType:'json',
                })
                    .done(function (res) {
                        // console.log(res.errmsg);

                        if(res.errno==='0'){
                             message.showSuccess('短信验证码发送成功!');

                            //倒计时
                            let num = 60;
                            let t =setInterval(function () {
                                if(num === 1){
                                    //清楚定时器
                                    clearInterval(t);
                                    $smsCodeBtn.html('获取验证码');
                                    send_flag=true;

                                }else{
                                    num -= 1;
                                    //展示到时信息
                                    $smsCodeBtn.html(num+'秒');

                                }

                            },1000);

                        }else{
                            message.showError(res.errmsg);
                            send_flag=false;
                        }

                    })
                 .fail(function () {
                        message.showError('服务器超时请重试!')
               });


                }

     // 5、注册逻辑
                let $register = $('.form-contain');  // 获取注册表单元素

                $register.submit(function (e) {
                    // 阻止默认提交操作
                    e.preventDefault();

                    // 获取用户输入的内容
                    let sUsername = $username.val();  // 获取用户输入的用户名字符串
                    // alert(sUsername);

                    let sPassword = $("input[name=password]").val();
                    // console.log(sPassword);

                    let sPasswordRepeat = $("input[name=password_repeat]").val();
                    // console.log(sPassword);

                    let sMobile = $mobile.val();  // 获取用户输入的手机号码字符串
                    let sSmsCode = $("input[name=sms_captcha]").val();

                    // 判断用户名是否已注册
                    if (!isUsernameFlag) {
                        fn_check_username();

                        return
                    }

                    // 判断手机号是否为空，是否已注册
                    if (!isMobileFlag) {
                        fn_check_mobile();
                        return
                    }


                    // 判断用户输入的密码是否为空
                    if ((!sPassword) || (!sPasswordRepeat)) {
                        message.showError('密码或确认密码不能为空');
                        return
                    }

                    // const reg = /^(?![^A-Za-z]+$)(?![^0-9]+$)[\x21-x7e]{6,18}$/
                    // 以首字母开头，必须包含数字的6-18位
                    // 判断用户输入的密码和确认密码长度是否为6-20位
                    if (!(/^[0-9A-Za-z]{6,20}$/).test(sPassword)) {
                        message.showError('请输入6到20位密码');
                        return
                    }


                    // 判断用户输入的密码和确认密码是否一致
                    if (sPassword !== sPasswordRepeat) {
                        message.showError('密码和确认密码不一致');
                        return
                    }


                    // 判断用户输入的短信验证码是否为6位数字
                    if (!(/^\d{6}$/).test(sSmsCode)) {
                        message.showError('短信验证码格式不正确，必须为6位数字！');
                        return
                    }

                    // 发起注册请求
                    // 1、创建请求参数
                    let SdataParams = {
                        "username": sUsername,
                        "password": sPassword,
                        "password_repeat": sPasswordRepeat,
                        "mobile": sMobile,
                        "sms_code": sSmsCode
                    };

                    // alert(SdataParams);
                    // 2、创建ajax请求
                    $.ajax({
                        // 请求地址
                        url: "/user/register/",  // url尾部需要添加/
                        // 请求方式
                        type: "POST",
                        data: JSON.stringify(SdataParams),
                        // headers: {
                        //     // 根据后端开启的CSRFProtect保护，cookie字段名固定为X-CSRFToken
                        //     "X-CSRFToken": getCookie("csrftoken")
                        // },
                        // 请求内容的数据类型（前端发给后端的格式）
                        contentType: "application/json; charset=utf-8",
                        // 响应数据的格式（后端返回给前端的格式）
                        dataType: "json",

                    })
                        .done(function (res) {
                            if (res.errno === "0") {
                                // 注册成功
                                message.showSuccess('恭喜你，注册成功！');
                                setTimeout(() => {
                                    // 注册成功之后重定向到主页
                                    window.location.href = '/user/login/';
                                }, 1500)
                            } else {
                                // 注册失败，打印错误信息
                                message.showError(res.errmsg);
                            }
                        })
                        .fail(function(){
                            message.showError('服务器超时，请重试！');
                        });

                });


                //获取cookie
                        // get cookie using jQuery
                        function getCookie(name) {
                            let cookieValue = null;
                            if (document.cookie && document.cookie !== '') {
                                let cookies = document.cookie.split(';');
                                for (let i = 0; i < cookies.length; i++) {
                                    //trim去除字符串两端空白
                                    let cookie = jQuery.trim(cookies[i]);
                                    // Does this cookie string begin with the name we want?
                                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                                        console.log(cookieValue);
                                        break;
                                    }
                                }
                            }
                            return cookieValue;

                        }


                     });
        });







