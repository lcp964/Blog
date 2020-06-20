$( () =>{
   let $course_data=$('.course-data');
   let sImageurl=$course_data.data('cover-url') ;//取值
   let sVideourl=$course_data.data('video-url') ;
   let player = cyberplayer("course-video").setup({   //触发播放标签
    width: '100%',
    height: 700,
    file: sVideourl,
    image: sImageurl,
    autostart: false, //关闭自动播放
    stretching: "uniform",
    repeat: false,
    volume: 100,
    controls: true,
    ak: 'e838a7756a8145a5ab0af4e6371e797c'
  });










});