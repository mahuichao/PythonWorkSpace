# encoding=utf-8
from numpy import *
import operator
import matplotlib.pyplot as plt
from os import listdir


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


#   1 计算已知类别数据集中的每个点与当前的点之间的距离
#   2 按照距离递增次序排序
#   3 选取与当前点距离最近的k个点
#   4 确定前k个点所在类别的出现频率
#   5 返回前k个点出现频率最高的类别作为当前的预测分类

def classifyo(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDistIndices = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndices[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.iteritems(),
                              key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


# 将文本转化为Numpy的解析程序
def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)
    # 创建矩阵(其实创建的是一个多维数组,这里也就是x行三列)
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []
    index = 0
    for line in arrayOLines:
        line = line.decode("utf-8").strip()
        listFromLine = line.decode("utf-8").split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector


# 数据归一
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet / tile(ranges, (m, 1))
    return normDataSet, ranges, minVals


# 误差评估
def datingClassTest():
    hoRatio = 0.10
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m * hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classifyo(normMat[i, :], normMat[numTestVecs:m, :], datingLabels[numTestVecs:m], 3)
        print "the classifier came back with:%d,the real answer is :%d" % (classifierResult, datingLabels[i])
        if (classifierResult != datingLabels[i]): errorCount += 1.0
    print "the total error rate is: %f" % (errorCount / float(numTestVecs))


# 开启匹配
def classcifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(raw_input("percentage of time spent playing video games?"))
    ffMiles = float(raw_input("frequent flier miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumed per year"))
    datingDataMat, datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classifyo((inArr - minVals) / ranges, normMat, datingLabels, 3)
    print "you will probably like this person: ", resultList[classifierResult - 1]


def img2vector(filename):
    returnVect = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32 * i + j] = int(lineStr[j])
    return returnVect


def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')
    m = len(trainingFileList)
    trainingMat = zeros((m, 1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i, :] = img2vector('trainingDigits/%s' % fileNameStr)
    testFileList = listdir('testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classifyo(vectorUnderTest, trainingMat, hwLabels, 3)
        print "the classifier came back with: %d,the real answer is :%d" % (classifierResult, classNumStr)
        if (classifierResult != classNumStr): errorCount += 1.0
    print "\nthe total number of errors is:%d" % errorCount
    print "\nthe total error  rate is:%f" % (errorCount / float(mTest))


# group, labels = createDataSet()

# 第一个参数为待分类的数据
# s = classifyo([0.6, 0.7], group, labels, 3)
# print(s)

# returnMat, classLabelVector = file2matrix("datingTestSet2.txt")
# print (returnMat[:,1])
# print(classLabelVector)


# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(returnMat[:, 1], returnMat[:, 2])
# ax.scatter(returnMat[:, 1], returnMat[:, 2], 15.0 * array(classLabelVector), 15.0 * array(classLabelVector))
# plt.show()

# normMat, ranges, minVals = autoNorm(returnMat)
# print(normMat)
# print(ranges)
# print(minVals)

# datingClassTest()

# classcifyPerson()

# testVector = img2vector("trainingDigits/0_13.txt")
# print(testVector)


handwritingClassTest()
