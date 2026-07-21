
from typing import List
import math

DEBUG = False



def numToBit(n):
    if n == 0:
        return 0x1
    else:
        return 0x1 << n

def lowest_set_bit(p):
    if p == 0:
        return 0
    return p & -p

def bitPatternToStr(bitPattern, size):
    return bin(bitPattern)[2:].zfill(size)

def splitBitPattern(pattern):
    bitList = []
    while pattern:
        bit = pattern & -pattern
        bitList.append(bit)
        pattern &= pattern - 1  
    return bitList 

def flipBitPattern(pattern, n):
    """Treat pattern as an n-bit pattern and flip all bits.  (~p) & ((1 << n) - 1)"""
    mask = (1 << n) - 1
    return (~pattern) & mask

    

def conflict(pos1, pos2):
    # print(f"  pos1={pos1}  pos2={pos2}")

    if pos1[0] == pos2[0] or pos1[1] == pos2[1]: 
        return True
    return abs(pos1[0]-pos2[0]) == abs(pos1[1]-pos2[1])

def printBoard(matrix):            
    for row in matrix:
        print(' '.join(row))
    print()

def saveBoardToFile(matrix, fileName):   
    """append matrix to the given file"""         
    with open(fileName, 'a', encoding='utf-8') as f:
        for row in matrix:
            f.write(' '.join(row) + '\n')
        f.write('\n\n')

def removeBoardFile(fileName):
    """delete the board result file"""
    from pathlib import Path
    Path(fileName).unlink(missing_ok=True)



