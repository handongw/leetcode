import sys
import time
import copy

from typing import List

'''130. Surrounded Regions'''
class Solution:
    def solve(self, board: List[List[str]]) -> None:
        m = len(board)
        if m<=1:
            return
        n = len(board[0])
        if n<=1:
            return

        cells_to_restore = []

        def scan_connected(i, j, isEdge):
            stack = []
            stack.append((i, j))

            while len(stack) > 0:
                row, col = stack.pop()
                # print(f" row={row} col={col}")
                if isEdge:
                    board[row][col] = '_'
                    cells_to_restore.append((row, col))
                else:
                    board[row][col] = 'X'    

                # upper
                if isEdge:
                    row_up = row - 1
                    if row_up >= 0 and board[row_up][col] == 'O':
                        stack.append((row_up, col))                    
                    # right
                    col_right = col + 1
                    if col_right < n and board[row][col_right] == 'O':
                        stack.append((row, col_right))
                    # bottom
                    row_bottom = row + 1
                    if row_bottom < m and board[row_bottom][col] == 'O':
                        stack.append((row_bottom, col))
                    # left
                    col_left = col - 1
                    if col_left >=0 and board[row][col_left] == 'O':
                        stack.append((row, col_left))
                else:
                    row_up = row - 1
                    if board[row_up][col] == 'O':
                        stack.append((row_up, col))                    
                    # right
                    col_right = col + 1
                    if board[row][col_right] == 'O':
                        stack.append((row, col_right))
                    # bottom
                    row_bottom = row + 1
                    if board[row_bottom][col] == 'O':
                        stack.append((row_bottom, col))
                    # left
                    col_left = col - 1
                    if board[row][col_left] == 'O':
                        stack.append((row, col_left))


        for j in range(n):
            if board[0][j] == 'O':
                scan_connected(0, j, True)
            if board[m-1][j] == 'O':
                scan_connected(m-1, j, True)


        for i in range(m):
            if board[i][0] == 'O':
                scan_connected(i, 0, True)
            if board[i][n-1] == 'O':
                scan_connected(i, n-1, True)

        for i in range(1, m-1):
            for j in range(1, n-1):
               if board[i][j] == 'O':
                    board[i][j] = 'X'

        for row, col in cells_to_restore:
            board[row][col] = 'O'

        return

if __name__ == '__main__':
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

    # Test cases representing various edge conditions, multi-region configurations, and empty states
    tests = [
        {
            "n": 1,
            "board": [
                ["X", "X", "X", "X"],
                ["X", "O", "O", "X"],
                ["X", "X", "O", "X"],
                ["X", "O", "X", "X"]
            ],
            "expected": [
                ["X", "X", "X", "X"],
                ["X", "X", "X", "X"],
                ["X", "X", "X", "X"],
                ["X", "O", "X", "X"]
            ]
        },
        {
            "n": 2,
            "board": [["X"]],
            "expected": [["X"]]
        },
        {
            "n": 3,
            "board": [
                ["O", "O", "O"],
                ["O", "O", "O"],
                ["O", "O", "O"]
            ],
            "expected": [
                ["O", "O", "O"],
                ["O", "O", "O"],
                ["O", "O", "O"]
            ]
        },
        {
            "n": 4,
            "board": [
                ["X", "X", "X"],
                ["X", "O", "X"],
                ["X", "X", "X"]
            ],
            "expected": [
                ["X", "X", "X"],
                ["X", "X", "X"],
                ["X", "X", "X"]
            ]
        },
        {
            "n": 5,
            "board": [
                ["X", "O", "X", "O", "X"],
                ["O", "X", "O", "X", "O"],
                ["X", "O", "X", "O", "X"],
                ["O", "X", "O", "X", "O"]
            ],
            "expected": [
                ["X", "O", "X", "O", "X"],
                ["O", "X", "X", "X", "O"],
                ["X", "X", "X", "X", "X"],
                ["O", "X", "O", "X", "O"]
            ]
        },
        {
            "n": 6,
            "board": [],
            "expected": []
        }
    ]

    solution = Solution()

    t1 = int(time.time() * 1000)

    for index, test in enumerate(tests, 1):
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        # Deep copy to maintain clean original matrices if needed for output
        board_input = copy.deepcopy(test["board"])
        expected = test["expected"]

        try:
            print(f"\nTEST {index} - Shape: {len(board_input)}x{len(board_input[0]) if board_input else 0}")
            
            if DEBUG:
                print("Initial Board:")
                for row in board_input:
                    print(" ".join(row))
            
            # Execute the in-place operation
            solution.solve(board_input)
            
            if board_input != expected:
                print(f"test {index} FAIL: n={test['n']}")
                print("Got:")
                for row in board_input:
                    print(" ".join(row))
                print("Expected:")
                for row in expected:
                    print(" ".join(row))
            else:
                print(f"test {index} OK: n={test['n']}")
                if DEBUG:
                    print("Resulting Board:")
                    for row in board_input:
                        print(" ".join(row))
                        
        except Exception as e:
            print(f"test {index} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"\nTotal test duration: {t2 - t1} ms")

        