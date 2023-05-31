import time
import requests
import json

class NewTime:

    def get_now_time(self):
        # 显示实时的时间戳
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


    def send_info(self):
        # while True:
        #     if self.get_now_time()
        # https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=41757ab9-1285-419d-9386-08372b258a85
        content = "高能已锁权限，可以开始烘焙了"
        data = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": ["v_chliangxu"],  # 被@的人
            }
        }
        header = {
            "Content-Type": "application/json"
        }

        # 发送企业微信消息
        requests.post("https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=41757ab9-1285-419d-9386-08372b258a85",
                      data=json.dumps(data), headers=header)

    def ko(self):
        print(type(self.get_now_time()))
        ret = json.loads(self.get_now_time())
        print(ret)
        return True
if __name__ == '__main__':
    print(NewTime().ko)

class mater:

    def __init__(self):
        self.regex = self.signed_regex

    @property
    def signed_regex(self) -> str:
        return f"-?{self.regex}"



class linsh(mater):

    regex = "15926811223"
    part_isolating = True


print(linsh())