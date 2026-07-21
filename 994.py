from typing import List

# You are given an m x n grid where each cell can have one of three values:

# 0 representing an empty cell,
# 1 representing a fresh orange, or
# 2 representing a rotten orange.
# Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

# Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])

        frontier = []
        orange_cnt = 0
        for i in range(m):
            for j in range(n):
                if grid[i][j] == 2:
                    frontier.append((i, j))
                if grid[i][j] > 0:
                    orange_cnt += 1    

        minutes = -1
        rotten_cnt = 0
        while frontier:
            minutes += 1
            rotten_cnt += len(frontier)

            new_frontier = []
            for i, j in frontier:
                # upper
                if i >= 1 and grid[i-1][j] == 1:
                    grid[i-1][j] = 2
                    new_frontier.append((i-1, j))
                # down
                if i < m-1 and grid[i+1][j] == 1:
                    grid[i+1][j] = 2
                    new_frontier.append((i+1, j))
                #left
                if j >= 1 and grid[i][j-1] == 1:
                    grid[i][j-1] = 2
                    new_frontier.append((i, j-1))
                #right   
                if j < n-1 and grid[i][j+1] == 1:
                    grid[i][j+1] = 2
                    new_frontier.append((i, j+1))

            frontier = new_frontier             

        return -1 if rotten_cnt == orange_cnt else minutes