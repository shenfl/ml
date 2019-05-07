import numpy as np


def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]
    return postingList, classVec


def createVocabList(dataSet):
    returnVec = set([])
    for data in dataSet:
        returnVec = returnVec | set(data)
    return list(returnVec)


def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print("the word %s is not in vocab" % word)
    return returnVec


def train(trainMetrix, trainCategory):
    numTrainDocs = len(trainMetrix)
    numWords = len(trainMetrix[0])
    pAbusive = sum(trainCategory) / float(numTrainDocs)
    p0num = np.ones(numWords); p1num = np.ones(numWords)
    p0denom = 2.0; p1denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1num += trainMetrix[i]
            p1denom += sum(trainMetrix[i])
        else:
            p0num += trainMetrix[i]
            p0denom += sum(trainMetrix[i])
    p1Vec = np.log(p1num / p1denom)
    p0Vec = np.log(p0num / p0denom)
    return p0Vec, p1Vec, pAbusive


def classifyNB(vec, p0vec, p1vec, pclass1):
    p1 = sum(vec * p1vec) + np.log(pclass1)
    p0 = sum(vec * p0vec) + np.log(1 - pclass1)
    if p1 > p0:
        return 1
    else:
        return 0


def testingNB():
    listData, listClasses = loadDataSet()
    myVectorList = createVocabList(listData)
    trainMat = []
    for doc in listData:
        trainMat.append(setOfWords2Vec(myVectorList, doc))
    p0v, p1v, pab = train(trainMat, listClasses)
    testEntry = ['love', 'my', 'dalmation']
    thisVec = setOfWords2Vec(myVectorList, testEntry)
    print(thisVec)
    cls = classifyNB(thisVec, p0v, p1v, pab)
    print(cls)
    testEntry = ['stupid', 'garbage']
    thisVec = setOfWords2Vec(myVectorList, testEntry)
    print(thisVec)
    cls = classifyNB(thisVec, p0v, p1v, pab)
    print(cls)


testingNB()
# listData, listClasses = loadDataSet()
# print(listData)
# print(listClasses)
# myVectorList = createVocabList(listData)
# print(myVectorList)
# vec = setOfWords2Vec(myVectorList, listData[0])
# print(vec)
#
#
# trainMat = []
# for doc in listData:
#     trainMat.append(setOfWords2Vec(myVectorList, doc))
# p0v, p1v, pab = train(trainMat, listClasses)
# print(p0v)
# print(p1v)
# print(pab)
