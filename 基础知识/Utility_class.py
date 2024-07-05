import os
import shutil
import time


class UTILITYCLASSNODE:
    """
    存放一些实用的小工具
    1.进度条
    """

    # 1.进度条
    def progress_bar(self):
        t = 60
        print("**************带时间的进度条**************")
        start = time.perf_counter()
        for i in range(t + 1):
            finsh = "▓" * i
            need_do = "-" * (t - i)
            progress = (i / t) * 100
            dur = time.perf_counter() - start
            print("\r{:^3.0f}%[{}->{}]{:.2f}s".format(progress, finsh, need_do, dur), end="")
            time.sleep(0.05)



if __name__ == '__main__':
    start_Node = UTILITYCLASSNODE()
    start_Node.progress_bar()



# 从流水线上获取数据所需的token
class All_parameter:

    def __init__(self):
        self.bk_app_code = "gngame-new"
        self.bk_app_secret = "djf4tgGCTYrclQQmNAEZWpnXUfx4leeY43Mb"
        self.projectId = "gngame"
        self.user_id = "v_chliangxu"
        self.refresh_token = "mDBmnlzSs6e2KmwKoteoqXhGYooHkM"
        self.access_token = "MKg5NcVmliYgpmjUFizJU4ePF7m9PI"
        self.bk_tickets = "3a-311ZNGtrAhcx_Qa0-3KQPasQckWxVq8RbKJnektU"


# 刷新access_token
def refresh_access_token():
    url = 'http://apigw.o.oa.com/auth_api/refresh_token/'
    app_code = All_parameter().bk_app_code
    print("app", app_code)
    refresh_token = All_parameter().refresh_token
    print("refresh_token", refresh_token)
    env_name = "test"
    grant_type = "refresh_token"
    data = {"app_code": app_code, "refresh_token": refresh_token, "env_name": env_name, "grant_type": grant_type}
    print(type(data))
    response = requests.get(url, params=data)
    log.info("response", response)

    if response.status_code == 200:
        print("-------")
        response_data = json.loads(response.text)
        data = response_data
        log.info("data", data)


def get_access_token():
    import requests

    ret = requests.post(
        'http://apigw.o.oa.com/auth_api/token/',
        data={
            'app_code': 'gngame-new',
            'app_secret': 'djf4tgGCTYrclQQmNAEZWpnXUfx4leeY43Mb',
            'env_name': 'prod',
            'grant_type': 'authorization_code',
            'rtx': 'v_chliangxu',
            'bk_ticket': '3a-311ZNGtrAhcx_Qa0-3ImjFddRgYbW2ABu54iHZEU'
        }
    )
    print(ret, ret)
    response_data = json.loads(ret.text)
    data = response_data
    log.info("data", data)
