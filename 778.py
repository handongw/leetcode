import heapq
from typing import List


class Solution:
    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)

        maxLevel = n*n - 1

        visited = [[False for _ in range(n)]   for _ in range(n)]
        def print_visisted():
            for r in range(n):
                l = ["*" if flag else "." for flag in visited[r]]
                print(" ".join(l) )

        q = []

        # expand accessible cells from [0][0] as water rising up
        heapq.heappush(q, (grid[0][0], 0,0))

        t = 0
        while t <= maxLevel:
            # print(f"t={t}")
            while q:
                level, row, col = q[0]
                # print(f"    check leve={level}, row={row}, col={col}")
                if level <= t:
                    visited[row][col] = True
                    if row==n-1 and col==n-1:
                        # print_visisted()
                        return t

                    heapq.heappop(q)
                    # print(f"        pop leve={level}, row={row}, col={col}")

                    for move in [(1,0), (-1,0), (0,1), (0,-1)]:                        
                        r = row + move[0]
                        c = col + move[1]
                        
                        if r>=0 and r<n and c>=0 and c<n and not visited[r][c]:
                            visited[r][c] = True
                            heapq.heappush(q, (grid[r][c], r, c))
                            # print(f"        push grid[{r}][{c}]={grid[r][c]}")
                else:
                    break 
            t = max(t+1, q[0][0])                 
       
        return t

if __name__ == "__main__":
    sol = Solution()

    grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]
    ans = sol.swimInWater(grid)
    print(f"ans={ans} test={'PASS' if ans==16 else 'FAIL'}")
