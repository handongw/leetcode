import heapq
from typing import List


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)

        visited = [[False for _ in range(n)]   for _ in range(n)]
        def print_visisted():
            for r in range(n):
                l = ["*" if flag else "." for flag in visited[r]]
                print(" ".join(l) )

        q = []

        # expand accessible cells from [0][0] as water rising up
        heapq.heappush(q, (grid[0][0], 0,0))

        watermark = 0 # or grid[0][0]
        heapq.heappush(q, (grid[0][0], 0, 0))
        visited[0][0] = True # Mark visited immediately!

        while q:
            level, row, col = heapq.heappop(q)
            
            # Update the highest water level we've had to endure
            watermark = max(watermark, level)
            
            # Did we reach the end?
            if row == n - 1 and col == n - 1:
                return watermark
                
            for dr, dc in [(1,0), (-1,0), (0,1), (0,-1)]:
                r, c = row + dr, col + dc
                
                if 0 <= r < n and 0 <= c < n and not visited[r][c]:
                    visited[r][c] = True # Mark visited before pushing!
                    heapq.heappush(q, (grid[r][c], r, c))

if __name__ == "__main__":
    sol = Solution()

    grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]
    ans = sol.swimInWater(grid)
    print(f"ans={ans} test={'PASS' if ans==16 else 'FAIL'}")
