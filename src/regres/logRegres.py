import numpy as np


def loadData():
    dataMat = []; labelMat = []
    fr = open('testSet.txt')
    for line in fr.readlines():
        lineArr = line.strip().split()
        dataMat.append([1.0, float(lineArr[0]), float(lineArr[1])])
        labelMat.append(int(lineArr[2]))
    return dataMat, labelMat


def sigmoid(inX):
    return 1.0 / (1 + np.exp(-inX))


def gradAscent(dataMatIn, classLabels):
    dataMatrix = np.mat(dataMatIn)
    classMatrix = np.mat(classLabels).transpose()
    m, n = np.shape(dataMatrix)
    alpha = 0.001
    weights = np.ones((n, 1))
    for i in range(500):
        h = sigmoid(dataMatrix * weights)
        error = classMatrix - h
        weights = weights + alpha * dataMatrix.transpose() * error
    return weights


def printBestFit(wei):
    import matplotlib.pyplot as plt
    weight = wei.getA()
    dataMat, labelMat = loadData()
    n = len(dataMat)
    x1 = []; y1 = []
    x2 = []; y2 = []
    for i in range(n):
        if int(labelMat[i]) == 1:
            x1.append(dataMat[i][1]); y1.append(dataMat[i][2])
        else:
            x2.append(dataMat[i][1]); y2.append(dataMat[i][2])
    flg = plt.figure()
    ax = flg.add_subplot(111)
    ax.scatter(x1, y1, s=30, c='red', marker='s')
    ax.scatter(x2, y2, s=30, c='green')
    x = np.arange(-3, 3, 0.1)
    y = (-weight[0] - weight[1] * x) / weight[2]
    ax.plot(x, y)
    plt.xlabel('X1'); plt.ylabel('X2')
    plt.show()


data, label = loadData()
weight = gradAscent(data, label)
print(weight)
printBestFit(weight)


print(np.ones((10, 1)).transpose())
