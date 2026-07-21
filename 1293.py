# 

from collections import deque
import time
from typing import List


class Solution:
    def shortestPath(self, grid: List[List[int]], k: int) -> int:
        m = len(grid)
        n = len(grid[0])

        # state[row][col][removed block count]
        state = [  [ [ float('inf') for _ in range(k+1)] for _ in range(n)]  for _ in range(m)  ]
        state[0][0][0] = 0 

        queue = deque()
        queue.append((0,0,0, 0)) # (row, col, min-length, removed block count)

        # candidates = []            
        while queue:
            r, c, w, cnt = queue.popleft()

            for dr, dc in [(-1,0), (1, 0), (0, -1), (0, 1)]:
                r1 = r + dr
                c1 = c + dc

                if r1>=0 and r1<m and c1>=0 and c1<n:
                    cnt1 = cnt+1 if grid[r1][c1] == 1 else cnt
                    if cnt1 <= k:
                        w1 = w + 1
                        if w1 < state[r1][c1][cnt1]:
                            if w1 == m+n-2 and r1==m-1 and c1==n-1:
                                return w1

                            # check if r1, c1, w1, cnt1 is dominated
                            domininated = False
                            # I need a dedicate data structure to check dominated path
                            # for t in reversed(range(cnt1)):
                            #     if state[r1][c1][t] <= w1:
                            #         domininated = True
                            #         break
                            if domininated:
                                continue

                            state[r1][c1][cnt1] = w1
                            queue.append((r1, c1, w1, cnt1))    

        ans = min(state[m-1][n-1])
        if ans == float('inf'):
            return -1
        else:
            return ans    

if __name__ == "__main__":
    sol = Solution()

    grid = [[0,0,0],[1,1,0],[0,0,0],[0,1,1],[0,0,0]]
    k = 1
    ans = sol.shortestPath(grid, k)
    print(f"ans={ans} test={'PASS' if ans==6 else 'FAIL'}")


    grid = [[0,1,1],[1,1,1],[1,0,0]]
    k = 1
    ans = sol.shortestPath(grid, k)
    print(f"ans={ans} test={'PASS' if ans==-1 else 'FAIL'}")

    grid = [
            [0, 1, 1, 0, 1, 0, 0, 0],
            [0, 1, 1, 0, 1, 1, 1, 0],
            [0, 0, 0, 0, 1, 1, 1, 0]
            ]
    k = 2

    ans = sol.shortestPath(grid, k)
    print(f"ans={ans} test={'PASS' if ans==13 else 'FAIL'}")

    def generate_baffle_maze(m=40, n=40):
        # Initialize grid with 0s
        grid = [[0 for _ in range(n)] for _ in range(m)]
        
        # Create alternating walls every 4 columns
        for c in range(4, n, 4):
            for r in range(m):
                # Leave a small gap in the wall so it's not impossible
                if r % 10 != 0: 
                    grid[r][c] = 1
        return grid

    grid = generate_baffle_maze(40, 40)
    # Example usage:
    k = 15 
    sol = Solution()

    t1 = int(time.time() * 1000)
    ans=sol.shortestPath(grid, k)
    print(f"ans={ans} test={'PASS' if ans==78 else 'FAIL'}")

    t2 = int(time.time() * 1000)
    print(f" exec time = {t2-t1:,} ms")
