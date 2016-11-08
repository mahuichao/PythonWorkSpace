# encoding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import random as rd


# 从文本读取数据,创建数据集和标签
def loadData(path):
    lines = open(path, "r").readlines()
    mymat = []
    mylabel = []
    for line in lines:
        lineArr = line.strip().split()
        mymat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        mylabel.append(int(lineArr[2]))
    return mymat, mylabel


# sigmoid 分类函数
def sigmoid(inX):
    return 1.0 / (1 + np.exp(-inX))


# 梯度递增
def gradAscent(dataInput, labelInput):
    dataMatrix = np.mat(dataInput)
    label_V = np.mat(labelInput).transpose()
    m, n = np.shape(dataMatrix)
    step = 0.001
    circle = 500
    weight = np.ones((n, 1))
    for i in range(circle):
        h = sigmoid(dataMatrix * weight)
        err = (label_V - h)
        weight = weight + step * dataMatrix.transpose() * err
    return weight


# 第一次改进后
def stocGradAscent0(dataInput, labelInput):
    m, n = np.shape(dataInput)
    alpha = 0.01
    weight1 = np.ones(n)
    for i in range(m):
        h = sigmoid(sum(dataInput[i] * weight1))
        error = labelInput[i] - h
        weight1 += alpha * dataInput[i] * error
    return weight1


def stocGradAscent1(dataInput, labelInput, numIter=150):
    m, n = shape(dataInput)
    weights = np.ones(n)
    dataIndex = range(m)
    for j in range(numIter):
        for i in range(m):
            alpha = 4 / (1.0 + j + i) + 0.01
            randIndex = int(rd.uniform(0, len(dataIndex)))
            h = sigmoid(sum(dataInput[randIndex] * weights))
            error = labelInput[randIndex] - h
            weights += alpha * error * dataInput[i]
            del (dataIndex[randIndex])
    return weights


# 画出图形
def plotBestFit(wei, path):
    weight2 = wei.getA1()
    dataMat, labelMat = loadData(path)
    dataArray = np.mat(dataMat)
    n = np.shape(dataArray)[0]
    xcord1 = []
    ycord1 = []
    xcord2 = []
    ycord2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            xcord1.append(dataArray[i, 1])
            ycord1.append(dataArray[i, 2])
        else:
            xcord2.append(dataArray[i, 1])
            ycord2.append(dataArray[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1, ycord1, s=30, c='red', marker='s')
    ax.scatter(xcord2, ycord2, s=30, c='green')
    x = np.arange(-3.0, 3.0, 0.1)
    y = (-weight2[0] - weight2[1] * x) / weight2[2]
    ax.plot(x, y)
    plt.xlabel("X1")
    plt.ylabel("X2")
    plt.show()


path = "/Users/mahuichao/PyCharmWorkSpace/Algorithm/DataSet/testSet.txt"
dataArr, labelMat = loadData(path)
weights = stocGradAscent0(np.array(dataArr), labelMat)
print np.mat(weights)
plotBestFit(np.mat(weights), path)
