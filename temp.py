# -*- coding: utf-8 -*-
"""
@Date: Created on 2019/9/3
@Author: Haojun Gao
@Description: 
"""

import requests
from random import choice
from proxy_github import getProxy
from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    text_title = False
    text_content = False

    def handle_starttag(self, tag, attr):
        if tag == 'h1':
            if dict(attr)["class"] == "title":
                self.text_title = True
                print(dict(attr))
        if tag == 'span':
            if dict(attr)["class"] == "fullText ":
                self.text_content = True
                print(dict(attr))

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.text_title = False
        if tag == 'span':
            self.text_content = False

    def handle_data(self, data):
        if self.text_title:
            print(data)
        if self.text_content:
            print(data)


ip_list = getProxy()
proxies = choice(ip_list)
print("[Get_List]The valid IP: ", ip_list)

page = 1

url = "https://cn.tripadvisor.com/OverlayWidgetAjax?Mode=EXPANDED_SUR_REVIEWS_RESP&metaReferer=ShowUserReviewsAttractions&reviewId=705665837"
response = requests.get(url, proxies=proxies)
html_code = response.text
print(html_code)
hp = MyHTMLParser()
hp.feed(html_code)
hp.close()
