# encoding=utf-8
import numpy as np
from math import *


def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVect = [0, 1, 0, 1, 0, 1]
    return postingList, classVect


def createVocabList(dataSet):
    resultsSet = set([])
    for document in dataSet:
        resultsSet = resultsSet | set(document)
    return list(resultsSet)


def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word %s is not  in my vocabulary!" % word
    return returnVec


def trainNBO(trainMatrix, trainCategory):
    numTrainDoc = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDoc)
    p0Num = np.zeros(numWords)
    p1Num = np.zeros(numWords)
    p0Denom = 0.0
    p1Denom = 0.0
    for i in range(numTrainDoc):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += 1
        else:
            p0Num += trainMatrix[i]
            p0Denom += 1
    p1Vect = p1Num / p1Denom
    p0Vect = p0Num / p0Denom
    return p0Vect, p1Vect, pAbusive


def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0


def testingNB():
    listOposts, listClasses = loadDataSet()
    myVocabList = createVocabList(listOposts)
    trainMat = []
    for postinDoc in listOposts:
        trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
    p0v, p1v, pAb = trainNBO(np.array(trainMat), np.array(listClasses))
    testEntry = ['love', 'my', 'dalmation']
    thisDoc = np.array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, 'classified as: ', classifyNB(thisDoc, p0v, p1v, pAb)
    testEntry = ['stupid', 'garbage']
    thisDoc = np.array(setOfWords2Vec(myVocabList, testEntry))
    print testEntry, "classified as: ", classifyNB(thisDoc, p0v, p1v, pAb)


testingNB()
