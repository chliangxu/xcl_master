dic1 = {'id': 174019, 'TopTwo': '0.1', 'TopThree': '0.1.50', 'third': 50, 'fourth': 2050, 'version': '0.1.50.2050', 'tag': '0.1.50+0.1.50+0.1.50+2023-06-08', 'pipeline': 'http://devops.oa.com/console/pipeline/gngame/p-e64069e3298b43a980e81ea37e9b8a79/detail/b-11f0099b023742a9836a938e87de263d', 'appversion': '0.1.50.2050', 'BuildClass': 'ipa', 'CommitId': '17099_17154_79304_None', 'build_mode': 'Shipping', 'UpdaterChannelID': '1001596', 'PufferChannelId': '1003623', 'ASANENABLE': 'None'}
dic2 = {'id': 174011, 'TopTwo': '0.1', 'TopThree': '0.1.50', 'third': 50, 'fourth': 2050, 'version': '0.1.50.2050', 'tag': '0.1.50+0.1.50+0.1.50+2023-06-08', 'pipeline': 'http://devops.oa.com/console/pipeline/gngame/p-13357673f7d8421681f9ea42e4dab3d6/detail/b-54a0962d7b154579af2aa0a28512457e', 'appversion': '0.1.50.2050', 'BuildClass': 'apk', 'CommitId': '17099_17154_79304_None', 'build_mode': 'Shipping', 'UpdaterChannelID': '1001594', 'PufferChannelId': '1003622', 'ASANENABLE': 'None'}

dic_list= []
dic_list.append(dic1)
dic_list.append(dic2)
print(dic_list)
for i in dic_list:
    print(i)