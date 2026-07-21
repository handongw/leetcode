
from typing import List

DEBUG = False


class Solution:
    def solveNQueens(self, n: int) -> List[List[str]]:
        succBoardList = []
        succSet = set()
        conflictSet = set()

        placeQueenCnt = 0
        skipCnt = 0

        def printBoard(matrix):
            if DEBUG:
                for row in matrix:
                    print(' '.join(row))
                print()
   

        def placeQueen(matrix, pos, remainingQueens, carryOver):
            nonlocal placeQueenCnt, skipCnt
            placeQueenCnt += 1

            path = carryOver["path"]

            if DEBUG:
                print(f"ENTER placeQueen pos={pos} remainingQueens={remainingQueens} path={path}")
                printBoard(matrix)

            row, col = pos
            matrix[row][col] = 'Q'
            

            if remainingQueens <= 0:
                # it is done                
                # Convert all 'X' in matrix to '.'
                for i in range(n):
                    for j in range(n):
                        if matrix[i][j] == 'X':
                            matrix[i][j] = '.'

                # INSERT_YOUR_CODE
                for existing_board in succBoardList:
                    if existing_board == matrix:
                        if DEBUG:
                            print("DUP solution found, skipping.")
                            printBoard(matrix)
                        return None
         
                succBoardList.append(matrix)
                if DEBUG:
                    print(f"FOUND ONE {carryOver["path"]}")

                return matrix

            # if frozenset(path) in succSet:
            #     skipCnt += 1
            #     if DEBUG:
            #         # encounter the prefix before
            #         print(f" encounter prefix {path} before succ set size = {len(succSet)}")
            #     return

            # mark diagonal of pos using 'X'
            def mark(m, i, j, c):
                m[i][j] = c
                return
                
                # if i>=0 and i<n and j>=0 and j<n:
                #     if m[i][j] == 'Q':
                #         if DEBUG:
                #             printBoard(m)
                #         raise Exception(f"mark {c} error: ({i},{j})={m[i][j]}  pos={pos} path={carryOver["path"]}")
               
                #     m[i][j] = c
                # else:
                #     raise Exception(f"mark {c} error: ({i},{j})={m[i][j]}  pos={pos} path={carryOver["path"]}")


            #mark same row of row using 'X'
            for j in range(n):
                if matrix[row][j] != 'Q':
                    matrix[row][j] = 'X'
                    

            # mark same colum of col using 'X'
            for i in range(n):
                if matrix[i][col] != 'Q':
                    matrix[i][col] = 'X'

            # mark diagonal position using 'X'
            def markDiagonalX():
                i, j = pos
                # move left , upper
                while i>0 and j>0:
                    i -= 1; j -= 1
                    mark(matrix, i, j, 'X')

                # move left down
                i, j = pos
                while i < n-1 and j>0:
                    i += 1; j -= 1
                    mark(matrix, i, j, 'X')

                # move right upper
                i, j = pos
                while i > 0 and j < n -1:
                    i -= 1; j += 1
                    mark(matrix, i, j, 'X')
    
                # move right down
                i, j = pos
                while i < n -1 and j < n -1:
                    i += 1; j += 1
                    mark(matrix, i, j, 'X')
    
            markDiagonalX()   
            if DEBUG:         
                printBoard(matrix)

             # find next available slot
            def findCandidatePos(m):
                slots = []
                for i in range(n):
                    for j in range(n):
                        if m[i][j] == '.':                        
                            slots.append((i, j))
                return slots

            
            slots = findCandidatePos(matrix)
            if len(slots) <= 0: 
                # dead end
                # failBoardList.append(matrix)
                key = frozenset(path)
                conflictSet.add(key)           
                if DEBUG:
                    print(f"DEAD END")
            else:
                if DEBUG:
                    print(f"  slots={slots}")
                
                for slot in slots:
                    path2 = path[:]
                    path2.append(slot)
                    key2 = frozenset(path2)
                    if key2 in succSet or key2 in conflictSet:                    
                        skipCnt += 1
                        if DEBUG:
                            # encounter the prefix before
                            print(f" encounter prefix {path} before set size = {len(succSet)}")                           
                    else:
                        matrix2 = [row[:] for row in matrix]
                        carryOver2 = {"path": path2 }            
                        placeQueen(matrix2, slot, remainingQueens-1, carryOver2)  

                # we have tried all solution with prefix = path
                key = frozenset(path)
                succSet.add(key)                    

            
        for i in range(n):
            for j in range(n):
                if i >= j:
                    # Check if there is already a board in doneBoardList with a 'Q' at (i, j)
                    # already_placed = False
                    # for b in succBoardList:
                    #     if b[i][j] == 'Q':
                    #         already_placed = True
                    #         break
                    # if already_placed:
                    #     continue
                    # create an empty board
                    board = [["." for j in range(n)] for i in range(n)]
                    placeQueen(board, (i, j), n-1, {'path':[(i, j)]})
        # if DEBUG:
        print(f"   place cnt={placeQueenCnt:,} skip cnt={skipCnt:,}")       

        result = []
        for b in succBoardList:
            x = []
            for r in b:
                s = ''.join(r)
                s = s.replace('X', '.')
                x.append(s)
            result.append(x)    

        return result        


if __name__ == '__main__':
    tests = [
        # {
        #     "n": 4,
        #     "expected": [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]],
        # },
        # {
        #     "n": 1, 
        #     "expected": [["Q"]]
        # },
        {
            "n": 8,
            "expected": [["Q....","..Q..","....Q",".Q...","...Q."],["Q....","...Q.",".Q...","....Q","..Q.."],[".Q...","...Q.","Q....","..Q..","....Q"],[".Q...","....Q","..Q..","Q....","...Q."],["..Q..","Q....","...Q.",".Q...","....Q"],["..Q..","....Q",".Q...","...Q.","Q...."],["...Q.","Q....","..Q..","....Q",".Q..."],["...Q.",".Q...","....Q","..Q..","Q...."],["....Q",".Q...","...Q.","Q....","..Q.."],["....Q","..Q..","Q....","...Q.",".Q..."]],
        },
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

    for index, test in enumerate(tests, 1):
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
