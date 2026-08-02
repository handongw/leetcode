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

        result = [ [1] * n for _ in range(m)]

        MODULE = 12345

        # def setNextCell(matrix, r, c, v):
        #     if c < n-1:
        #         matrix[r][c+1] = v
        #     else:
        #         matrix[r+1][0] = v


        prod = 1
        for r in range(m):
            for c in range(n):
                # prod *= grid[r][c]
                prod = (prod * grid[r][c]) % MODULE
                if r != m-1 or c != n-1:
                    # setNextCell(result, r, c, prod)  # store endOf[x-1] in result[x]
                    if c < n-1:
                        result[r][c+1] = prod
                    else:
                        result[r+1][0] = prod    

        # print(f"    endOf in result={result}")            

        prod = 1
        for r in reversed(range(m)):
            for c in reversed(range(n)):
                result[r][c] *= prod
                result[r][c] %= MODULE

                prod *= grid[r][c]
                prod = prod % MODULE

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

