# encoding=utf-8

import os
import sys

# 使用脚本前请注意,在根目录下创建文件件/source/
des = "/cp_lz4"
# 设置递归深度,防止文件过多
sys.setrecursionlimit(1000000)  # 例如这里设置为一百万


# 进行压缩
def zipFiles(path):
    target_files = os.listdir(path)
    for i in range(0, len(target_files)):
        if not (path.endswith("/")):
            path = path + "/"  # 初始进入的时候最后没有/,所以需要进行此操作
        fileDir = path + target_files[i] + "/"
        judge = os.path.isdir(fileDir)
        if judge == True:
            # 证明是文件夹
            zipFiles(fileDir)
        else:
            print("开始进行压缩")
            # 如果不是文件夹,开始压缩
            print(fileDir[:-1])

            os.system('lz4_hadoop ' + fileDir[:-1] + " " + fileDir[:-1] + ".lz4")
    print("数据压缩完成")


# 参数最后要带有/ eg.  /log/
# 例如目标文件目录如下:   /data/20160908/
def splitData(path):
    print("开始切分数据")
    files = os.listdir(path)
    print(files)
    for i in range(0, len(files), 1):
        print("正在切分第" + str(i) + "份数据")
        filesDir = path + files[i]
        judge = os.path.isdir(filesDir)
        if judge == True:
            # 证明是文件夹
            print("现在文件路径为:" + filesDir)
            splitData(filesDir + "/")
        else:
            # 如果不是文件夹
            fileName = str.split(filesDir, '/')[-1]
            print("文件名字为: " + str(fileName))
            source = path + files[i]
            target = des + "/" + str.split(path, '/')[-2]  # deslog
            ex = os.path.exists(target)
            if ex == False:
                os.system('mkdir -p ' + target)
            os.system('split -l 2100000 -d ' + source)
            # 这里注意,因为read x后读出来的是./xxxx 格式的,我们需要把前面的./ 去掉,所以这使用${x#*./},他的意思是把首次出现的./给去掉
            # 剩下的是我们所需的
            cmd = 'find . -name "x*" | while read x; do mv  $x  ' + target + "/" + fileName + '_${x#*./}' + '; done'
            os.system(cmd)
    print("数据切分完毕")


# 导出到hdfs
# data带上路径,target如: hdfs://iZ23cnv8zg3Z:8022/tmp/tmpTest/"
def toHDFS(data, target):
    os.system("HADOOP_USER_NAME=hdfs hdfs dfs -put " + data + "  " + target)


maxSize = 0.0


# 获取压缩文件中最大文件 (目前还有缺陷,路径需要人为调整)
def getMaxFileSize():
    files = os.popen('du -sh /url_log_lz4/log/*.lz4').readlines()
    for i in range(0, len(files), 1):
        items = files[i].split("\t")
        size = items[0][:-1]
        if size > maxSize:
            maxSize = size


for i in range(1, len(sys.argv), 1):
    splitData(sys.argv[i])

zipFiles(des)
