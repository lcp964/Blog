$(function() {

    let sdk = baidubce.sdk; //拿到客户端
    let VodClient = sdk.VodClient; //调用客户端

    let config = {
        endpoint: 'http://vod.bj.baidubce.com', //加载配置
        credentials: {
            ak: 'e838a7756a8145a5ab0af4e6371e797c',
            sk: '784863ffe474460a9ca15548ddfb2fdb'
        }
    };

          let client = new VodClient(config);
          let $file=$('.up'); //拿到UP文件
          $file.change(function () {  //定义一个视频迁移文件
              let video_file = this.files[0]; //拿到视频文件
              console.log(video_file);
              let title='步兵测试';
              let desc='这是一个视频';
              let video_type=video_file.type;
              let data=new Blob([video_file],{type:video_type}); //这个是文件对象
              client.createMediaResource(title, desc, data)
    // Node.js中<data>可以为一个Stream、<pathToFile>；在浏览器中<data>为一个Blob对象
    .then(function (response) {
        // 上传完成
        console.log(response.body.mediaId);
        console.log(video_type);
        // http://kdrdxb00kexev9wg66j.exp.bcevod.com/mda-kdrmnfm9fwfnax3q/mda-kdrmnfm9fwfnax3q.m3u8
        // http://kdrdxb00kexev9wg66j.exp.bcevod.com/mda-kdrmnfm9fwfnax3q/mda-kdrmnfm9fwfnax3q.m3u8
        let ym ='kdrdxb00kexev9wg66j.exp.bcevod.com';
        let os =response.body.mediaId;
        let url='http://'+ym+'/'+os+'/'+os+'.m3u8';
        console.log(url)
    })
    .catch(function (error) {
        console.log(error);
        // 上传错误
//监听progress事件 获取上传进度
client.on('progress', function (evt) {
    console.log(evt);
    });

          });
});
});