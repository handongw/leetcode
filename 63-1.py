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

        if obstacleGrid[0][0] != 0 or obstacleGrid[m-1][n-1] != 0:
            return 0

        dp = [[ 0 for _ in range(0,n)] for _ in range(0,m)]
        dp[m-1][n-1] = 1  # destination

        for r in reversed(range(0, m-1)):
            if obstacleGrid[r][n-1] == 0 and dp[r+1][n-1] == 1:
                dp[r][n-1] = 1  # right edge
        
        for c in reversed(range(0, n-1)):
            if obstacleGrid[m-1][c] == 0 and dp[m-1][c+1] == 1:
                dp[m-1][c] = 1  # bottom edge

        for r in reversed(range(0, m-1)):
            for c in reversed(range(0, n-1)):
                if obstacleGrid[r][c] == 0:
                    dp[r][c] = dp[r+1][c] + dp[r][c+1]

        # print(dp)
        return dp[0][0]
        
