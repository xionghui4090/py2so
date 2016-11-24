#!/usr/bin/env python
#-* -coding: UTF-8 -* -

__author__ = 'Xiong Hui'

"""
执行前提：
    系统安装python-devel 和 gcc
    Python安装cython
编译整个当前目录：
    python py-setup.py
编译某个文件夹：
    python py-setup.py SLB
生成结果：
    在build/SLB/下，保留__init__.py文件，其他全部都是.so文件
生成完成后：
    启动文件还需要py/pyc担当，须将启动的py/pyc拷贝到编译目录并删除so文件
"""

import sys, os, shutil, time
from distutils.core import setup
from Cython.Build import cythonize

starttime = time.time()
currdir = os.path.abspath('.')
parentpath = sys.argv[1] if len(sys.argv) > 1 else ""



def getpy(basepath=currdir, parentpath=parentpath, name='', excepts=(), delC=True, delPy=True):
    """
    获取py文件的路径
    :param basepath: 根路径
    :param parentpath: 父路径
    :param name: 文件/夹
    :param excepts: 排除文件
    :return: py文件的迭代器
    """
    fullpath = os.path.join(basepath, parentpath, name)
    for fname in os.listdir(fullpath):
        ffile = os.path.join(fullpath, fname)
	# process directory        
	if os.path.isdir(ffile) and not fname.startswith('.'):
            getpy(basepath, os.path.join(parentpath, name), fname, excepts, delC, delPy)
        elif os.path.isfile(ffile):
            ext = os.path.splitext(fname)[1]
            if ext == ".c" and delC or ext in ('.pyc', '.pyo') and delPy:
                os.remove(ffile)
            elif ffile not in excepts and os.path.splitext(fname)[1] not in('.pyc', '.pyx'):
                if os.path.splitext(fname)[1] in ('.py', '.pyx') and not fname.startswith('__'):
                    # compile to so
		    setup(ext_modules = cythonize([ffile]),script_args=["build_ext","-b", os.path.abspath('.') ,"-t", os.path.abspath('.')])
                    os.remove(ffile)
		    os.remove(os.path.join(fullpath, os.path.splitext(fname)[0]+'.c'))
getpy()
print "complete! time:", time.time()-starttime, 's'
