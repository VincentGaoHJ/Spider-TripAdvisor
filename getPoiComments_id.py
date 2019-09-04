# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/9/3
@Author: Haojun Gao
@Description: 
"""

import threading
from paras import header_useragent
from urllib import request
from random import choice
from html.parser import HTMLParser
from proxy_github import getProxy


# 继承父类 threading.Thread
class myThread(threading.Thread):
    def __init__(self, threadID, name, counter, url, ip):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.url = url
        self.ip = ip

    # 把要执行的代码写到 run 函数里面 线程在创建后会直接运行 run 函数
    def run(self):
        print("Starting " + self.name)
        links = get(self.url, self.ip)
        print("Exiting " + self.name)
        self.result = links

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def multi_threading(post_url_pool, ip_list):
    threads = []
    thread_num = len(post_url_pool)
    nloops = range(thread_num)

    for i in nloops:
        t = myThread(i, "Thread-" + str(i), i, post_url_pool[i], ip_list[i])
        threads.append(t)

    for i in nloops:  # start threads 此处并不会执行线程，而是将任务分发到每个线程，同步线程。等同步完成后再开始执行start方法
        threads[i].start()

    for i in nloops:  # jion()方法等待线程完成
        threads[i].join()

    return threads


def get(post_url, ip):
    param = {}
    opener, req = prepare_request(param, ip, post_url)
    response = opener.open(req, timeout=20)
    res_text = response.read().decode('utf-8')
    hp = MyHTMLParser()
    hp.feed(res_text)
    hp.close()
    links = hp.links
    return links


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


def prepare_request(paras, ip, post_url):
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
    proxy_handler = request.ProxyHandler(ip)
    opener = request.build_opener(proxy_handler)
    return opener, req


def getPoiComments_id(base_url, ip_list):
    origin = "https://cn.tripadvisor.com"
    base_sec = base_url.split("Reviews")

    param = {}
    page = 1
    comments_id = []

    page_num = 60
    threading_num = len(ip_list)
    post_url_pool = []
    while page <= page_num:
        num = (page - 1) * 10
        post_url = origin + base_sec[0] + "-Reviews-or" + str(num) + base_sec[0]
        if len(post_url_pool) < threading_num and page != page_num:
            print("准备爬从第 {} 页开始的评论".format(page))
            post_url_pool.append(post_url)
            page += 1
            continue

        # 最后一页既要进url池，又要启动线程
        if page == page_num:
            print("准备爬从第 {} 页开始的评论".format(page))
            post_url_pool.append(post_url)

        threads = multi_threading(post_url_pool, ip_list)

        for thread in threads:
            result = thread.get_result()
            print(result)
            try:
                if len(result) == 0:
                    return comments_id
            except Exception as e:
                print("[Get_List]Error ", e)
                continue
            comments_id.extend(result)
            print(len(comments_id))
            print("已经爬到了 {} 个的评论".format(len(comments_id)))

        # 准备下一次输送给线程的url
        if page != page_num:
            print("准备爬从第 {} 页开始的评论".format(page))
            post_url_pool = [origin + base_sec[0] + "-Reviews-or" + str(num) + base_sec[0]]

        page += 1

    return comments_id


if __name__ == '__main__':
    base_url = "/Attraction_Review-g60763-d1687489-Reviews-The_National_9_11_Memorial_Museum-New_York_City_New_York.html	"
    ip_list = getProxy(10)
    print("[Get_List]The valid IP: ", ip_list)
    links = getPoiComments_id(base_url, ip_list)
    print(len(links))
    for item in links:
        print(item)
