# -*- config: utf-8 -*-
# @File  : prog.py.py
# @Auther: Hxp
# @Date  : 2021/2/1 : 21:55
# @

import argparse
import configparser
import os,re,sys,shutil

"""argparse 测试部分
"""
# parser = argparse.ArgumentParser(description='Process some integers.',
#                                  prog="argparse测试程序",
#                                  usage='%(prog)s [options]',
#                                  epilog="a test program of argparse package:{}".format(os.path.join("d://","h")))
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
# 
# argsubparsers = parser.add_subparsers(title="Commands", dest="command")
# argsubparsers.required = True
# 
# def main(argv = sys.argv[1:]):
#     args = parser.parse_args()
#     print(args.accumulate(args.integers))
# 
#     if args.command == "dir":
#         cmd_dir(args)
# 
# args = parser.parse_args()
# print(args.accumulate(args.integers))

try:
    result=10/2
except ZeroDivisionError:
    print("除数为零！！")
else:
    print(result)

# raise Exception('这个可以用')

class DogNotFoundException(Exception):
    pass

try:
    os.makedirs("./1/2/3/4/5")
    #shutil.rmtree("./1/")
    config = configparser.ConfigParser()
    config.read("./test.conf") # 读取文件，如果目录内无该文件则创
    config.add_section('module_1') # 添加section
    config.set("module_1", "A", "1") # 在section中添加键值对
    print(config.sections(),"中的键值对：", config.items('module_1')) # 获取文件中所有的section及键值对
    config.write(open("./test.conf","w+"))
    os.remove("./test.conf")

    raise DogNotFoundException()
except DogNotFoundException:
    print('Dog not found!')

assert ("./a")

print(sys.argv[1:])