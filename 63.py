from functools import cache
from typing import List

# You are given an m x n integer array grid. There is a robot initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.

# An obstacle and space are marked as 1 or 0 respectively in grid. A path that the robot takes cannot include any square that is an obstacle.

# Return the number of possible unique paths that the robot can take to reach the bottom-right corner.

# The testcases are generated so that the answer will be less than or equal to 2 * 109.

# Constraints:

# m == obstacleGrid.length
# n == obstacleGrid[i].length
# 1 <= m, n <= 100
# obstacleGrid[i][j] is 0 or 1. 

class Solution:
    def uniquePathsWithObstacles(self, obstacleGrid: List[List[int]]) -> int:
        m = len(obstacleGrid)
        n = len(obstacleGrid[0])

        if obstacleGrid[0][0] != 0:
            return 0

        @cache
        def traverse(r:int, c:int) -> int:
            
            # traverse path never forms loop so no need to track cell as visisted
            if r == m-1 and c == n-1:
                if obstacleGrid[r][c] == 0:
                    return 1
                else:
                    return 0

            paths = 0
            moves = [(0, 1), (1, 0)]
            for delta in moves:
                r1 = r + delta[0]
                c1 = c + delta[1]

                if r1 < m and c1 < n and obstacleGrid[r1][c1] == 0:
                    paths += traverse(r1, c1)
            return paths    

        return traverse(0, 0)
        
