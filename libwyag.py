# -*- config: utf-8 -*-
# @File  : libwyag.py.py
# @Auther: Hxp
# @Date  : 2021/2/1 : 9:46
# @create myself own git

# 导入模块
import argparse
import collections
import configparser
import hashlib
import os,re,sys,zlib
import time

# 解析命令行参数
argparser = argparse.ArgumentParser(description="The stupid content tracker")

# 增加子命令
argsubparsers = argparser.add_subparsers(title="Commands", dest="command")
argsubparsers.required = True

# init 子命令
argsp = argsubparsers.add_parser("init", help="Initialize a new, empty repository.")

argsp.add_argument("path",
                   metavar="directory",
                   nargs="?",
                   default=".",
                   help="Where to create the repository.")

def cmd_init(args):
    print("调用命令{}中：".format(sys._getframe().f_code.co_name))
    repo_create(args.path)

def main(argv = sys.argv[1:]):
    args = argparser.parse_args(argv)

    if args.command == "add": cmd_add(args)
    elif args.command == "cat-file": cmd_cat_file(args)
    elif args.command == "checkout": cmd_checkout(args)
    elif args.command == "commit": cmd_commit(args)
    elif args.command == "hash-object": cmd_hash_object(args)
    elif args.command == "init": cmd_init(args)
    elif args.command == "log": cmd_log(args)
    elif args.command == "ls-tree": cmd_ls_tree(args)
    elif args.command == "merge": cmd_merge(args)
    elif args.command == "rebase": cmd_rebase(args)
    elif args.command == "rev-parse": cmd_rev_parse(args)
    elif args.command == "rm": cmd_rm(args)
    elif args.command == "show-ref": cmd_show_ref(args)
    elif args.command == "tag": cmd_tag(args)

def repo_create(path):
    """Create a new repository at path."""
    time.sleep(5)
    print("调用成功，正在创建仓库--{}".format(path))
    time.sleep(1)
    repo = WyagRepository(path, True)

    # First, we make sure the path either doesn't exist or is an empty dir.
    print(f"########\n验证{repo.worktree}目录情况\n#######")
    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            raise Exception("{} is not a directory".format(path))
        if os.listdir(repo.worktree):
            raise Exception("{} is not empty".format(path))
    else:
        os.makedirs(repo.worktree)

    assert (repo_dir(repo, "branches", mkdir=True))
    assert (repo_dir(repo, "objects", mkdir=True))
    assert (repo_dir(repo, "refs", "tags", mkdir=True))
    assert (repo_dir(repo, "refs", "heads", mkdir=True))

    time.sleep(5)
    print("写入相关文件。。。")
    # .wyag/description
    with open(repo_file(repo, "description"), "w") as f:
        f.write("Unnamed repository; edit this file 'description' to name the repository.\n")

    # .wyag/HEAD
    time.sleep(1)
    print("写入HEAD文件。。。")
    with open(repo_file(repo, "HEAD"), "w") as f:
        f.write("ref: refs/heads/master\n")

    time.sleep(1)
    print("写入config文件。。。")
    with open(repo_file(repo, "config"), "w") as f:
        config = repo_default_config()
        config.write(f)

    return repo

class WyagRepository(object):
    """A wyag repository"""

    worktree = None
    wyagdir = None
    conf = None

    def __init__(self, path, force=False):
        self.worktree = path
        self.wyagdir = os.path.join(path, ".wyag")

        time.sleep(5)
        print("读取地址：\n{}\n{}\n{}\n{}".format(self,self.worktree,self.wyagdir,self.conf))
        if not (force or os.path.join(self.wyagdir)):
            raise Exception("Not a wyag repository %s"%path)

        # Read configuration file in .wyag/config
        time.sleep(5)
        print("读取{}/.wyag/config文件".format(path))
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        time.sleep(5)
        print(f"检查conf文件：{cf}\n{self.conf}")
        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file misssing")

        print("验证程序版本。。。")
        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception("Unsupported repository format version %s"% vers)

def repo_file(repo, *path, mkdir=False):
    """Same as repo_path, but create dirname(*path) if absent.
    For example, repo_file(r, \"refs\", \"remotes\", \"origin\",
    \"HEAD\") will create .wyag/refs/remotes/origin."""

    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        return repo_path(repo, *path)

def repo_dir(repo, *path, mkdir=False):
    """Same as repo_path, but mkdir *path if absent if mkdir."""

    path = repo_path(repo, *path)

    if os.path.exists(path):
        if (os.path.isdir(path)):
            return path
        else:
            raise Exception("Not a diretory %s"% path)


    if mkdir:
        os.makedirs(path)
        return path
    else:
        return None

def repo_path(repo, *path):
    """Comute path under repo's wyagdir"""
    time.sleep(5)
    print("文件路径:{}".format(os.path.join(repo.wyagdir, *path)))
    return os.path.join(repo.wyagdir, *path)

def repo_default_config():
    time.sleep(5)
    print("加载默认配置。。。")
    ret = configparser.ConfigParser()

    ret.add_section("core")
    ret.set("core", "repositoryformatversion", "0")
    ret.set("core", "filemode", "false")
    ret.set("core", "bare", "false")

    return ret

def repo_find(path = ".", required=True):
    # 返回指定文件的规范路径，消除path中存在的任何符号链接
    path = os.path.realpath(path)

    # 通过.wyag目录查找repository
    if os.path.isdir(os.path.join(path,".wyag")):
        return WyagRepository(path)

    # 递归到父结点
    parent = os.path.join(path,"..")

    # 退出条件 验证是否是根目录
    if path == parent:
        if required:
            raise Exception("Not found a repository!")
        else:
            return None
    
    return repo_find(parent,required)

# 创建wyag对象基类
class WyagObject(object):
    
    repo = None
    
    def __init__(self, repo, data = None):
        self.repo = repo

        if data != None:
            self.deserialize(data)