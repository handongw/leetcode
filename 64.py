from typing import List

class Solution:
    def minPathSum(self, grid: List[List[int]]) -> int:
        m = len(grid)
        n = len(grid[0])

        dp = [[None] * n for _ in range(m)]
        dp[0][0] = grid[0][0]

        for r in range(m):
            for c in range(n):
                if r==0 and c==0:
                    continue

                if r == 0:
                    dp[r][c] = dp[r][c-1] + grid[r][c]
                elif c == 0:
                    dp[r][c] = dp[r-1][c] + grid[r][c]
                else:
                    dp[r][c] = min(dp[r][c-1], dp[r-1][c])+grid[r][c]         


        return dp[m-1][n-1]


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
                f"Unknown argument: {a!r} (use -d and/or 1-based test indices, e.g. 1 2 4)",
                file=sys.stderr,
            )
            sys.exit(2)

    if selected_tests is not None and len(selected_tests) == 0:
        print("Test selection is empty.", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"selected_tests={selected_tests}")

    tests = [
        {"n": 1, "grid": [[1, 3, 1], [1, 5, 1], [4, 2, 1]], "expected": 7},
        {"n": 2, "grid": [[1, 2, 3], [4, 5, 6]], "expected": 12},
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        grid = test["grid"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} grid={grid!r}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.minPathSum(grid)
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
