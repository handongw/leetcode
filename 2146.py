from collections import deque
from heapq import heapify, heappop
from typing import List

class Solution:
    def highestRankedKItems(self, grid: List[List[int]], pricing: List[int], start: List[int], k: int) -> List[List[int]]:
        '''
        high level solution: (1) BFS traverse the grid from start cell. (2) append legitimate candidate (dist, price, row, col) items while traversing
                             (3) heapify candidate array (4) heap pop up to k items from candidate array (5) format and return result.

        Time complexity: O(m*n + k log C) where Let C be the size of candidate array. worst case O(m*n log (m*n))
        Space complexity: O(m*n)    

        possible optimization: 1. replace adjacent_cells with for possible adjacent cells directly to avoid creating array objects.
                               2. dist can encoding visited flag so we can get rid of visisted matrix.                 
        '''

        m = len(grid)
        n = len(grid[0])

        q = deque()
        visited = [ [False] * n for _ in range(m) ]
        dist = [[0] * n for _ in range(m)]

        visited[start[0]][start[1]] = True
        q.append(start)
        

        moves = [(-1,0),(1,0),(0,-1),(0,1)]
        def adjacent_cells(u):
            cells = []
            for mv in moves:
                adj_cell = (u[0]+mv[0], u[1]+mv[1])
                if adj_cell[0] < 0 or adj_cell[0] >= m:
                    continue
                if adj_cell[1] < 0 or adj_cell[1] >= n:
                    continue
                if grid[adj_cell[0]][adj_cell[1]] == 0:
                    continue

                cells.append(adj_cell)
            return cells    
                

        candidates = []

        while q:
            u = q.popleft()
            price = grid[u[0]][u[1]]
            d = dist [u[0]][u[1]]
            if price > 1 and price >= pricing[0] and price <= pricing[1]:
                candidates.append((d, price, u[0], u[1]))


            for v in adjacent_cells(u):
                if not visited[v[0]][v[1]]:
                    visited[v[0]][v[1]] = True
                    dist [v[0]][v[1]] = dist[u[0]][u[1]] + 1
                    q.append(v)

        print(f"debug: candidates={candidates}")                
        heapify(candidates)

        result = []
        for i in range(min(k, len(candidates))):
            x = heappop(candidates)
            result.append([x[2], x[3]])

        return result

if __name__ == "__main__":
    sol = Solution()

    grid = [[1,2,0,1],[1,3,0,1],[0,2,5,1]] 
    pricing = [2,5]
    start = [0,0]
    k = 3
    expected = [[0,1],[1,1],[2,1]]        
    output = sol.highestRankedKItems(grid, pricing, start, k)

    print(f"grid={grid} pricing={pricing} start={start} k={k}")
    print(f"    expected={expected}")
    print(f"    output  ={output}")
    print(f"    {'PASS' if output == expected else 'FAIL'}\n\n")


    grid = [[1,2,0,1],[1,3,3,1],[0,2,5,1]] 
    pricing = [2,3] 
    start = [2,3] 
    k = 2
    expected = [[2,1],[1,2]]        
    output = sol.highestRankedKItems(grid, pricing, start, k)

    print(f"grid={grid} pricing={pricing} start={start} k={k}")
    print(f"    expected={expected}")
    print(f"    output  ={output}")
    print(f"    {'PASS' if output == expected else 'FAIL'}")


    # test start if part of the result
    grid = [[2,2,0,1],[1,3,0,1],[0,2,5,1]] 
    pricing = [2,5]
    start = [0,0]
    k = 3
    expected = [[0,0], [0,1],[1,1]]        
    output = sol.highestRankedKItems(grid, pricing, start, k)
