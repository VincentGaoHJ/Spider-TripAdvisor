# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/9/3
@Author: Haojun Gao
@Description: 
"""

from random import choice
from proxy_github import getProxy
from urllib import request, parse
from html.parser import HTMLParser
from paras import header_useragent


class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        # print "Encountered the beginning of a %s tag" % tag
        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                # print('====')
                for (variable, value) in attrs:
                    # print(variable, value)
                    if variable == "href":
                        if 'ShowUserReviews' in value:
                            if value not in self.links:
                                self.links.append(value)


def prepare_request(paras, ip_list, post_url):
    """
    构建完整的请求内容，其中包括参数，headers和代理IP
    :param paras: 请求参数
    :param ip_list: 可用的代理IP
    :return: opener, req
    """
    # 构建req
    # paras = parse.urlencode(paras)
    # paras = paras.encode('utf-8')
    # headers = {'User-Agent':ua.random}
    headers, user_agent = header_useragent()
    headers['User-Agent'] = choice(user_agent)
    # req = request.Request(post_url, paras, headers=headers)
    req = request.Request(post_url, headers=headers)

    # 构建opener
    # 基本的urlopen()方法不支持代理、cookie等其他的HTTP/HTTPS高级功能
    # 需要通过urllib2.build_opener()方法来使用这些处理器对象
    proxy_handler = request.ProxyHandler(choice(ip_list))
    opener = request.build_opener(proxy_handler)
    return opener, req


def getPoiComments_id(base_url, ip_list):
    origin = "https://cn.tripadvisor.com"
    base_sec = base_url.split("Reviews")

    param = {}
    page = 1
    comments_id = []

    while page < 2:
        num = (page - 1) * 10
        post_url = origin + base_sec[0] + "-Reviews-or" + str(num) + base_sec[0]
        opener, req = prepare_request(param, ip_list, post_url)
        response = opener.open(req)
        res_text = response.read().decode('utf-8')
        hp = MyHTMLParser()
        hp.feed(res_text)
        hp.close()
        print(hp.links)
        if len(hp.links) == 0:
            break
        comments_id.extend(hp.links)
        print(len(comments_id))
        page += 1

    return comments_id


if __name__ == '__main__':
    base_url = "/Attraction_Review-g60763-d1687489-Reviews-The_National_9_11_Memorial_Museum-New_York_City_New_York.html	"
    ip_list = getProxy()
    print("[Get_List]The valid IP: ", ip_list)
    links = getPoiComments_id(base_url, ip_list)
    print(len(links))
    for item in links:
        print(item)
