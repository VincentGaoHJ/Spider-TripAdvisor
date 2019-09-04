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
from proxy_github import getProxy
from getPoiComments_id import getPoiComments_id


def get_list(input_file):
    """
    读取文件，将每一行的元素保存成元组放入列表
    :param input_file: 文件路径
    :return: list_loc
    """
    list_loc = []
    with open(input_file, 'r', encoding='utf-8') as f:
        next(f)
        for line in f.readlines():
            list = line.strip().split()
            list_loc.append((list[0], list[1], list[2], list[3]))
    return list_loc


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

    print(last_line)
    return last_line


def get_starter(init_file_path, file_path):
    """
    判断完整的景点目录文件是否存在，如果存在则读入;
    判断将要写入的评论文件是否存在，如果存在则读入已经爬取到的最后一个景点的poiid和这个景点评论的页数，若不存在则不用管;
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
        poi_id = last_line_list[1]
        print("[Continue]Already Spider POI :", poi_id)

        list_loc_copy = copy.deepcopy(list_loc)
        for poi in list_loc_copy:
            if poi[0] != poi_id:
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
    print("[Get_List]The valid IP: ", ip_list)

    for i in range(total_number):
        with open(filePath, 'a+', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            base_url = list_loc[i][2]
            links = getPoiComments_id(base_url, ip_list)
            for link in links:
                link_sec = link.split("-")
                writer.writerow([link_sec[1], link_sec[2], link_sec[3], link])
            print("[Get_Comments]Done write file " + str(list_loc[i][1]) + " page number is " + str(list_loc[i][3]))


if __name__ == "__main__":
    city_id = "g60763"
    initFilePath = "./data/" + city_id + "_list_all.txt"
    filePath = "./data/" + city_id + "_comment_id.csv"
    get_comments(initFilePath, filePath)
