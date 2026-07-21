from typing import List

DEBUG = False

class Solution:
    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        enhanced_cell_list = []
        
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                enhanced_cell_list.append({"v": matrix[i][j], "row": i, "col": j})

        enhanced_cell_list.sort(key=lambda x: x["v"])

        state = [ [ 1  for c in r]  for r in matrix]

        # matrix size
        m = len(matrix)
        n = len(matrix[0])

        for cell in enhanced_cell_list:
            row = cell["row"]
            col = cell["col"]
            val = cell["v"]

            upper_lip = 0
            upper_row = row - 1
            if upper_row>=0 and val > matrix[upper_row][col]:
                upper_lip = state[upper_row][col] + 1

            right_lip = 0
            right_col = col+1
            if right_col<n and val > matrix[row][right_col]:
                right_lip = state[row][right_col] + 1

            down_lip = 0
            down_row = row + 1
            if down_row < m and val > matrix[down_row][col]:
                down_lip = state[down_row][col] + 1
            
            left_lip = 0
            left_col = col - 1
            if left_col >= 0 and val > matrix[row][left_col]:
                left_lip = state[row][left_col] + 1
   
            state[row][col] = max(state[row][col], upper_lip, right_lip, down_lip, left_lip)


        # traverse state and find max lip.
        max_lip = 0
        for row in state:
            for cell in row:
                max_lip = max(max_lip, cell)
        return max_lip
     
if __name__ == '__main__':
    import sys
    import time

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
        {"n": 1, "matrix": [[9, 9, 4], [6, 6, 8], [2, 1, 1]], "expected": 4},
        {"n": 2, "matrix": [[3, 4, 5], [3, 2, 6], [2, 2, 1]], "expected": 4},
        {"n": 3, "matrix": [[1]], "expected": 1},
        {"n": 4, "matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "expected": 5},
        {"n": 5, "matrix": [[1, 2, 3, 4]], "expected": 4},
        {"n": 6, "matrix": [[2, 2], [2, 2]], "expected": 1},
        {"n": 7, "matrix": [[4, 3, 2, 1]], "expected": 4},
        {"n": 8, "matrix": [[1], [2], [3], [4]], "expected": 4},
        {"n": 9, "matrix": [[7, 8, 9], [9, 7, 6], [7, 2, 3]], "expected": 6},
        {"n": 10, "matrix": [[3, 4, 5], [3, 2, 1], [4, 4, 4]], "expected": 4},
        {"n": 11, "matrix": [[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], "expected": 10},
        {"n": 12, "matrix": [[5, 4, 3], [2, 1, 0]], "expected": 4},
        {"n": 13, "matrix": [[1, 2], [2, 3]], "expected": 3},
        {
            "n": 14,
            "matrix": [[1, 2, 3, 4, 5], [16, 17, 18, 19, 20], [11, 12, 13, 14, 15], [6, 7, 8, 9, 10]],
            "expected": 7,
        },
        {
            "n": 15,
            "matrix": [[i + j for j in range(20)] for i in range(20)],
            "expected": 39,
        },
    ]

    solution = Solution()

    t1 = int(time.time() * 1000)

    for index, test in enumerate(tests, 1):
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        matrix = test["matrix"]
        expected = test["expected"]

        try:
            print(f"\nTEST {index} matrix={matrix}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.longestIncreasingPath(matrix)
            if result != expected:
                print(f"test {index} FAIL: n={test['n']}")
                print(f"  got:      {result}")
                print(f"  expected: {expected}")
            else:
                print(f"test {index} OK: n={test['n']} (result={result})")
        except Exception as e:
            print(f"test {index} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")

