# 爬虫中所需要用到的公共函数

#将把二进制数据(bytes)转化成人看的懂得英文或者汉字，也就是unicode编码

def get_unicode(html):
    return html.decode("utf-8")