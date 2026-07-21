
from typing import List

DEBUG = False



def numToBit(n):
    if n == 0:
        return 0x1
    else:
        return 0x1 << n

idxBitList = []
for i in range(81*81):
    idxBitList.append(numToBit(i))

def conflict(pos1, pos2):
    # print(f"  pos1={pos1}  pos2={pos2}")

    if pos1[0] == pos2[0] or pos1[1] == pos2[1]: 
        return True
    return abs(pos1[0]-pos2[0]) == abs(pos1[1]-pos2[1])

def printBoard(matrix):            
    for row in matrix:
        print(' '.join(row))
    print()

class Solution:

   


    def solveNQueens(self, n: int) -> List[List[str]]:
        allPosList = []
        for i in range(n):
            for j in range(n):
                allPosList.append((i, j, len(allPosList))) 

        conflictPosIdxPairSet = set()
        conflictPosIdxPairList = []
        conflictBitPatternSet = set()

        friendlyPosIdxPairSet = set()
        friendlyPosIdxPairList = []

        # prefixIdxSet = set()
        bitPatternSet = set()
        succBitPatternSet = set()
        # deadEndBitPatternSet = set()

        totalShrinks = 0
        
        for i, pos1 in enumerate(allPosList):
            for j, pos2 in enumerate( allPosList):
                key = frozenset((i, j))
                if conflict(pos1, pos2):
                    conflictPosIdxPairSet.add(key)
                    conflictPosIdxPairList.append((i, j))
                    conflictBitPatternSet.add(idxBitList[i] | idxBitList[j])
                else:
                    friendlyPosIdxPairSet.add(key) 
                    friendlyPosIdxPairList.append((i, j))   

        def conflictIdx(i, j):
            return (idxBitList[i] | idxBitList[j]) in conflictBitPatternSet

        if DEBUG:
            print(f" conflictPosIdxPairSet size={len(conflictPosIdxPairSet)} friendlyPosIdxPairSet size={len(friendlyPosIdxPairSet)}")

        
        if n == 1:
            return [["Q"]]

        if n == 2 or n == 3:
            return [ ]    
          
        result = []

        def placeQueenRecursively(availablePosList, depth, friendlyPosList, bitPattern):
            nonlocal totalShrinks

            if DEBUG:
                print(f" depth={depth} friendlyPosList={friendlyPosList} availablePosList={availablePosList}")
                print(f" depth={depth} bitPatternSet size={len(bitPatternSet)} succBitPatternSet size={len(succBitPatternSet)}")

            if depth >= n:
                if bitPattern in succBitPatternSet:
                    if DEBUG:
                        print(f" duplicate result")   
                else:         
                    board = [["." for j in range(n)] for i in range(n)]

                    for idx in range(n*n):
                        if idxBitList[idx] & bitPattern > 0:
                            p = allPosList[idx]
                            board[p[0]][p[1]] = 'Q'

                    if DEBUG:
                        printBoard(board)

                    ret = [''.join(row) for row in board]
                    result.append(ret)   
                    succBitPatternSet.add(bitPattern)
                return True

            isDeadEnd = True

            for i in range(len(availablePosList)):
                nextPos = availablePosList[i]
                nextBitPattern = bitPattern | idxBitList[nextPos[2]]


                # if all( not conflictIdx(nextPos[2], p[2])  for p in friendlyPosList):
                if True:
                    friendL2 = friendlyPosList
                    if nextBitPattern in bitPatternSet:
                        if DEBUG:
                            print(f"  skip tried prefix {friendL2} size={len(friendL2)}")
                        continue

                    availL2 = [x for x in availablePosList if not conflictIdx(x[2], nextPos[2])]
                    totalShrinks += len(availablePosList)-len(availL2)
                    if DEBUG:
                        print(f"  shrink available list by {len(availablePosList)-len(availL2)}")
                    # del availL2[i: i+1]
                    if placeQueenRecursively(availL2, depth+1, friendL2, nextBitPattern):
                        isDeadEnd = False
            bitPatternSet.add(bitPattern)    
        
        for p in allPosList:
            if p[0] <= p[1]:  # solutions are symmetric so try half of them
                depth = 1
                friendlyPosList=[]
                availablePosList = [x for x in allPosList if not conflict(x, p) ]
                placeQueenRecursively(availablePosList, depth, friendlyPosList, idxBitList[p[2]])

        if DEBUG:
            print(f"total shrinks = {totalShrinks}")        

        return result   