class Solution:

    def solveNQueens(self, n: int) -> List[List[str]]:
        boardFileName = f"leetcode-17-{n}.result"

        if DEBUG:
            removeBoardFile(boardFileName)

        idxBitList = []
        idxFlipBitList = []
        bitToIdxMap = {}

        def printBoardPattern(boardPattern):
            for i in range(n):
                line = []
                for j in range(n):
                    if boardPattern & idxBitList[i * n + j] > 0:
                        line.append('*')
                    else:
                        line.append('_')
                print(" ".join(line))
            print()


        for i in range(n * n):
            idxBitList.append(numToBit(i))
            idxFlipBitList.append(~numToBit(i))
            bitToIdxMap[numToBit(i)] = i
            if DEBUG:
                print(f" idxList[{i:02}]={bitPatternToStr(idxBitList[i], n*n)}")
           
        if DEBUG:
            bits = 0x1
            print(f"   test printBoardPattern({bitPatternToStr(bits, n*n)})")
            printBoardPattern(bits)

            bits = 0x1 | 0x1 << 8
            print(f"   test printBoardPattern({bitPatternToStr(bits, n*n)})")
            printBoardPattern(bits)



        allPosList = []
        for i in range(n):
            for j in range(n):
                allPosList.append((i, j, len(allPosList))) 

        exhustedBitPatternSet = set()
        succBitPatternSet = set()
        shortExhustedBitPatternSet = set()
        

        idxMaskBitsList = []  # bit masks representing positions blocked by a given Q
        idxMaskFlipBitsList = []  # bit masks representing positions blocked by a given Q
        # idxUnmaskBitsList = []
        allMaskedBits = 0  # n x n 1's bits
        for i in range(n*n):
            maskBits = 0
            allMaskedBits = allMaskedBits | idxBitList[i]
            for j in range(n*n):
                if conflict(allPosList[i], allPosList[j]):
                    maskBits = maskBits | idxBitList[j]
                    if DEBUG and i != j:
                        print(f"  pos1 {allPosList[i]} conflicts pos2 {allPosList[j]} bits={bitPatternToStr(idxBitList[j], n*n)}")

            idxMaskBitsList.append(maskBits)
            idxMaskFlipBitsList.append(~maskBits)
            if DEBUG:
                print(f" mask bits idx={i:02} {bitPatternToStr(maskBits, n*n)}")
                printBoardPattern(maskBits)


        if n == 1:
            return [["Q"]]

        if n == 2 or n == 3:
            return [ ]    
          
        result = []

        result2 = []
       
        def placeQueens(boardPattern, flipBoardPattern, depth, partialSolutions):
            """
            partialSolutions: bits of a given solution
            """
            if DEBUG:
                print(f" depth={depth} boardPattern:")
                printBoardPattern(boardPattern)
                printBoardPattern(partialSolutions)

            foundSolution = False
            if depth >= n:
                foundSolution = True
                if partialSolutions in succBitPatternSet:
                    if DEBUG:
                        print(f" duplicate result")   
                else:         
                    board = [["." for j in range(n)] for i in range(n)]

                    posList = []

                    for bit in splitBitPattern(partialSolutions):
                        idx = bitToIdxMap[bit]
                        p = allPosList[idx]
                        posList.append([p[0], p[1]])
                        board[p[0]][p[1]] = 'Q'

                    result2.append(posList)    

                    if DEBUG:
                        print(f" ADD unique solution {len(succBitPatternSet)}:")
                        printBoard(board)
                        saveBoardToFile(board, boardFileName)

                    ret = [''.join(row) for row in board]
                    result.append(ret)   
                    succBitPatternSet.add(partialSolutions)                    
            else:
                if boardPattern != allMaskedBits:
                    availableBits = flipBoardPattern

                    while availableBits > 0:
                        singleBit = lowest_set_bit(availableBits) # first available
                        k = bitToIdxMap[singleBit]  
                        kMaskBits = idxMaskBitsList[k]
                        partialSol = kMaskBits & ~boardPattern # remove existig bits

                        if partialSol > 0:
                            partialSolutions2 = partialSolutions | singleBit
                            if partialSolutions2 not in exhustedBitPatternSet:
                                boardPattern2 = boardPattern | kMaskBits 
                                flipBoardPattern2 = flipBoardPattern & (idxMaskFlipBitsList[k])
                                if placeQueens(boardPattern2, flipBoardPattern2, depth+1, partialSolutions2):
                                    foundSolution = True
                            else:
                                if DEBUG:
                                    print(f" depth={depth} skip tried partial solution")        
                        else:
                            None # shouldn't happen                            

                        availableBits =  availableBits & ~singleBit    
                else:
                    if DEBUG:
                        print(f" depth={depth} DEAD END")

            exhustedBitPatternSet.add(partialSolutions)
            if depth == 1:
                shortExhustedBitPatternSet.add(partialSolutions)
            if DEBUG:
                print(f"  exhustedBitPatternSet size={len(exhustedBitPatternSet)}")
            if not foundSolution:
                if DEBUG:
                    print(f" depth={depth} No solutions")


            return foundSolution

        def placeQRecursively(boardPattern, flipBoardPattern, depth, bitPattern, nextPosIdx):
            """
            boardPattern: positions conflict with bitPattern or positions that can not be used
            flipBoardPattern: mark positions do not conflict with bitPattern yet
            """
            if DEBUG:
                bitPatternStr = bitPatternToStr(bitPattern, n*n)

                print(f"   depth={depth} bitPattern (bin): {bitPatternStr} flipBoardPattern={bitPatternToStr(flipBoardPattern, n*n)} nextPosIdx={nextPosIdx}")
                printBoardPattern(boardPattern)
                print(f" bit pattern")
                printBoardPattern(bitPattern)
       
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

                exhustedBitPatternSet.add(bitPattern)
                return # no need to try
                
            if boardPattern != allMaskedBits:
                # find all next 0 bits in boardPattern starting from nextPosIdx
                # availableBits = flipBoardPattern

                # it is slower
                # while availableBits > 0:
                #     singleBit = lowest_set_bit(availableBits)
                #     bitPattern2 = bitPattern | singleBit
                #     k = bitToIdxMap[singleBit]  
                #     if DEBUG:
                #         print(f" depth={depth} k={k} singleBit={bitPatternToStr(singleBit, n*n)}")

                #     if bitPattern2 in bitPatternSet:
                #         if DEBUG:
                #             print(f"  skip tried prefix {bitPatternToStr(bitPattern2, n*n)}")
                #     else:
                #         boardPattern2 = boardPattern | idxMaskBitsList[k] 
                #         flipBoardPattern2 = flipBoardPattern & (idxMaskFlipBitsList[k])
                #         # given (k, nextPosIdx, boardPattern2, bitPattern2), what is the optimal next jump?
                #         # any position before nextPosIdx is not available

                #         row = k // n
                #         nextPosIdx2 = (row+1)*n
                #         if col > 0:
                #             nextPosIdx2 += 1
                #         nextPosIdx2 = max(nextPosIdx2, k+1)    
                #         if DEBUG:
                #             print(f"  nextPosIdx jumps {nextPosIdx2-k} ")

                #         # this call will explore all solutions starts from bitPattern2             
                #         placeQRecursively(boardPattern2, flipBoardPattern2, depth+1, bitPattern2, nextPosIdx2) 
                    
                #     availableBits = availableBits & idxFlipBitList[k]   


                k = nextPosIdx
                while k < n * n:
                    # suppose the while tries k = k1 < k2 < k3. 
                    # the solutions tried by k1 might or might not include k2.
                    # A. if solutions tried by k1 include k2, then k1 and k2 do not conflict. k2 -> k1 solution will be skipped 
                    # B. if solutions tried byh k1 does not include k2, then k1 and k2 conflict. k2 -> k1 solution wont happen
                    #    there could one solution includes k1; another solution includes k2
                    # In either case A or B, when could ignore k1 when handling k2
                    singleBit = idxBitList[k]
                    if boardPattern & singleBit == 0:
                        bitPattern2 = bitPattern | singleBit  
                        if bitPattern2 in exhustedBitPatternSet:
                            if DEBUG:
                                print(f"  skip tried prefix {bitPatternToStr(bitPattern2, n*n)}")
                        else:
                            boardPattern2 = boardPattern | idxMaskBitsList[k] 
                            flipBoardPattern2 = flipBoardPattern & (idxMaskFlipBitsList[k])
                            
                            # given (k, nextPosIdx, boardPattern2, bitPattern2), what is the optimal next jump?
                            # any position before nextPosIdx is not available

                            row = k // n
                            col = k % n
                            nextPosIdx2 = (row+1)*n
                            if col == 0:
                                nextPosIdx2 += 1

                            # if flipBoardPattern2 > 0:
                            #     m = bitToIdxMap[lowest_set_bit(flipBoardPattern2)]
                            #     if m > nextPosIdx2:
                            #         if DEBUG:
                            #             print(f"  adjust nextPosIdx2 by {m-nextPosIdx2} flipBoardPattern2")
                            #         nextPosIdx2 = m
                                    
                            # if col > 0:
                            #     nextPosIdx2 += 1
                            # nextPosIdx2 = max(nextPosIdx2, k+1)    
                            if DEBUG:
                                print(f"  nextPosIdx jumps {nextPosIdx2-k} ")

                            # this call will explore all solutions starts from bitPattern2             
                            placeQRecursively(boardPattern2, flipBoardPattern2, depth+1, bitPattern2, nextPosIdx2)   
                                                
                    k += 1    
            else: # deadend
                if DEBUG:
                    print(f"  DEAD END: board is full")

            exhustedBitPatternSet.add(bitPattern)

            return


        # for p in allPosList:
        #     row, col, idx = p
        #     if row <= col:  # solutions are symmetric so try half of them
        #         depth = 1
        #         boardPattern = idxMaskBitsList[idx]  # ints are immutable in Python
        #         flipBoardPattern = flipBitPattern(boardPattern, n*n)
        #         bitPattern = idxBitList[idx]
        #         nextPosIdx = idx+1 # 0 if col >0 else 0
        #         if row == 0:
        #             if col == 0:
        #                 nextPosIdx = n + 1
        #             else:   
        #                 nextPosIdx = n

        #         placeQRecursively(boardPattern, flipBoardPattern, depth, bitPattern, nextPosIdx)

        for p in allPosList:
            row, col, idx = p
            if row <= col and row <= math.ceil(n/2) and col <= math.ceil(n/2):
                depth = 1
                boardPattern = idxMaskBitsList[idx]  # ints are immutable in Python
                flipBoardPattern = flipBitPattern(boardPattern, n*n)
                for pattern in shortExhustedBitPatternSet:
                    flipBoardPattern = flipBoardPattern & ~pattern # these positions are done
                partialSolutions = idxBitList[idx]

                if not placeQueens(boardPattern, flipBoardPattern, depth, partialSolutions):
                    if DEBUG:
                        print(f" depth={depth} No solutions")
        if DEBUG:
            print(f"num of unique solutions={len(result)}")


        return result        


