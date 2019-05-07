class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        print("\t" * ind, self.name, '\t', self.count)
        for child in self.children.values():
            child.disp(ind + 1)


# rootNode = treeNode('pyramid', 9, None)
# rootNode.disp()
# rootNode.children['eye'] = treeNode('eye', 13, None)
# rootNode.disp()

def createTree(dataSet, nimSup=1):
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]
    delset = set()
    for k in headerTable.keys():
        if headerTable[k] < nimSup:
                delset.add(k)
    for item in delset:
        del(headerTable[item])
    freqItemSet = set(headerTable.keys())
    if len(freqItemSet) == 0:
        return None, None
    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree = treeNode('Null set', 1, None)
    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderdItems = [v[0] for v in sorted(localD.items(), key=lambda p: p[1], reverse=True)]
            updateTree(orderdItems, retTree, headerTable, count)
    return retTree, headerTable


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] is None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
    if len(items) > 1:
        updateTree(items[1::], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):
    while nodeToTest.nodeLink is not None:
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def loadSimpData():
    simpData = [['r', 'z', 'h', 'j', 'p'],
                ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
                ['z'],
                ['r', 'x', 'n', 'o', 's'],
                ['y', 'r', 'x', 'z', 'q', 't', 'p'],
                ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpData


def createInitSet(dataSet):
    retDict = {}
    for tran in dataSet:
        retDict[frozenset(tran)] = 1
    return retDict


def findPrefixPath(basePat, treeNode):
    condPats = {}
    while treeNode is not None:
        prefixPath = []
        ascentTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


def ascentTree(leafNode, prefixPath):
    if leafNode.parent is not None:
        prefixPath.append(leafNode.name)
        ascentTree(leafNode.parent, prefixPath)


def mineTree(inTree, headerTable, minSup, prefix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1][0])]
    for basePat in bigL:
        newFreqSet = prefix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(newFreqSet)
        condPattBase = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead = createTree(condPattBase, minSup)
        if myHead is not None:
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)


initSet = createInitSet(loadSimpData())
print(initSet)
tree, table = createTree(initSet, 3)
tree.disp()
condPath = findPrefixPath('r', table['r'][1])
print(condPath)
freqItem = []
mineTree(tree, table, 3, set([]), freqItem)
print(freqItem)


parsedDat = [line.split() for line in open('kosarak.dat').readlines()]
initSet = createInitSet(parsedDat)
myTree, myTable = createTree(initSet, 100000)
myFreqList = []
mineTree(myTree, myTable, 100000, set([]), myFreqList)
print(myFreqList)
