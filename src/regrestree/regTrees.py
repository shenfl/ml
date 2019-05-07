import numpy as np


def loadDataSet(fileName):
    dataMat = []  # assume last column is target value
    fr = open(fileName)
    for line in fr.readlines():
        curLine = line.strip().split('\t')
        fltLine = list(map(float, curLine))
        dataMat.append(fltLine)
    return dataMat


def binSplitDataSet(dataSet, feature, value):
    mat0 = dataSet[np.nonzero(dataSet[:, feature] > value)[0], :]
    mat1 = dataSet[np.nonzero(dataSet[:, feature] <= value)[0], :]
    return mat0, mat1


def regLeaf(dataSet):
    return np.mean(dataSet[:, -1])


def regErr(dataSet):
    return np.var(dataSet[:, -1]) * np.shape(dataSet)[0]


def chooseBestSplit(dataSet, leafType=regLeaf, errType=regErr, ops=(1, 4)):
    tolS = ops[0]; tolN = ops[1]
    if len(set(dataSet[:, -1].T.tolist()[0])) == 1:
        return None, leafType(dataSet)
    m, n = np.shape(dataSet)
    S = errType(dataSet)
    bestS = float('inf'); bestIndex = 0; bestValue = 0
    for featIndex in range(n - 1):
        for splitVal in set(dataSet[:, featIndex].T.tolist()[0]):
            mat0, mat1 = binSplitDataSet(dataSet, featIndex, splitVal)
            if (np.shape(mat0)[0]) < tolN or (np.shape(mat1)[0]) < tolN:
                continue
            newS = errType(mat0) + errType(mat1)
            if newS < bestS:
                bestIndex = featIndex
                bestValue = splitVal
                bestS = newS
    if (S - bestS) < tolS:
        return None, leafType(dataSet)
    mat0, mat1 = binSplitDataSet(dataSet, bestIndex, bestValue)
    if (np.shape(mat0)[0]) < tolN or (np.shape(mat1)[0]) < tolN:
        return None, leafType(dataSet)
    return bestIndex, bestValue


def createTree(dataSet, leafType=regLeaf, errorType=regErr, ops=(1, 4)):
    feat, val = chooseBestSplit(dataSet, leafType, errorType, ops)
    if feat is None:
        return val
    retTree = {'spInd': feat, 'spVal': val}
    lSet, rSet = binSplitDataSet(dataSet, feat, val)
    retTree['left'] = createTree(lSet, leafType, errorType, ops)
    retTree['right'] = createTree(rSet, leafType, errorType, ops)
    return retTree


def isTree(obj):
    return type(obj).__name__ == 'dict'


def getMean(tree):
    if isTree(tree['right']):
        tree['right'] = getMean(tree['right'])
    if isTree(tree['left']):
        tree['left'] = getMean(tree['left'])
    return (tree['left'] + tree['right']) / 2


def prune(tree, testData):
    if np.shape(testData)[0] == 0:
        return getMean(tree)
    if isTree(tree['left']) or isTree(tree['right']):
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
        if isTree(tree['left']):
            tree['left'] = prune(tree['left'], lSet)
        if isTree(tree['right']):
            tree['right'] = prune(tree['right'], rSet)
    if not isTree(tree['left']) and not isTree(tree['right']):
        lSet, rSet = binSplitDataSet(testData, tree['spInd'], tree['spVal'])
        errorNoMerge = sum(np.power(lSet[:, -1] - tree['left'], 2)) + sum(np.power(lSet[:, -1] - tree['right'], 2))
        treeMean = (tree['left'] + tree['right']) / 2
        errorMerge = sum(np.power(testData[:, -1] - treeMean, 2))
        if errorMerge < errorNoMerge:
            print('merging')
            return treeMean
        else:
            return tree
    else:
        return tree


testMat = np.mat(np.eye(4))
mat0, mat1 = binSplitDataSet(testMat, 1, 0.5)
print(mat0)
print('----------')
print(mat1)
print('-----')
a = np.mat([[1, 1, 0], [0, 0, 0], [0, 0, 0]])
b = np.nonzero(a)
print(b)
print(b[0])
print(testMat[:, 1] > 0.5)
myData = loadDataSet('ex00.txt')
myMat = np.mat(myData)
tree = createTree(myMat)
print(tree)

myMat = np.mat(loadDataSet('ex0.txt'))
tree = createTree(myMat)
print(tree)

myMat = np.mat(loadDataSet('ex2.txt'))
tree = createTree(myMat, ops=(0, 1))
print(tree)
fi = prune(tree, np.mat(loadDataSet('ex2test.txt')))
print(fi)
