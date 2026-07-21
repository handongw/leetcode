import copy
from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:

        island_cnt = 0

        for row in range(len(grid)):
            for col in range(len(grid[row])):
                if grid[row][col] == '1':
                    stack = []

                    stack.append((row, col))
                    grid[row][col] = '*'  # visited

                    while len(stack) > 0:
                        i, j = stack.pop()

                        up_row = i - 1
                        down_row = i + 1
                        left_col = j - 1
                        right_col = j + 1

                        if up_row>=0 and grid[up_row][j] == '1':
                            stack.append((up_row, j))
                            grid[up_row][j] = '*'
                        if down_row < len(grid) and grid[down_row][j] == '1':
                            stack.append((down_row, j))
                            grid[down_row][j] = '*'
                        if left_col>=0 and grid[i][left_col] == '1':
                            stack.append((i, left_col))
                            grid[i][left_col] = '*'
                        if right_col < len(grid[0]) and grid[i][right_col] == '1':
                            stack.append((i, right_col))
                            grid[i][right_col] = '*'
                    island_cnt += 1        

        return island_cnt


if __name__ == "__main__":
    import traceback
    import time

    solver = Solution()

    test_cases = [
        {
            "grid": [
                ["1", "1", "1", "1", "0"],
                ["1", "1", "0", "1", "0"],
                ["1", "1", "0", "0", "0"],
                ["0", "0", "0", "0", "0"],
            ],
            "expected": 1,
        },
        {
            "grid": [
                ["1", "1", "0", "0", "0"],
                ["1", "1", "0", "0", "0"],
                ["0", "0", "1", "0", "0"],
                ["0", "0", "0", "1", "1"],
            ],
            "expected": 3,
        },
        {
            "grid": [["1"]],
            "expected": 1,
        },
        {
            "grid": [["0"]],
            "expected": 0,
        },
        {
            "grid": [
                ["0", "0"],
                ["0", "0"],
            ],
            "expected": 0,
        },
        {
            "grid": [
                ["1", "1"],
                ["1", "1"],
            ],
            "expected": 1,
        },
        {
            "grid": [
                ["1", "0", "1"],
                ["0", "1", "0"],
                ["1", "0", "1"],
            ],
            "expected": 5,
        },
    ]

    # cases = [2]
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
                print(f"\n\nCase {idx}: {case['grid']}\n")
                actual = solver.numIslands(grid)
                print(f"Case {idx}:")
                print(f"  grid={case['grid']}")
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