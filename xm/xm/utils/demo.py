# import requests
# import json
#
# url='http://longlong.com:8080/user/register/'
# r=requests.post(url,data=json.dumps({
#     'username':13333333333,
#     'password':13444444,
#     'password_repeat':13444444,
#     'mobile':13333333333,
#     'sms_code':444444,
# }))
# print(r.status_code)


# import requests
# import json
# import time

# url='http://127.0.0.1:8080/user/login/'
# r=requests.post(url,data=json.dumps({
# "user_account":"longlong",
# "password'":'123456',
# "remember'":False
# }))

#
# url='http://longlong.com:8080/media/流畅的Python.pdf/'
# # s_time=time.time() #开始时间
# # for i in range(50):
# res=requests.get(url,timeout=1,stream=True) #timeout超过一秒种就停止
# print(res)
#     # e_time=time.time() #结束时间
#     # print(f'time:{e_time-s_time}')
# with open('baids/aaa.pdf','wb')as f:
#     for i in res.iter_content(chunk_size=8*1024*1024):
#         if i:
#          f.write(i)


