# 爬虫实现urllib2实现GET请求
import urllib
# 调用parse模块的urlencode()进行编码
from urllib.parse import urlencode
# 打开链接
import urllib.request as urllib_url
from reptile import public_function

from bs4 import BeautifulSoup
import codecs


def get_contents(word):
    # 前半部分的链接(注意是http，不是https)
    url_pre = 'http://www.baidu.com/s'

    # GET参数
    params = {}
    params['pn'] = 20  # 设置这个每页可以获取10个内容

    # 若是unicode编码，转成byte
    if isinstance(word, bytes):
        params['wd'] = word.encode('utf-8')
    url_params = urlencode(params)

    # GET请求完整链接
    url = '%s?%s' % (url_pre, url_params)
    print("url", url)
    # 打开链接，获取响应
    request = urllib_url.Request(url)
    response = urllib_url.urlopen(request)

    # 获取响应的html
    html = response.read()
    print("html", html)

    # 解析内容
    soup = BeautifulSoup(html, 'lxml')
    items = soup.select('.t a')
    print("sdfaf",items)
    # 写入文件
    f = codecs.open('test.txt', 'w', 'utf-8')
    for item in items:
        f.write('%s\r\n' % ''.join(item.stripped_strings))
        f.write('%s\r\n\r\n' % item['href'])
    f.close()


if __name__ == '__main__':
    get_contents(u'测试')


# 对url地址进行编码的意义
# https://blog.csdn.net/Itmastergo/article/details/128492021