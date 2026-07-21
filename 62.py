"""
There is a robot on an m x n grid. The robot is initially located at the
top-left corner (i.e., grid[0][0]). The robot tries to move to the
bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move
either down or right at any point in time.

Given the two integers m and n, return the number of possible unique paths
that the robot can take to reach the bottom-right corner.

The test suite below is for uniquePaths.

1 <= m, n <= 100

Example 1:
Input: m = 3, n = 7
Output: 28

Example 2:
Input: m = 3, n = 2
Output: 3
"""


class Solution:
    def uniquePaths(self, m: int, n: int) -> int:

        result_matrix = [  [-1] * n for row in range(m)]

        result_matrix[m-1][n-1] = 1
        
        for col in reversed(range(n)):
            for row in reversed(range(m)):
                if result_matrix[row][col] != -1:
                    continue

                # check down block
                if row < m - 1:
                    row1 = row + 1
                    if result_matrix[row1][col] < 0:
                        raise Exception(f"result_matrix[{row1}][{col}]={result_matrix[row1][col]}")
                    r1 = result_matrix[row1][col]
                else:
                    r1 = 0
                # check right block

                if col < n-1:
                    col1 = col + 1
                    if result_matrix[row][col1] < 0:
                        raise Exception(f"result_matrix[{row}][{col1}]={result_matrix[row][col1]}")
                    r2 = result_matrix[row][col1]
                else:
                    r2 = 0

                result_matrix[row][col] = r1 + r2
                
        return result_matrix[0][0]


def _brute_unique_paths(m: int, n: int) -> int:
    """Reference: paths = C(m + n - 2, m - 1) (only down/right moves)."""
    import math

    return math.comb(m + n - 2, m - 1)


if __name__ == '__main__':
    import sys
    import time

    DEBUG = False
    selected_tests = None  # None: run all; else set of 1-based indices from argv

    for a in sys.argv[1:]:
        if a == "-d":
            DEBUG = True
        elif a.replace(",", "").isdigit() and "," in a:
            if selected_tests is None:
                selected_tests = set()
            for part in a.split(","):
                part = part.strip()
                if part.isdigit():
                    selected_tests.add(int(part))
        elif a.isdigit():
            if selected_tests is None:
                selected_tests = set()
            selected_tests.add(int(a))
        else:
            print(
                f"Unknown argument: {a!r} (use -d and/or 1-based test indices, e.g. 1 2 3)",
                file=sys.stderr,
            )
            sys.exit(2)

    if selected_tests is not None and len(selected_tests) == 0:
        print("Test selection is empty.", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"selected_tests={selected_tests}")

    tests = [
        {"n": 1, "m": 3, "cols": 7, "expected": 28},
        {"n": 2, "m": 3, "cols": 2, "expected": 3},
        {"n": 3, "m": 1, "cols": 1, "expected": 1},
        {"n": 4, "m": 1, "cols": 10, "expected": 1},
        {"n": 5, "m": 10, "cols": 1, "expected": 1},
        {"n": 6, "m": 2, "cols": 2, "expected": 2},
        {"n": 7, "m": 3, "cols": 3, "expected": 6},
        {"n": 8, "m": 7, "cols": 3, "expected": 28},
        {"n": 9, "m": 2, "cols": 5, "expected": 5},
        {"n": 10, "m": 4, "cols": 4, "expected": 20},
        {"n": 11, "m": 5, "cols": 5, "expected": 70},
        {"n": 12, "m": 2, "cols": 100, "expected": 100},
        {"n": 13, "m": 100, "cols": 2, "expected": 100},
        {
            "n": 14,
            "m": 23,
            "cols": 12,
            "expected": _brute_unique_paths(23, 12),
        },
        {
            "n": 15,
            "m": 100,
            "cols": 100,
            "expected": _brute_unique_paths(100, 100),
        },
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        m = test["m"]
        n = test["cols"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} m={m} n={n}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.uniquePaths(m, n)
            if result != expected:
                print(f"test {test['n']} FAIL")
                print(f"  got:      {result}")
                print(f"  expected: {expected}")
            else:
                print(f"test {test['n']} OK: (result={result})")
        except Exception as e:
            print(f"test {test['n']} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")
