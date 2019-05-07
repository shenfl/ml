import numpy as np
import matplotlib.pyplot as plt
import operator
from os import listdir


def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())  # get the number of lines in the file
    returnMat = np.zeros((numberOfLines, 3))  # prepare matrix to return
    classLabelVector = []  # prepare labels return
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat, classLabelVector


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    m = dataSet.shape[0]
    normDataSet = dataSet - np.tile(minVals, (m, 1))
    normDataSet = normDataSet / np.tile(ranges, (m, 1))
    return normDataSet, ranges, minVals


def createDataSet():
    group = np.array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = np.tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffMat ** 2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances ** 0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)  # key=lambda x: x[1]
    return sortedClassCount[0][0]


def datingClassTest():
    hoRatio = 0.5
    datingDataMat, datingLabels = file2matrix("datingTestSet2.txt")
    normMat, ranges, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTest = int(m * hoRatio)
    errorCount = 0
    for i in range(numTest):
        classifierResult = classify0(normMat[i, :], normMat[numTest:m, :], datingLabels[numTest:m], 3)
        print("the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i]))
        if classifierResult != datingLabels[i]:
            errorCount += 1.0
    print("the total error rate is: %f" % (errorCount / float(numTest)))
    print(errorCount)


def image2Vec(fileName):
    returnVec = np.zeros((1, 1024))
    fr = open(fileName)
    for i in range(32):
        line = fr.readline()
        for j in range(32):
            returnVec[0, 32 * i + j] = int(line[j])
    return returnVec


def handWritingClassifier():
    hwLabels = []
    trainingFileList = listdir("trainingDigits")
    m = len(trainingFileList)
    trainingMat = np.zeros((m, 1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        number = int(fileStr.split('_')[0])
        hwLabels.append(number)
        trainingMat[i, :] = image2Vec('trainingDigits/%s' % fileNameStr)
    testFileList = listdir('testDigits')
    errorCount = 0;
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileName = fileNameStr.split('.')[0]
        classNum = int(fileName.split('_')[0])
        vector = image2Vec('testDigits/%s' % fileNameStr)
        result = classify0(vector, trainingMat, hwLabels, 3)
        print("the classifier came back with: %d, the real answer is: %d" % (result, classNum))
        if result != classNum:
            errorCount += 1
    print("\nthe total number of errors is: %d" % errorCount)
    print("\nthe total error rate is: %f" % (errorCount / float(mTest)))


# 第一个例子
# group, label = createDataSet()
# print(group)
# print(label)
# res = classify0([0, 0], group, label, 3)
# print(res)


# datingDataMat, datingLabels = file2matrix("datingTestSet2.txt")
# print(datingDataMat)
# print(datingLabels)
# a, b, c = autoNorm(datingDataMat)
# print(a)


# datingClassTest()
handWritingClassifier()

# 画图
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.scatter(group[:, 0], group[:, 1])
# plt.show()
