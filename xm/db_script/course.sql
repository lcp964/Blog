
INSERT INTO tb_teachers VALUES (1,now(),now(),0,'龙龙','爬虫开发工程师','向前冲','/media/avatar.jpeg');
INSERT INTO tb_teachers VALUES (2,now(),now(),0,'花开','web开发工程师','向前大冲','/media/avatar.jpeg');


INSERT INTO tb_course_category (name,create_time,update_time,is_delete) VALUES
('日韩',now(),now(),0),
('欧美',now(),now(),0),
('国剧',now(),now(),0);




INSERT INTO tb_course(title, cover_url, video_url,profile, outline, teacher_id, category_id, create_time, update_time, is_delete) VALUES
('告白气球','http://kdrdxb00kexev9wg66j.exp.bcevod.com/mda-kdrmkh7bw0vfavr8/mda-kdrmkh7bw0vfavr8.jpg','http://kdrdxb00kexev9wg66j.exp.bcevod.com/mda-kdrmkh7bw0vfavr8/mda-kdrmkh7bw0vfavr8.m3u8','武将上下而求索','爱情故事',1,3,now(),now(),0),
('告白气球2','http://kdrdxb00kexev9wg66j.exp.bcevod.com/mda-kdrmnfm9fwfnax3q/mda-kdrmnfm9fwfnax3q.jpg','http://kdrdxb00kexev9wg66j.exp.bcevod.com/mda-kdrmnfm9fwfnax3q/mda-kdrmnfm9fwfnax3q.m3u8','五漫漫其修远矣','爱情故事',1,3,now(),now(),0);





