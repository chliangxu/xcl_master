#
# # def set_access_token():
# #     ret = requests.get(
# #         'http://apigw.o.oa.com/auth_api/check_token/',
# #         params={
# #             'access_token': 'XnXfvRE62m7l4eWvSNfRaWG9sAPk9H',
# #         }
# #     )
# #     ret_json = ret.json()
# #     return ret_json['data']
# #
# #
# # print(set_access_token())
#
# import requests
#
# def set_access_token_old():
#     ret = requests.post(
#         'http://apigw.o.oa.com/auth_api/token/',
#         data={
#             'app_code': 'test',
#             'app_secret': 'xxx',
#             'env_name': 'prod',
#             'grant_type': 'authorization_code',
#             'rtx=xxx': 'yyy',
#             'bk_ticket': 'zzz'
#         }
#     )
#     ret_json = ret.json()
#     return ret_json['data']
#
#
# set_access_token_old()
# for i in range(1, 101):
#     print(i)

