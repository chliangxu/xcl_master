import json
import requests
#
class All_parameter:

    def __init__(self):
        self.bk_app_code = "gngame-new"
        self.bk_app_secret = "djf4tgGCTYrclQQmNAEZWpnXUfx4leeY43Mb"
        self.projectId = "gngame"
        self.user_id = "v_chliangxu"
        # self.refresh_token = "OjvYexPqfJ3MMt8NNpdhYpgt8FhP1q"
        self.refresh_token = "rSb1b5GBUiYgkjlkOUjkHFVsS9me8K"
        self.access_token = "VEg5rMSUhfHLiil1zvHNbUppwg5axm"
        # self.access_token = "6ue1f4rMM4DoytJfcSrjMJsY65kWI2"
        self.bk_tickets = "3a-311ZNGtrAhcx_Qa0-3KQPasQckWxVq8RbKJnektU"

def get_header():
    all_parameter = All_parameter()
    bk_app_code = all_parameter.bk_app_code
    bk_app_secret = all_parameter.bk_app_secret
    access_token = all_parameter.access_token
    bk_username = all_parameter.user_id
    x_bkapi_authorization = {"bk_app_code": bk_app_code,
                             "bk_app_secret": bk_app_secret,
                             "access_token": access_token, "bk_username": bk_username}
    headers = {'content-type': 'application/json',
               'X-DEVOPS-UID': '{X-DEVOPS-UID}',
               'X-Bkapi-Authorization': json.dumps(x_bkapi_authorization)
               }
    return headers
# 刷新access_token
def refresh_access_token():
    # url = 'http://apigw.o.oa.com/auth_api/refresh_token/'
    # app_code = All_parameter().bk_app_code
    # print("app", app_code)
    # refresh_token = All_parameter().refresh_token
    # print("refresh_token", refresh_token)
    # env_name = "test"
    # grant_type = "refresh_token"
    # data = {"app_code": app_code, "refresh_token": refresh_token, "env_name": env_name, "grant_type": grant_type}
    # print(type(data))
    # response = requests.get(url, params=data)
    # print("response", response)
    #
    # if response.status_code == 200:
    #     print("-------")
    #     response_data = json.loads(response.text)
    #     data = response_data
    #     print("data", data)
    ret = requests.get(
        'http://apigw.o.oa.com/auth_api/refresh_token/',
        params={
            'app_code': 'get-build-links',
            'refresh_token': All_parameter().refresh_token,
            'env_name': 'test',
            'grant_type': 'refresh_token'
        }
    )
    ret_json = ret.json()
    print("123", ret_json)
    # print(ret_json)
    accessToken = ret_json['data']['access_token']
    print(accessToken)

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
            # 失败时看一下bk_ticket
            'bk_ticket': '3a-311ZNGtrAhcx_Qa0-3DxLXQtBBYE4iW-qg393w5s'
        }
    )
    print(ret, ret)
    response_data = json.loads(ret.text)
    data = response_data
    print("data", data)

refresh_access_token()