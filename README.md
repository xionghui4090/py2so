# py2so
编译py为so文件，更好的隐藏源码，可以直接编译整个python工程\n
删除.pyc .pyo文件\n
删除.py源文件\n
删除.c编译文件\n

也可以使用Makefile的形式：
1.将Makefile和工程目录放在同一目录下；\n
2.前提是安装Cpython解释器；\n
3.执行make，则直接编译所有文件；\n
4.执行make clean-build，删除所有py文件；\n
5.执行make dist，直接将工程打包成tar.gz包；\n
