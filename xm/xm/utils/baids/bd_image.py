from baidubce.bce_client_configuration import BceClientConfiguration
from baidubce.auth.bce_credentials import BceCredentials
from baidubce.services.bos.bos_client import BosClient
# 设置BosClient的Host，Access Key ID和Secret Access Key
class Bd_Storage(object):
    def __init__(self):
        self.bos_host = "bj.bcebos.com"
        self.access_key_id = "e838a7756a8145a5ab0af4e6371e797c"
        self.secret_access_key = "784863ffe474460a9ca15548ddfb2fdb"
        # 空间名
        self.back_name = '888888888888'

    def up_image(self, file):
            # 公共权限目录
            # 创建BceClientConfiguration
            config = BceClientConfiguration(credentials=BceCredentials(self.access_key_id, self.secret_access_key),
                                            endpoint=self.bos_host)
            # 传值实例化对象
            client = BosClient(config)
            self.key_name = '123.jpg'
            try:
             res = client.put_object_from_string(bucket=self.back_name, key=self.key_name, data=file)
            except Exception as e:
                return None
            else:
              # 上传二进制方法
              result=res.__dict__
              if result['metadata']:

                  url='https://' + self.back_name + '.bj.bcebos.com/' + self.key_name
                  print('图片上传成功')
                  return url



if __name__ == '__main__':
   bd=Bd_Storage()
   with open('123.png', 'rb')as f:
       s = f.read()
       bd.up_image(s)



