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

       # Forward: store product before current cell
        prod = 1
        for r in range(m):
            for c in range(n):
                result[r][c] = prod
                prod = (prod * grid[r][c]) % MODULE

        # Backward: multiply by product after current cell
        prod = 1
        for r in range(m - 1, -1, -1):
            for c in range(n - 1, -1, -1):
                result[r][c] = (result[r][c] * prod) % MODULE
                prod = (prod * grid[r][c]) % MODULE

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

