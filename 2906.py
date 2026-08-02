from typing import List

# Constraints:

# 1 <= n == grid.length <= 105
# 1 <= m == grid[i].length <= 105
# 2 <= n * m <= 105
# 1 <= grid[i][j] <= 109
class Solution:
    def constructProductMatrix(self, grid: List[List[int]]) -> List[List[int]]:
        m = len(grid)
        n = len(grid[0])

        endOf = [ [1] * n for _ in range(m)]
        startOf = [ [1] * n for _ in range(m)]

        MODULE = 12345

        prod = 1
        for r in range(m):
            for c in range(n):
                prod *= grid[r][c]
                prod = prod % MODULE
                endOf[r][c] = prod

        prod = 1
        for r in reversed(range(m)):
            for c in reversed(range(n)):
                prod *= grid[r][c]
                prod = prod % MODULE
                startOf[r][c] = prod

        def nextCell(matrix, r, c):
            if c < n-1:
                return matrix[r][c+1]
            else:
                return matrix[r+1][0]

        def prevCell(matrix, r, c):
            if c > 0:
                return matrix[r][c-1]
            else:
                return matrix[r-1][n-1]    

        result = [ [1] * n for _ in range(m)]
        for r in range(m):
            for c in range(n):
                if r == 0 and c == 0:
                    result[r][c] = nextCell(startOf, r, c)
                elif r == m-1 and c== n-1:
                    result[r][c] = prevCell(endOf, r, c) 
                else:
                    result[r][c] =  (prevCell(endOf, r, c) * nextCell(startOf, r, c)) % MODULE              

        return result

if __name__ == "__main__":
    sol = Solution()

    grid = [[1,2],[3,4]]
    expected = [[24,12],[8,6]]        
    result = sol.constructProductMatrix(grid)
    print(f"grid={grid}")
    print(f"    expected={expected}")
    print(f"    result={result}")
    print(f"{'PASS' if result==expected else 'FAIL'}\n\n")

    grid = [[12345],[2],[1]]
    expected = [[2],[0],[0]]        
    result = sol.constructProductMatrix(grid)
    print(f"grid={grid}")
    print(f"    expected={expected}")
    print(f"    result={result}")
    print(f"{'PASS' if result==expected else 'FAIL'}\n\n")

