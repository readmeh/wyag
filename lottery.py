# -*- config: utf-8 -*-
# @File  : lottery.py.py
# @Auther: Hxp
# @Date  : 2021/1/5 : 10:46
# @彩票预测

import requests
from bs4 import BeautifulSoup
from collections import Counter
import csv


def pparser():
    # 发起请求
    basic_url = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list_1.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    response = requests.get(basic_url, headers=headers, timeout=10)
    response.encoding = 'utf-8'
    htm = response.text

    # 解析内容
    soup = BeautifulSoup(htm, 'html.parser')
    # 获取页数信息
    page = int(soup.find('p', attrs={"class": "pg"}).find_all('strong')[0].text)

    # url前缀
    url_part = 'http://kaijiang.zhcw.com/zhcw/html/ssq/list'

    # 分页获取每一页的开奖信息
    for i in range(1, page + 1):
        url = url_part + '_' + str(i) + '.html'
        print(url)

        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = 'utf-8'
        context = res.text
        soups = BeautifulSoup(context, 'html.parser')

        if soups.table is None:
            continue
        elif soups.table:
            table_rows = soups.table.find_all('tr')
            for row_num in range(2, len(table_rows) - 1):
                row_tds = table_rows[row_num].find_all('td')
                ems = row_tds[2].find_all('em')
                result = row_tds[0].string + ',' + row_tds[1].string + ',' + ems[0].string + ',' + ems[
                    1].string + ',' + ems[2].string + ',' + ems[3].string + ',' + ems[4].string + ',' + ems[
                             5].string + ',' + ems[6].string
                #print(result)

                save_to_file(result)

                red_num[0].append(ems[0].string)  # 红色球1
                red_num[1].append(ems[1].string)  # 红色球2
                red_num[2].append(ems[2].string)  # 红色球3
                red_num[3].append(ems[3].string)  # 红色球4
                red_num[4].append(ems[4].string)  # 红色球5
                red_num[5].append(ems[5].string)  # 红色球6
                blue_num.append(ems[6].string)  # 蓝色球
                print(blue_num)
        else:
            continue

    return red_num, blue_num


def save_to_file(content):
    with open('ssq.txt', 'a', encoding='utf-8') as f:
        f.write(content + '\n')


def predict(red_num, blue_num):
    names = locals()
    for i in range(5):
        name['red_count' + str(i)] = Counter(red_num[i])
    print(red_count0)
    blue_count = Counter(blue_num)
    print(blue_count)

    print('------------------------------------------------------------------------------')
    # 按照出现频率顺序
    names = locals()
    for i in range(5):
        names['red_sorted0' + str(i)] = sorted(names['red_count' + str(i)].items(), key=lambda x: x[1], reverse=False)
    blue_sorted = sorted(blue_count.items(), key=lambda x: x[1], reverse=False)
    red0 = red_sorted[0]
    blue = blue_sorted[0:3]

    red = list(map(lambda x: x[0], red))
    blue = list(map(lambda x: x[0], blue))
    print('号码高频-1注：' + str(red) + ' | ' + blue[0])
    print('号码高频-2注：' + str(red) + ' | ' + blue[1])
    print('号码高频-3注：' + str(red) + ' | ' + blue[2])
    print('------------------------------------------------------------------------------')


if __name__ == '__main__':
    # 定义两个变量, 用于记录历史开奖信息中的红球、蓝球号码信息
    red_num = [[],[],[],[],[],[]]
    blue_num = []

    # 调用函数，用于获取并解析开奖的数据
    pparser()
    #with open('lottery_red.csv', 'w', newline='') as csvfile:
    #    writer = csv.writer(csvfile)
    #    for row in red_num:
    #        writer.writerow(row)
    #with open('lottery_blue.csv', 'w', newline='') as csvfile:
    #    writer = csv.writer(csvfile)
    #    for row in blue_num:
    #        writer.writerow([row])
    #print(red_num)
    #print(blue_num)
    # 分析数据并预测未来的开奖信息
    #with open('lottery_red.csv', 'r', newline='') as csvfile:
    #    red_num = list(csv.reader(csvfile))
    #    print(red_num)
    #with open('lottery_blue.csv', 'r', newline='') as csvfile:
    #    tmp = list(csv.reader(csvfile,delimiter="\n"))
    #blue_num = [tmp[i] for i in range(len(tmp))]
    predict(red_num, blue_num)