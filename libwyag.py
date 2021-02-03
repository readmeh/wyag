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

# cat-file 子命令
argsp = argsubparsers.add_parser("cat-file",
                                 help="Provide content of repository objects")

argsp.add_argument("type",
                   metavar="type",
                   choices=["blob", "commit", "tag", "tree"],
                   help="Specify the type")

argsp.add_argument("object",
                   metavar="object",
                   help="The object to display")

argsp = argsubparsers.add_parser("hash-object",
                                 help="Compute object ID and optionally creates a blob from a file")

argsp.add_argument("-t",
                   metavar="type",
                   dest="type",
                   choices=["blob", "commit", "tag", "tree"],
                   default="blob",
                   help="Specify the type")

argsp.add_argument("-w",
                   dest="write",
                   action="store_true",
                   help="Actually write the object into the database")

argsp.add_argument("path",
                   help="Read object from <file>")

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



def cmd_init(args):
    print("调用命令{}中：".format(sys._getframe().f_code.co_name))
    repo_create(args.path)

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

        if not (force or os.path.join(self.wyagdir)):
            raise Exception("Not a wyag repository %s"%path)

        # Read configuration file in .wyag/config

        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception("Unsupported repository format version %s"% vers)

def repo_file(repo, *path, mkdir=False):
    """Same as repo_path, but create dirname(*path) if absent.
    For example, repo_file(r, \"refs\", \"remotes\", \"origin\",
    \"HEAD\") will create .wyag/refs/remotes/origin."""

    if repo_dir(repo, *path[:-1], mkdir=mkdir):
        print(path)
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
    return os.path.join(repo.wyagdir, *path)

def repo_default_config():
    ret = configparser.ConfigParser()

    ret.add_section("core")
    ret.set("core", "repositoryformatversion", "0")
    ret.set("core", "filemode", "false")
    ret.set("core", "bare", "false")

    return ret

def repo_find1(path=".", required=True):
    path = os.path.realpath(path)

    if os.path.isdir(os.path.join(path, ".git")):
        return GitRepository(path)

    # If we haven't returned, recurse in parent, if w
    parent = os.path.realpath(os.path.join(path, ".."))

    if parent == path:
        # Bottom case
        # os.path.join("/", "..") == "/":
        # If parent==path, then path is root.
        if required:
            raise Exception("No git directory.")
        else:
            return None

    # Recursive case
    return repo_find(parent, required)

def repo_find(path = ".", required=True):
    # 返回指定文件的规范路径，消除path中存在的任何符号链接
    path = os.path.realpath(path)

    # 通过.wyag目录查找repository
    print(path)
    if os.path.isdir(os.path.join(path,".wyag")):
        return WyagRepository(path)

    # 递归到父结点
    parent = os.path.realpath(os.path.join(path, ".."))

    # 退出条件 验证是否是根目录
    if parent == path:
        if required:
            raise Exception("Not found a repository!")
        else:
            return None
    
    return repo_find(parent,required)


#####################################################
#实现cat-file命令                                     #
#####################################################

def cmd_cat_file(args):
    print(args.object)
    repo = repo_find()
    cat_file(repo, args.object, fmt=args.type.encode())

def cat_file(repo, obj, fmt=None):
    obj = object_read(repo, object_find(repo, obj, fmt=fmt))
    sys.stdout.buffer.write(obj.serialize())

def cmd_hash_object(args):
    if args.write:
        repo = repo_find(args.path)
    else:
        repo = None

    with open(args.path, "rb") as fd:
        sha = object_hash(fd, args.type.encode(), repo)
        print(sha)

# 创建wyag object 基类
class WyagObject(object):
    
    repo = None
    
    def __init__(self, repo, data = None):
        self.repo = repo

        if data != None:
            self.deserialize(data)

    def serialize(self):
        raise Exception("Unimplemented")

    def deserialize(self, data):
        raise Exception("Unimplemented")

def object_read(repo, sha):
    """Read object object_id from Wyag repository repo. Return a WyagObject whose exact type
    depends on the object."""

    print(sha)
    path = repo_file(repo, "objects", sha[0:2], sha[2:])
    print(path)

    with open(path, "rb") as f:
        raw = zlib.decompress(f.read())

        x = raw.find(b' ')
        fmt = raw[0:x]
        
        y = raw.find(b'\x00', x)
        size = int(raw[x+1:y].decode('ascii'))
        if size != len(raw) - y -1:
            raise Exception("Malformed object {0}: bad length".format(sha))

        if fmt == b'commit':
            c = WyagCommit
        elif fmt == b'tree':
            c = WyagTree
        elif fmt == b'tag':
            c = WyagTag
        elif fmt == b'blob':
            c = WyagBlob
        else:
            raise Exception("Unknown type %s for object %s".format(fmt.decode("ascii"), sha))

        # Call constructor and return object
        return c(repo, raw[y + 1:])

def object_find(obj, name, fmt=None, follow=True):
    return name

def object_write(obj, actually_write=True):
    # Serialize object data
    data = obj.serialize()
    # Add header
    result = obj.fmt + b' ' + str(len(data)).encode() + b'\x00' + data
    # Compute hash
    sha = hashlib.sha1(result).hexdigest()

    if actually_write:
        # Compute path
        path = repo_file(obj.repo, "objects", sha[0:2], sha[2:], mkdir=actually_write)
        print(obj.repo,'\n',sha,'\n',path)
        with open(path, 'wb') as f:
            # Compress and write
            f.write(zlib.compress(result))

    return sha

def object_hash(fd, fmt, repo=None):
    data = fd.read()

    # Choose constructor depending on
    # object type found in header.
    if   fmt==b'commit' : obj=WyagCommit(repo, data)
    elif fmt==b'tree'   : obj=WyagTree(repo, data)
    elif fmt==b'tag'    : obj=WyagTag(repo, data)
    elif fmt==b'blob'   : obj=WyagBlob(repo, data)
    else:
        raise Exception("Unknown type %s!" % fmt)

    return object_write(obj, repo)

class WyagBlob(WyagObject):
    fmt = b'blob'

    def serialize(self):
        return self.blobdata

    def deserialize(self, data):
        self.blobdata = data
