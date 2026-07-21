# You are given an m x n binary grid grid where 1 represents land and 0 represents water. An island is a maximal 4-directionally (horizontal or vertical) connected group of 1's.

# The grid is said to be connected if we have exactly one island, otherwise is said disconnected.

# In one day, we are allowed to change any single land cell (1) into a water cell (0).

# Return the minimum number of days to disconnect the grid.

# m == grid.length
# n == grid[i].length
# 1 <= m, n <= 30
# grid[i][j] is either 0 or 1.

from typing import List


class Solution:
    def minDays(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])

        vertex_list = []
        vertex_map = {}

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    vertex_map[(i, j)] = len(vertex_list)
                    vertex_list.append((i, j))
                    
        adj_list = [ [] for _ in range(len(vertex_list))]
        movements = [(-1,0), (1, 0), (0, -1), (0, 1)]

        for idx, v in enumerate(vertex_list):
            for delta in movements:
                row = v[0] + delta[0]
                col = v[1] + delta[1]
                if row >=0 and row < m and col>=0 and col<n and grid[row][col]==1:
                    adj_list[idx].append(vertex_map[(row, col)])

        print(", ".join([ f"#{i}:{v}" for i, v in enumerate(vertex_list)]) )           

        if len(vertex_list) == 0:
            return 0
        if len(vertex_list) == 1:
            return 1
        if len(vertex_list) == 2:
            if adj_list[0]:
                return 2
            return 0

        # we will use vertex id instead of (row, col) hereafter
        # low link support data structures
        disc = [-1] * len(vertex_list)
        low = [n*m] * len(vertex_list)
        timer = 1

        def dfs(u, parent, memo):
            nonlocal timer

            disc[u] = low[u] = timer
            timer += 1
            child_count = 0

            for v in adj_list[u]:
                if v == u or v == parent:
                    continue

                if disc[v] >= 0:
                    low[u] = min(low[u], disc[v])
                else: # find a tree edge
                    child_count += 1
                    dfs(v, u, memo)
                    low[u] = min(low[u], low[v])
                    # check articulation vertex (non-root)
                    if parent != -1 and disc[u] <= low[v]:
                        memo["has_articulation_vertex"] = True

            # check articulation vertex (root with 2+ tree children)
            if parent == -1 and child_count >= 2:
                memo["has_articulation_vertex"] = True

        cc_memos = []
        for u in range(len(vertex_list)):
            if disc[u] < 0:
                memo = {"has_articulation_vertex": False}
                dfs(u, -1, memo)
                cc_memos.append(memo)
        # print(f"disc={disc}")
        # print(f"low={low}")
        # print(f"cc_memos={cc_memos}")
        if len(cc_memos) > 1:
            return 0 # grid is already disconnected
        else:
            if cc_memos[0]["has_articulation_vertex"]:
                return 1  # grid has one CC that has articulate vertex
            else:
                return 2  # we can disconnect the grid in by deleting 2 cells of a corner island


if __name__ == "__main__":
    import copy
    import traceback
    import time

    solver = Solution()

    test_cases = [
        # LeetCode examples
        {
            "grid": [
                [0, 1, 1, 0],
                [0, 1, 1, 0],
                [0, 0, 0, 0],
            ],
            "expected": 2,
        },
        {
            "grid": [
                [1, 1, 1],
                [1, 1, 0],
                [1, 1, 1],
            ],
            "expected": 1,
        },
        {
            "grid": [
                [1, 1, 1],
                [1, 1, 0],
                [1, 1, 1],
            ],
            "expected": 1,
        },
        {
            "grid": [
                [1, 1],
            ],
            "expected": 2,
        },
        # already disconnected -> 0
        {
            "grid": [
                [1, 0],
                [0, 1],
            ],
            "expected": 0,
        },
        {
            "grid": [
                [1, 1, 0, 0, 0],
                [1, 1, 0, 0, 0],
                [0, 0, 1, 0, 0],
                [0, 0, 0, 1, 1],
            ],
            "expected": 0,
        },
        {
            "grid": [
                [0, 0, 0],
                [0, 0, 0],
            ],
            "expected": 0,
        },
        # articulation point -> 1
        {
            "grid": [
                [1, 1, 1],
                [0, 1, 0],
                [0, 1, 0],
            ],
            "expected": 1,
        },
        {
            "grid": [
                [1, 0, 1],
                [0, 1, 0],
                [1, 0, 1],
            ],
            "expected": 0,
        },
        {
            "grid": [[1]],
            "expected": 1,
        },
        {
            "grid": [
                [1, 1],
                [1, 0],
            ],
            "expected": 1,
        },
        # no articulation point -> 2
        {
            "grid": [
                [1, 1],
                [1, 1],
            ],
            "expected": 2,
        },
        {
            "grid": [
                [1, 1, 1],
                [1, 1, 1],
            ],
            "expected": 2,
        },
        {
            "grid": [
                [1, 1, 0],
                [1, 1, 0],
                [0, 0, 0],
            ],
            "expected": 2,
        },
    ]

    # cases = [1]
    cases = None
    t1 = int(time.time() * 1000)
    succCount = 0
    totalCount = 0
    for idx, case in enumerate(test_cases, start=1):
        if cases is None or idx in cases:
            totalCount += 1
            grid = copy.deepcopy(case["grid"])
            expected = case["expected"]
            try:
                print(f"\n\nCase {idx}: grid={grid!r}\n")
                actual = solver.minDays(grid)
                print(f"Case {idx}:")
                print(f"  grid    ={case['grid']}")
                print(f"  expected={expected}")
                print(f"  actual  ={actual}")
                print(f"  Case {idx} pass    ={actual == expected}")
                print("\n")
                if actual == expected:
                    succCount += 1
            except Exception as exc:
                print(f"Case {idx} raised an exception: {exc}")
                traceback.print_exc()

    t2 = int(time.time() * 1000)
    print(f"   total time={t2-t1:,} ms  succ= {succCount}/{totalCount}")