if __name__ == '__main__':
    import sys

    DEBUG = False
    selected_tests = None  # None: run all; else set of 1-based indices from argv

    for a in sys.argv[1:]:
        if a == "-d":
            DEBUG = True
        elif a.replace(",", "").isdigit() and "," in a:
            if selected_tests is None:
                selected_tests = set()
            for part in a.split(","):
                part = part.strip()
                if part.isdigit():
                    selected_tests.add(int(part))
        elif a.isdigit():
            if selected_tests is None:
                selected_tests = set()
            selected_tests.add(int(a))
        else:
            print(
                f"Unknown argument: {a!r} (use -d and/or 1-based test indices, e.g. 1 2 4)",
                file=sys.stderr,
            )
            sys.exit(2)

    if selected_tests is not None and len(selected_tests) == 0:
        print("Test selection is empty.", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"selected_tests={selected_tests}")    

    tests = [
        {
            "n": 1, 
            "expected": [["Q"]]
        },
        {
            "n": 2, 
            "expected": []
        },
        {
            "n": 3, 
            "expected": []
        },
        {
            "n": 4,
            "expected": [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]],
        },
        {
            "n": 5,
            "expected": [["Q....","..Q..","....Q",".Q...","...Q."],["Q....","...Q.",".Q...","....Q","..Q.."],[".Q...","...Q.","Q....","..Q..","....Q"],[".Q...","....Q","..Q..","Q....","...Q."],["..Q..","Q....","...Q.",".Q...","....Q"],["..Q..","....Q",".Q...","...Q.","Q...."],["...Q.","Q....","..Q..","....Q",".Q..."],["...Q.",".Q...","....Q","..Q..","Q...."],["....Q",".Q...","...Q.","Q....","..Q.."],["....Q","..Q..","Q....","...Q.",".Q..."]],
        },
        {
            "n": 6,
            "expected":  [['.Q....', '...Q..', '.....Q', 'Q.....', '..Q...', '....Q.'], ['..Q...', '.....Q', '.Q....', '....Q.', 'Q.....', '...Q..'], ['...Q..', 'Q.....', '....Q.', '.Q....', '.....Q', '..Q...'], ['....Q.', '..Q...', 'Q.....', '.....Q', '...Q..', '.Q....']]
        },
        {
        "n": 7,
        "expected":   [['Q......', '..Q....', '....Q..', '......Q', '.Q.....', '...Q...', '.....Q.'], ['Q......', '...Q...', '......Q', '..Q....', '.....Q.', '.Q.....', '....Q..'], ['Q......', '....Q..', '.Q.....', '.....Q.', '..Q....', '......Q', '...Q...'], ['Q......', '.....Q.', '...Q...', '.Q.....', '......Q', '....Q..', '..Q....'], ['.Q.....', '...Q...', 'Q......', '......Q', '....Q..', '..Q....', '.....Q.'], ['.Q.....', '...Q...', '.....Q.', 'Q......', '..Q....', '....Q..', '......Q'], ['.Q.....', '....Q..', 'Q......', '...Q...', '......Q', '..Q....', '.....Q.'], ['.Q.....', '....Q..', '..Q....', 'Q......', '......Q', '...Q...', '.....Q.'], ['.Q.....', '....Q..', '......Q', '...Q...', 'Q......', '..Q....', '.....Q.'], ['.Q.....', '.....Q.', '..Q....', '......Q', '...Q...', 'Q......', '....Q..'], ['.Q.....', '......Q', '....Q..', '..Q....', 'Q......', '.....Q.', '...Q...'], ['..Q....', 'Q......', '.....Q.', '.Q.....', '....Q..', '......Q', '...Q...'], ['..Q....', 'Q......', '.....Q.', '...Q...', '.Q.....', '......Q', '....Q..'], ['..Q....', '....Q..', '......Q', '.Q.....', '...Q...', '.....Q.', 'Q......'], ['..Q....', '.....Q.', '.Q.....', '....Q..', 'Q......', '...Q...', '......Q'], ['..Q....', '......Q', '.Q.....', '...Q...', '.....Q.', 'Q......', '....Q..'], ['..Q....', '......Q', '...Q...', 'Q......', '....Q..', '.Q.....', '.....Q.'], ['...Q...', 'Q......', '..Q....', '.....Q.', '.Q.....', '......Q', '....Q..'], ['...Q...', 'Q......', '....Q..', '.Q.....', '.....Q.', '..Q....', '......Q'], ['...Q...', '.Q.....', '......Q', '....Q..', '..Q....', 'Q......', '.....Q.'], ['...Q...', '.....Q.', 'Q......', '..Q....', '....Q..', '......Q', '.Q.....'], ['...Q...', '......Q', '..Q....', '.....Q.', '.Q.....', '....Q..', 'Q......'], ['...Q...', '......Q', '....Q..', '.Q.....', '.....Q.', 'Q......', '..Q....'], ['....Q..', 'Q......', '...Q...', '......Q', '..Q....', '.....Q.', '.Q.....'], ['....Q..', 'Q......', '.....Q.', '...Q...', '.Q.....', '......Q', '..Q....'], ['....Q..', '.Q.....', '.....Q.', '..Q....', '......Q', '...Q...', 'Q......'], ['....Q..', '..Q....', 'Q......', '.....Q.', '...Q...', '.Q.....', '......Q'], ['....Q..', '......Q', '.Q.....', '...Q...', '.....Q.', 'Q......', '..Q....'], ['....Q..', '......Q', '.Q.....', '.....Q.', '..Q....', 'Q......', '...Q...'], ['.....Q.', 'Q......', '..Q....', '....Q..', '......Q', '.Q.....', '...Q...'], ['.....Q.', '.Q.....', '....Q..', 'Q......', '...Q...', '......Q', '..Q....'], ['.....Q.', '..Q....', 'Q......', '...Q...', '......Q', '....Q..', '.Q.....'], ['.....Q.', '..Q....', '....Q..', '......Q', 'Q......', '...Q...', '.Q.....'], ['.....Q.', '..Q....', '......Q', '...Q...', 'Q......', '....Q..', '.Q.....'], ['.....Q.', '...Q...', '.Q.....', '......Q', '....Q..', '..Q....', 'Q......'], ['.....Q.', '...Q...', '......Q', 'Q......', '..Q....', '....Q..', '.Q.....'], ['......Q', '.Q.....', '...Q...', '.....Q.', 'Q......', '..Q....', '....Q..'], ['......Q', '..Q....', '.....Q.', '.Q.....', '....Q..', 'Q......', '...Q...'], ['......Q', '...Q...', 'Q......', '....Q..', '.Q.....', '.....Q.', '..Q....'], ['......Q', '....Q..', '..Q....', 'Q......', '.....Q.', '...Q...', '.Q.....']]
        },
        {
            "n": 8,
            "expected":  [['Q.......', '....Q...', '.......Q', '.....Q..', '..Q.....', '......Q.', '.Q......', '...Q....'], ['Q.......', '.....Q..', '.......Q', '..Q.....', '......Q.', '...Q....', '.Q......', '....Q...'], ['Q.......', '......Q.', '...Q....', '.....Q..', '.......Q', '.Q......', '....Q...', '..Q.....'], ['Q.......', '......Q.', '....Q...', '.......Q', '.Q......', '...Q....', '.....Q..', '..Q.....'], ['.Q......', '...Q....', '.....Q..', '.......Q', '..Q.....', 'Q.......', '......Q.', '....Q...'], ['.Q......', '....Q...', '......Q.', 'Q.......', '..Q.....', '.......Q', '.....Q..', '...Q....'], ['.Q......', '....Q...', '......Q.', '...Q....', 'Q.......', '.......Q', '.....Q..', '..Q.....'], ['.Q......', '.....Q..', 'Q.......', '......Q.', '...Q....', '.......Q', '..Q.....', '....Q...'], ['.Q......', '.....Q..', '.......Q', '..Q.....', 'Q.......', '...Q....', '......Q.', '....Q...'], ['.Q......', '......Q.', '..Q.....', '.....Q..', '.......Q', '....Q...', 'Q.......', '...Q....'], ['.Q......', '......Q.', '....Q...', '.......Q', 'Q.......', '...Q....', '.....Q..', '..Q.....'], ['.Q......', '.......Q', '.....Q..', 'Q.......', '..Q.....', '....Q...', '......Q.', '...Q....'], ['..Q.....', 'Q.......', '......Q.', '....Q...', '.......Q', '.Q......', '...Q....', '.....Q..'], ['..Q.....', '....Q...', '.Q......', '.......Q', 'Q.......', '......Q.', '...Q....', '.....Q..'], ['..Q.....', '....Q...', '.Q......', '.......Q', '.....Q..', '...Q....', '......Q.', 'Q.......'], ['..Q.....', '....Q...', '......Q.', 'Q.......', '...Q....', '.Q......', '.......Q', '.....Q..'], ['..Q.....', '....Q...', '.......Q', '...Q....', 'Q.......', '......Q.', '.Q......', '.....Q..'], ['..Q.....', '.....Q..', '.Q......', '....Q...', '.......Q', 'Q.......', '......Q.', '...Q....'], ['..Q.....', '.....Q..', '.Q......', '......Q.', 'Q.......', '...Q....', '.......Q', '....Q...'], ['..Q.....', '.....Q..', '.Q......', '......Q.', '....Q...', 'Q.......', '.......Q', '...Q....'], ['..Q.....', '.....Q..', '...Q....', 'Q.......', '.......Q', '....Q...', '......Q.', '.Q......'], ['..Q.....', '.....Q..', '...Q....', '.Q......', '.......Q', '....Q...', '......Q.', 'Q.......'], ['..Q.....', '.....Q..', '.......Q', 'Q.......', '...Q....', '......Q.', '....Q...', '.Q......'], ['..Q.....', '.....Q..', '.......Q', 'Q.......', '....Q...', '......Q.', '.Q......', '...Q....'], ['..Q.....', '.....Q..', '.......Q', '.Q......', '...Q....', 'Q.......', '......Q.', '....Q...'], ['..Q.....', '......Q.', '.Q......', '.......Q', '....Q...', 'Q.......', '...Q....', '.....Q..'], ['..Q.....', '......Q.', '.Q......', '.......Q', '.....Q..', '...Q....', 'Q.......', '....Q...'], ['..Q.....', '.......Q', '...Q....', '......Q.', 'Q.......', '.....Q..', '.Q......', '....Q...'], ['...Q....', 'Q.......', '....Q...', '.......Q', '.Q......', '......Q.', '..Q.....', '.....Q..'], ['...Q....', 'Q.......', '....Q...', '.......Q', '.....Q..', '..Q.....', '......Q.', '.Q......'], ['...Q....', '.Q......', '....Q...', '.......Q', '.....Q..', 'Q.......', '..Q.....', '......Q.'], ['...Q....', '.Q......', '......Q.', '..Q.....', '.....Q..', '.......Q', 'Q.......', '....Q...'], ['...Q....', '.Q......', '......Q.', '..Q.....', '.....Q..', '.......Q', '....Q...', 'Q.......'], ['...Q....', '.Q......', '......Q.', '....Q...', 'Q.......', '.......Q', '.....Q..', '..Q.....'], ['...Q....', '.Q......', '.......Q', '....Q...', '......Q.', 'Q.......', '..Q.....', '.....Q..'], ['...Q....', '.Q......', '.......Q', '.....Q..', 'Q.......', '..Q.....', '....Q...', '......Q.'], ['...Q....', '.....Q..', 'Q.......', '....Q...', '.Q......', '.......Q', '..Q.....', '......Q.'], ['...Q....', '.....Q..', '.......Q', '.Q......', '......Q.', 'Q.......', '..Q.....', '....Q...'], ['...Q....', '.....Q..', '.......Q', '..Q.....', 'Q.......', '......Q.', '....Q...', '.Q......'], ['...Q....', '......Q.', 'Q.......', '.......Q', '....Q...', '.Q......', '.....Q..', '..Q.....'], ['...Q....', '......Q.', '..Q.....', '.......Q', '.Q......', '....Q...', 'Q.......', '.....Q..'], ['...Q....', '......Q.', '....Q...', '.Q......', '.....Q..', 'Q.......', '..Q.....', '.......Q'], ['...Q....', '......Q.', '....Q...', '..Q.....', 'Q.......', '.....Q..', '.......Q', '.Q......'], ['...Q....', '.......Q', 'Q.......', '..Q.....', '.....Q..', '.Q......', '......Q.', '....Q...'], ['...Q....', '.......Q', 'Q.......', '....Q...', '......Q.', '.Q......', '.....Q..', '..Q.....'], ['...Q....', '.......Q', '....Q...', '..Q.....', 'Q.......', '......Q.', '.Q......', '.....Q..'], ['....Q...', 'Q.......', '...Q....', '.....Q..', '.......Q', '.Q......', '......Q.', '..Q.....'], ['....Q...', 'Q.......', '.......Q', '...Q....', '.Q......', '......Q.', '..Q.....', '.....Q..'], ['....Q...', 'Q.......', '.......Q', '.....Q..', '..Q.....', '......Q.', '.Q......', '...Q....'], ['....Q...', '.Q......', '...Q....', '.....Q..', '.......Q', '..Q.....', 'Q.......', '......Q.'], ['....Q...', '.Q......', '...Q....', '......Q.', '..Q.....', '.......Q', '.....Q..', 'Q.......'], ['....Q...', '.Q......', '.....Q..', 'Q.......', '......Q.', '...Q....', '.......Q', '..Q.....'], ['....Q...', '.Q......', '.......Q', 'Q.......', '...Q....', '......Q.', '..Q.....', '.....Q..'], ['....Q...', '..Q.....', 'Q.......', '.....Q..', '.......Q', '.Q......', '...Q....', '......Q.'], ['....Q...', '..Q.....', 'Q.......', '......Q.', '.Q......', '.......Q', '.....Q..', '...Q....'], ['....Q...', '..Q.....', '.......Q', '...Q....', '......Q.', 'Q.......', '.....Q..', '.Q......'], ['....Q...', '......Q.', 'Q.......', '..Q.....', '.......Q', '.....Q..', '...Q....', '.Q......'], ['....Q...', '......Q.', 'Q.......', '...Q....', '.Q......', '.......Q', '.....Q..', '..Q.....'], ['....Q...', '......Q.', '.Q......', '...Q....', '.......Q', 'Q.......', '..Q.....', '.....Q..'], ['....Q...', '......Q.', '.Q......', '.....Q..', '..Q.....', 'Q.......', '...Q....', '.......Q'], ['....Q...', '......Q.', '.Q......', '.....Q..', '..Q.....', 'Q.......', '.......Q', '...Q....'], ['....Q...', '......Q.', '...Q....', 'Q.......', '..Q.....', '.......Q', '.....Q..', '.Q......'], ['....Q...', '.......Q', '...Q....', 'Q.......', '..Q.....', '.....Q..', '.Q......', '......Q.'], ['....Q...', '.......Q', '...Q....', 'Q.......', '......Q.', '.Q......', '.....Q..', '..Q.....'], ['.....Q..', 'Q.......', '....Q...', '.Q......', '.......Q', '..Q.....', '......Q.', '...Q....'], ['.....Q..', '.Q......', '......Q.', 'Q.......', '..Q.....', '....Q...', '.......Q', '...Q....'], ['.....Q..', '.Q......', '......Q.', 'Q.......', '...Q....', '.......Q', '....Q...', '..Q.....'], ['.....Q..', '..Q.....', 'Q.......', '......Q.', '....Q...', '.......Q', '.Q......', '...Q....'], ['.....Q..', '..Q.....', 'Q.......', '.......Q', '...Q....', '.Q......', '......Q.', '....Q...'], ['.....Q..', '..Q.....', 'Q.......', '.......Q', '....Q...', '.Q......', '...Q....', '......Q.'], ['.....Q..', '..Q.....', '....Q...', '......Q.', 'Q.......', '...Q....', '.Q......', '.......Q'], ['.....Q..', '..Q.....', '....Q...', '.......Q', 'Q.......', '...Q....', '.Q......', '......Q.'], ['.....Q..', '..Q.....', '......Q.', '.Q......', '...Q....', '.......Q', 'Q.......', '....Q...'], ['.....Q..', '..Q.....', '......Q.', '.Q......', '.......Q', '....Q...', 'Q.......', '...Q....'], ['.....Q..', '..Q.....', '......Q.', '...Q....', 'Q.......', '.......Q', '.Q......', '....Q...'], ['.....Q..', '...Q....', 'Q.......', '....Q...', '.......Q', '.Q......', '......Q.', '..Q.....'], ['.....Q..', '...Q....', '.Q......', '.......Q', '....Q...', '......Q.', 'Q.......', '..Q.....'], ['.....Q..', '...Q....', '......Q.', 'Q.......', '..Q.....', '....Q...', '.Q......', '.......Q'], ['.....Q..', '...Q....', '......Q.', 'Q.......', '.......Q', '.Q......', '....Q...', '..Q.....'], ['.....Q..', '.......Q', '.Q......', '...Q....', 'Q.......', '......Q.', '....Q...', '..Q.....'], ['......Q.', 'Q.......', '..Q.....', '.......Q', '.....Q..', '...Q....', '.Q......', '....Q...'], ['......Q.', '.Q......', '...Q....', 'Q.......', '.......Q', '....Q...', '..Q.....', '.....Q..'], ['......Q.', '.Q......', '.....Q..', '..Q.....', 'Q.......', '...Q....', '.......Q', '....Q...'], ['......Q.', '..Q.....', 'Q.......', '.....Q..', '.......Q', '....Q...', '.Q......', '...Q....'], ['......Q.', '..Q.....', '.......Q', '.Q......', '....Q...', 'Q.......', '.....Q..', '...Q....'], ['......Q.', '...Q....', '.Q......', '....Q...', '.......Q', 'Q.......', '..Q.....', '.....Q..'], ['......Q.', '...Q....', '.Q......', '.......Q', '.....Q..', 'Q.......', '..Q.....', '....Q...'], ['......Q.', '....Q...', '..Q.....', 'Q.......', '.....Q..', '.......Q', '.Q......', '...Q....'], ['.......Q', '.Q......', '...Q....', 'Q.......', '......Q.', '....Q...', '..Q.....', '.....Q..'], ['.......Q', '.Q......', '....Q...', '..Q.....', 'Q.......', '......Q.', '...Q....', '.....Q..'], ['.......Q', '..Q.....', 'Q.......', '.....Q..', '.Q......', '....Q...', '......Q.', '...Q....'], ['.......Q', '...Q....', 'Q.......', '..Q.....', '.....Q..', '.Q......', '......Q.', '....Q...']],
        },
        {
            "n": 9,
            "expected":  [['Q.......', '....Q...', '.......Q', '.....Q..', '..Q.....', '......Q.', '.Q......', '...Q....'], ['Q.......', '.....Q..', '.......Q', '..Q.....', '......Q.', '...Q....', '.Q......', '....Q...'], ['Q.......', '......Q.', '...Q....', '.....Q..', '.......Q', '.Q......', '....Q...', '..Q.....'], ['Q.......', '......Q.', '....Q...', '.......Q', '.Q......', '...Q....', '.....Q..', '..Q.....'], ['.Q......', '...Q....', '.....Q..', '.......Q', '..Q.....', 'Q.......', '......Q.', '....Q...'], ['.Q......', '....Q...', '......Q.', 'Q.......', '..Q.....', '.......Q', '.....Q..', '...Q....'], ['.Q......', '....Q...', '......Q.', '...Q....', 'Q.......', '.......Q', '.....Q..', '..Q.....'], ['.Q......', '.....Q..', 'Q.......', '......Q.', '...Q....', '.......Q', '..Q.....', '....Q...'], ['.Q......', '.....Q..', '.......Q', '..Q.....', 'Q.......', '...Q....', '......Q.', '....Q...'], ['.Q......', '......Q.', '..Q.....', '.....Q..', '.......Q', '....Q...', 'Q.......', '...Q....'], ['.Q......', '......Q.', '....Q...', '.......Q', 'Q.......', '...Q....', '.....Q..', '..Q.....'], ['.Q......', '.......Q', '.....Q..', 'Q.......', '..Q.....', '....Q...', '......Q.', '...Q....'], ['..Q.....', 'Q.......', '......Q.', '....Q...', '.......Q', '.Q......', '...Q....', '.....Q..'], ['..Q.....', '....Q...', '.Q......', '.......Q', 'Q.......', '......Q.', '...Q....', '.....Q..'], ['..Q.....', '....Q...', '.Q......', '.......Q', '.....Q..', '...Q....', '......Q.', 'Q.......'], ['..Q.....', '....Q...', '......Q.', 'Q.......', '...Q....', '.Q......', '.......Q', '.....Q..'], ['..Q.....', '....Q...', '.......Q', '...Q....', 'Q.......', '......Q.', '.Q......', '.....Q..'], ['..Q.....', '.....Q..', '.Q......', '....Q...', '.......Q', 'Q.......', '......Q.', '...Q....'], ['..Q.....', '.....Q..', '.Q......', '......Q.', 'Q.......', '...Q....', '.......Q', '....Q...'], ['..Q.....', '.....Q..', '.Q......', '......Q.', '....Q...', 'Q.......', '.......Q', '...Q....'], ['..Q.....', '.....Q..', '...Q....', 'Q.......', '.......Q', '....Q...', '......Q.', '.Q......'], ['..Q.....', '.....Q..', '...Q....', '.Q......', '.......Q', '....Q...', '......Q.', 'Q.......'], ['..Q.....', '.....Q..', '.......Q', 'Q.......', '...Q....', '......Q.', '....Q...', '.Q......'], ['..Q.....', '.....Q..', '.......Q', 'Q.......', '....Q...', '......Q.', '.Q......', '...Q....'], ['..Q.....', '.....Q..', '.......Q', '.Q......', '...Q....', 'Q.......', '......Q.', '....Q...'], ['..Q.....', '......Q.', '.Q......', '.......Q', '....Q...', 'Q.......', '...Q....', '.....Q..'], ['..Q.....', '......Q.', '.Q......', '.......Q', '.....Q..', '...Q....', 'Q.......', '....Q...'], ['..Q.....', '.......Q', '...Q....', '......Q.', 'Q.......', '.....Q..', '.Q......', '....Q...'], ['...Q....', 'Q.......', '....Q...', '.......Q', '.Q......', '......Q.', '..Q.....', '.....Q..'], ['...Q....', 'Q.......', '....Q...', '.......Q', '.....Q..', '..Q.....', '......Q.', '.Q......'], ['...Q....', '.Q......', '....Q...', '.......Q', '.....Q..', 'Q.......', '..Q.....', '......Q.'], ['...Q....', '.Q......', '......Q.', '..Q.....', '.....Q..', '.......Q', 'Q.......', '....Q...'], ['...Q....', '.Q......', '......Q.', '..Q.....', '.....Q..', '.......Q', '....Q...', 'Q.......'], ['...Q....', '.Q......', '......Q.', '....Q...', 'Q.......', '.......Q', '.....Q..', '..Q.....'], ['...Q....', '.Q......', '.......Q', '....Q...', '......Q.', 'Q.......', '..Q.....', '.....Q..'], ['...Q....', '.Q......', '.......Q', '.....Q..', 'Q.......', '..Q.....', '....Q...', '......Q.'], ['...Q....', '.....Q..', 'Q.......', '....Q...', '.Q......', '.......Q', '..Q.....', '......Q.'], ['...Q....', '.....Q..', '.......Q', '.Q......', '......Q.', 'Q.......', '..Q.....', '....Q...'], ['...Q....', '.....Q..', '.......Q', '..Q.....', 'Q.......', '......Q.', '....Q...', '.Q......'], ['...Q....', '......Q.', 'Q.......', '.......Q', '....Q...', '.Q......', '.....Q..', '..Q.....'], ['...Q....', '......Q.', '..Q.....', '.......Q', '.Q......', '....Q...', 'Q.......', '.....Q..'], ['...Q....', '......Q.', '....Q...', '.Q......', '.....Q..', 'Q.......', '..Q.....', '.......Q'], ['...Q....', '......Q.', '....Q...', '..Q.....', 'Q.......', '.....Q..', '.......Q', '.Q......'], ['...Q....', '.......Q', 'Q.......', '..Q.....', '.....Q..', '.Q......', '......Q.', '....Q...'], ['...Q....', '.......Q', 'Q.......', '....Q...', '......Q.', '.Q......', '.....Q..', '..Q.....'], ['...Q....', '.......Q', '....Q...', '..Q.....', 'Q.......', '......Q.', '.Q......', '.....Q..'], ['....Q...', 'Q.......', '...Q....', '.....Q..', '.......Q', '.Q......', '......Q.', '..Q.....'], ['....Q...', 'Q.......', '.......Q', '...Q....', '.Q......', '......Q.', '..Q.....', '.....Q..'], ['....Q...', 'Q.......', '.......Q', '.....Q..', '..Q.....', '......Q.', '.Q......', '...Q....'], ['....Q...', '.Q......', '...Q....', '.....Q..', '.......Q', '..Q.....', 'Q.......', '......Q.'], ['....Q...', '.Q......', '...Q....', '......Q.', '..Q.....', '.......Q', '.....Q..', 'Q.......'], ['....Q...', '.Q......', '.....Q..', 'Q.......', '......Q.', '...Q....', '.......Q', '..Q.....'], ['....Q...', '.Q......', '.......Q', 'Q.......', '...Q....', '......Q.', '..Q.....', '.....Q..'], ['....Q...', '..Q.....', 'Q.......', '.....Q..', '.......Q', '.Q......', '...Q....', '......Q.'], ['....Q...', '..Q.....', 'Q.......', '......Q.', '.Q......', '.......Q', '.....Q..', '...Q....'], ['....Q...', '..Q.....', '.......Q', '...Q....', '......Q.', 'Q.......', '.....Q..', '.Q......'], ['....Q...', '......Q.', 'Q.......', '..Q.....', '.......Q', '.....Q..', '...Q....', '.Q......'], ['....Q...', '......Q.', 'Q.......', '...Q....', '.Q......', '.......Q', '.....Q..', '..Q.....'], ['....Q...', '......Q.', '.Q......', '...Q....', '.......Q', 'Q.......', '..Q.....', '.....Q..'], ['....Q...', '......Q.', '.Q......', '.....Q..', '..Q.....', 'Q.......', '...Q....', '.......Q'], ['....Q...', '......Q.', '.Q......', '.....Q..', '..Q.....', 'Q.......', '.......Q', '...Q....'], ['....Q...', '......Q.', '...Q....', 'Q.......', '..Q.....', '.......Q', '.....Q..', '.Q......'], ['....Q...', '.......Q', '...Q....', 'Q.......', '..Q.....', '.....Q..', '.Q......', '......Q.'], ['....Q...', '.......Q', '...Q....', 'Q.......', '......Q.', '.Q......', '.....Q..', '..Q.....'], ['.....Q..', 'Q.......', '....Q...', '.Q......', '.......Q', '..Q.....', '......Q.', '...Q....'], ['.....Q..', '.Q......', '......Q.', 'Q.......', '..Q.....', '....Q...', '.......Q', '...Q....'], ['.....Q..', '.Q......', '......Q.', 'Q.......', '...Q....', '.......Q', '....Q...', '..Q.....'], ['.....Q..', '..Q.....', 'Q.......', '......Q.', '....Q...', '.......Q', '.Q......', '...Q....'], ['.....Q..', '..Q.....', 'Q.......', '.......Q', '...Q....', '.Q......', '......Q.', '....Q...'], ['.....Q..', '..Q.....', 'Q.......', '.......Q', '....Q...', '.Q......', '...Q....', '......Q.'], ['.....Q..', '..Q.....', '....Q...', '......Q.', 'Q.......', '...Q....', '.Q......', '.......Q'], ['.....Q..', '..Q.....', '....Q...', '.......Q', 'Q.......', '...Q....', '.Q......', '......Q.'], ['.....Q..', '..Q.....', '......Q.', '.Q......', '...Q....', '.......Q', 'Q.......', '....Q...'], ['.....Q..', '..Q.....', '......Q.', '.Q......', '.......Q', '....Q...', 'Q.......', '...Q....'], ['.....Q..', '..Q.....', '......Q.', '...Q....', 'Q.......', '.......Q', '.Q......', '....Q...'], ['.....Q..', '...Q....', 'Q.......', '....Q...', '.......Q', '.Q......', '......Q.', '..Q.....'], ['.....Q..', '...Q....', '.Q......', '.......Q', '....Q...', '......Q.', 'Q.......', '..Q.....'], ['.....Q..', '...Q....', '......Q.', 'Q.......', '..Q.....', '....Q...', '.Q......', '.......Q'], ['.....Q..', '...Q....', '......Q.', 'Q.......', '.......Q', '.Q......', '....Q...', '..Q.....'], ['.....Q..', '.......Q', '.Q......', '...Q....', 'Q.......', '......Q.', '....Q...', '..Q.....'], ['......Q.', 'Q.......', '..Q.....', '.......Q', '.....Q..', '...Q....', '.Q......', '....Q...'], ['......Q.', '.Q......', '...Q....', 'Q.......', '.......Q', '....Q...', '..Q.....', '.....Q..'], ['......Q.', '.Q......', '.....Q..', '..Q.....', 'Q.......', '...Q....', '.......Q', '....Q...'], ['......Q.', '..Q.....', 'Q.......', '.....Q..', '.......Q', '....Q...', '.Q......', '...Q....'], ['......Q.', '..Q.....', '.......Q', '.Q......', '....Q...', 'Q.......', '.....Q..', '...Q....'], ['......Q.', '...Q....', '.Q......', '....Q...', '.......Q', 'Q.......', '..Q.....', '.....Q..'], ['......Q.', '...Q....', '.Q......', '.......Q', '.....Q..', 'Q.......', '..Q.....', '....Q...'], ['......Q.', '....Q...', '..Q.....', 'Q.......', '.....Q..', '.......Q', '.Q......', '...Q....'], ['.......Q', '.Q......', '...Q....', 'Q.......', '......Q.', '....Q...', '..Q.....', '.....Q..'], ['.......Q', '.Q......', '....Q...', '..Q.....', 'Q.......', '......Q.', '...Q....', '.....Q..'], ['.......Q', '..Q.....', 'Q.......', '.....Q..', '.Q......', '....Q...', '......Q.', '...Q....'], ['.......Q', '...Q....', 'Q.......', '..Q.....', '.....Q..', '.Q......', '......Q.', '....Q...']],
        }
    ]



    solution = Solution()


    def cmpResult(result, expected):
        # result and expected have same size and same item values (ignore order)
        if len(result) != len(expected):
            print(f"Result size: {len(result)}, Expected size: {len(expected)}")
           

        normalize = lambda boards: sorted(tuple(board) for board in boards)
        cmp = normalize(result) == normalize(expected)
        if not cmp:
            result_norm = normalize(result)
            expected_norm = normalize(expected)
            diff_result = [board for board in result_norm if board not in expected_norm]
            diff_expected = [board for board in expected_norm if board not in result_norm]
            print("Boards in result but not in expected:", diff_result)
            print("Boards in expected but not in result:", diff_expected)
   
        return cmp

    import time
    t1 = int(time.time() * 1000)
    
    for index, test in enumerate(tests, 1):
        if selected_tests is not None and test['n'] not in selected_tests:
            continue

        n = test["n"]
        expected = test["expected"]

        try:
            print(f"\nTEST {index} n={n}")
            result = solution.solveNQueens(n)
            ok = cmpResult(result, expected)
            if not ok:
                print(f"test {index} FAIL: n={n}")
                print(f"  got:      {result}")
                print(f"  expected: {expected}")
            else:
                print(f"test {index} OK: n={n} ({len(result)} subsets)")
        except Exception as e:
            print(f"test {index} ERROR: {e}")
            raise
    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")