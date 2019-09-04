# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/9/3
@Author: Haojun Gao
@Description:
"""

import os
import sys
import csv
import copy
import threading
import requests
from random import choice
from proxy_github import getProxy
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    text_title = False
    text_content = False

    def __init__(self):
        HTMLParser.__init__(self)
        self.title = ''
        self.content = ''

    def handle_starttag(self, tag, attr):
        if tag == 'h1':
            if dict(attr)["class"] == "title":
                self.text_title = True
        if tag == 'span':
            if dict(attr)["class"] == "fullText ":
                self.text_content = True

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.text_title = False
        if tag == 'span':
            self.text_content = False

    def handle_data(self, data):
        if self.text_title:
            self.title = data
        if self.text_content:
            self.content = data


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
        title, content = get(self.url, self.ip)
        print("Exiting " + self.name)
        self.result = (title, content)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None


def get(post_url, ip):
    response = requests.get(post_url, proxies=ip, timeout=20)
    html_code = response.text
    hp = MyHTMLParser()
    hp.feed(html_code)
    hp.close()
    title = hp.title
    content = hp.content
    return title, content


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


def csv_last_line(input_file):
    """"
    读取CSV文件的最后一行
    :param input_file: 文件名
    :return: last_line
    """
    last_line = []
    with open(input_file, "r", newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            if line is not "":
                last_line = line

    return last_line


def get_list(input_file):
    """
    读取文件，将每一行的元素保存成元组放入列表
    :param input_file: 文件路径
    :return: list_loc
    """
    list_loc = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            list = line.strip().split(",")
            list_loc.append((list[0], list[1], list[2], list[3]))
    return list_loc


def get_starter(init_file_path, file_path):
    """
    :param init_file_path: 景点信息所在文件路径
    :param file_path: 景点评论信息所在文件路径
    :return:
    """
    if os.access(init_file_path, os.F_OK):
        print("[Get_Comments]Basic file is exist.")
    else:
        print("[Get_Comments]Basic file is not exist, please run getList.py first.")
        sys.exit(0)

    list_loc = get_list(init_file_path)

    if os.access(file_path, os.F_OK):
        print("[Get_Comments]Given file path is exist.")
        last_line_list = csv_last_line(file_path)
        comment_id = last_line_list[2]
        print("[Continue]Already Spider Comment :", comment_id)

        list_loc_copy = copy.deepcopy(list_loc)
        for poi in list_loc_copy:
            if poi[2] != comment_id:
                list_loc.remove(poi)
            else:
                list_loc.remove(poi)
                break
    else:
        print("[Get_Comments]Start Collecting Comments")

    return list_loc


def get_comments(initFilePath, filePath):
    list_loc = get_starter(initFilePath, filePath)
    total_number = len(list_loc)

    ip_list = getProxy(10)

    url_base = "https://cn.tripadvisor.com/OverlayWidgetAjax?Mode=EXPANDED_SUR_REVIEWS_RESP&metaReferer=ShowUserReviewsAttractions&reviewId="

    # for i in range(total_number):
    #     with open(filePath, 'a+', newline='', encoding='utf-8-sig') as csvfile:
    #         writer = csv.writer(csvfile)
    #         url = url_base + list_loc[i][2][1:]
    #         response = requests.get(url, proxies=proxies)
    #         html_code = response.text
    #         hp = MyHTMLParser()
    #         hp.feed(html_code)
    #         hp.close()
    #         title = hp.title
    #         content = hp.content
    #         print("title: {}".format(title))
    #         print("content: {}".format(content))
    #         writer.writerow([list_loc[i][0], list_loc[i][1], list_loc[i][2], title, content])

    threading_num = len(ip_list)
    post_url_pool = []
    infor_pool = []
    for i in range(total_number):
        url = url_base + list_loc[i][2][1:]
        if len(post_url_pool) < threading_num and i != total_number - 1:
            post_url_pool.append(url)
            infor_pool.append((list_loc[i][0], list_loc[i][1], list_loc[i][2]))
            print("准备爬取第 {} 个的评论全文".format(i))
            continue

        # 最后一页既要进url池，又要启动线程
        if i == total_number - 1:
            print("准备爬取第 {} 个的评论全文".format(i))
            post_url_pool.append(url)

        threads = multi_threading(post_url_pool, ip_list)

        with open(filePath, 'a+', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            num = 0
            for thread in threads:
                (title, content) = thread.get_result()
                print("title: {}".format(title))
                print("content: {}".format(content))
                writer.writerow(
                    [infor_pool[num][0], infor_pool[num][1], infor_pool[num][2], title, content])
                num += 1

        # 准备下一次输送给线程的url
        if i != total_number - 1:
            print("准备爬从第 {} 页开始的评论".format(i))
            post_url_pool = [url]
            infor_pool = [(list_loc[i][0], list_loc[i][1], list_loc[i][2])]


if __name__ == "__main__":
    city_id = "g60763"
    comment_id_path = "./data/" + city_id + "_comment_id.csv"
    comment_path = "./data/" + city_id + "_comment_all.csv"
    get_comments(comment_id_path, comment_path)
