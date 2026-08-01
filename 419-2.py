from typing import List

DEBUG = False

class Solution:
    def countBattleships(self, board: List[List[str]]) -> int:
        m = len(board)
        n = len(board[0])
        if DEBUG:
            print(f"m={m} n={n}")

        # where to start scanning the board next iteration
        nextRow = 0
        nextCol = 0

        battleShipCount = 0

        while nextRow < m:
            # find next battleship
            while nextCol < n and board[nextRow][nextCol] == '.':
                nextCol += 1
            if nextCol >= n: # no more battleship in currnet row
                nextCol = 0
                nextRow += 1
                continue    

            # found a battleship
            battleShipCount += 1

            # is battleship horizontal or vertical or single X
            if nextCol+1 < n and board[nextRow][nextCol+1] == 'X':
                # layout = 'horizontal'
                # keep scan right ward
                c = nextCol
                while c < n and board[nextRow][c] == 'X':
                    board[nextRow][c] = '.' # consume the cell
                    c += 1
            elif nextRow+1 < m and board[nextRow+1][nextCol] == 'X':
                # layout = 'vertical'
                # scan down ward
                r = nextRow
                if DEBUG:
                    print(f"    vertical r={nextRow} nextCol={nextCol}")
                while r < m and board[r][nextCol] == 'X':
                    board[r][nextCol] = '.' # consume the cell
                    r += 1 
            else:
                # layout = 'single'
                board[nextRow][nextCol] = '.'               
            
            nextCol += 1
            if nextCol >= n:
                nextCol = 0
                nextRow += 1

        return battleShipCount

        
        

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
        {
            "n": 1,
            "board": [["X", ".", ".", "X"], [".", ".", ".", "X"], [".", ".", ".", "X"]],
            "expected": 2,
        },
        {
            "n": 2,
            "board": [["."]],
            "expected": 0,
        },
        {
            "n": 3,
            "board": [["X", "X", "X"]],
            "expected": 1,
        },
        {
            "n": 4,
            "board": [[".", "."], ["X", "X"]],
            "expected": 1,
        },
        {
            "n": 5,
            "board": [[".", "X"], ["X", "."]],
            "expected": 2,
        },
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        # deep-copy board since solution mutates it
        board = [row[:] for row in test["board"]]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} board={test['board']!r}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.countBattleships(board)
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
