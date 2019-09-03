# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/9/3
@Author: Haojun Gao
@Description:
"""

import os
import requests
from random import choice
from proxy_github import getProxy
from html.parser import HTMLParser


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
                print('====')
                for (variable, value) in attrs:
                    print(variable, value)
                    if variable == "href":
                        if 'Attraction_Review' in value and '#REVIEWS' not in value:
                            if value not in self.links:
                                self.links.append(value)


def get_last_line(input_file):
    """
    读取文件的最后一行
    :param input_file: 文件名
    :return: last_line
    """
    file_size = os.path.getsize(input_file)
    block_size = 1024
    dat_file = open(input_file, 'rb')
    last_line = ""
    if file_size > block_size:
        max_seek_point = (file_size // block_size)
        dat_file.seek((max_seek_point - 1) * block_size)
    elif file_size:
        dat_file.seek(0, 0)
    lines = dat_file.readlines()
    if lines:
        last_line = lines[-1].strip()
    dat_file.close()
    return last_line


def get_starter(file_path):
    """
    读取文件中最后一行的内容并且判断已经爬取到的页数
    :param file_path: 文件所在路径
    :return: page_num(已经爬取到的页数)
    """
    page_num = 1
    if os.access(file_path, os.F_OK):
        print("[Get_List]Given file path is exist.")
        page_byte = get_last_line(file_path).split()[-1]
        # 检查是否只有表头
        if page_byte.decode(encoding='utf-8') != "page":
            page_num = int(page_byte.decode(encoding='utf-8'))
            print("[Get_List]Already spider page :", page_num)
    else:
        with open(file_path, 'a+', encoding='utf-8') as f:
            f.write("name\tpoi_id\tpoi_html\tpage\n")
    return page_num


def get_list(province_id, filePath):
    ip_list = getProxy()
    proxies = choice(ip_list)
    print("[Get_List]The valid IP: ", ip_list)

    url_base_1 = 'https://cn.tripadvisor.com/Attractions-' + str(province_id) + '-Activities-oa'
    url_base_2 = '-New_York_City_New_York.html'

    page = get_starter(filePath)

    while page <= 50:
        num = (page - 1) * 30
        url = url_base_1 + str(num) + url_base_2

        # 使用自定义的opener对象，调用open()方法来发送请求
        try:
            response = requests.get(url, proxies=proxies)
        except Exception as e:
            print("[Get_List]Error ", e)
            print("[Get_List]False to spider page " + str(page))
            page -= 1
            ip_list = getProxy()
            proxies = choice(ip_list)
        else:
            print("[Get_List]Success to spider page " + str(page))

            html_code = response.text
            # print(html_code)
            hp = MyHTMLParser()
            hp.feed(html_code)
            hp.close()
            print(hp.links)
            print("[Get_List]Success to spider poi " + str(len(hp.links)))

            # 判断是否爬完
            if len(hp.links) == 0:
                break

            for loc in hp.links:
                with open(filePath, 'a+', encoding='utf-8') as f:
                    loc_list = loc.split("-")
                    # print(loc_list[4])
                    f.write(str(loc_list[2]) + "\t" +
                            str(loc_list[4]) + "\t" +
                            str(loc) + "\t" +
                            str(page) + "\n")
        page += 1
    print("[Get_List]Done spider all the list")


if __name__ == "__main__":
    # 纽约 g60763
    city_id = "g60763"

    poi_path = "./data/" + city_id + "_list_all.txt"

    get_list(city_id, poi_path)
