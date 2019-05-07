from math import log


def calcShanonEnt(dataSet):
    number = len(dataSet)
    labelCounts = {}
    for data in dataSet:
        currentLabel = data[-1]
        if currentLabel not in labelCounts.keys():
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannon = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key]) / number
        shannon -= prob * log(prob, 2)
    return shannon


def createDataSet():
    dataSet = [
        [1, 1, 'yes'],
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 1, 'no']
    ]
    labels = ['no suf', 'flippers']
    return dataSet, labels


def splitDataSet(dataSet, axis, value):
    result = []
    for vec in dataSet:
        if vec[axis] == value:
            reduce = vec[:axis]
            reduce.extend(vec[axis + 1:])
            result.append(reduce)
    return result


def chooseBestFeature(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseValue = calcShanonEnt(dataSet)
    baseGain = 0.0; bestFeature = -1
    for i in range(numFeatures):
        valueList = [example[i] for example in dataSet]
        unique = set(valueList)
        new = 0.0
        for value in unique:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            new += prob * calcShanonEnt(subDataSet)
        gain = baseValue - new
        if gain > baseGain:
            baseGain = gain
            bestFeature = i
    return bestFeature


def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] +=1
    sorted(classCount.items(), key=lambda x: x[1], reverse=true)
    return classCount[0][0]


def createTree(dataSet, lables):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(classList[0]) == 1:
        return majorityCnt(classList)
    bestFeat = chooseBestFeature(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueValues = set(featValues)
    for value in uniqueValues:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree


myMat, labels = createDataSet()
print(myMat)
print(labels)
print(calcShanonEnt(myMat))
print(splitDataSet(myMat, 0, 0))
print(chooseBestFeature(myMat))
print(createTree(myMat, labels))
