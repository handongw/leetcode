from functools import cache
from math import ceil


DEBUG = False

class Solution:
    def countTexts(self, pressedKeys: str) -> int:

        keyToLetters = {
            "2": 3,
            "3": 3,
            "4": 3,
            "5": 3,
            "6": 3,
            "7": 4,
            "8": 3,
            "9": 4,
        }

        smallResult = [None,1,2,4,8]
        
        MOD = 10**9 + 7

        countCache = {}

        # @cache
        def countMsgs(keyCnt, m):
            if keyCnt <= m:
                return smallResult[keyCnt]

            
            if keyCnt < 1_000_000:
                cacheKey = f"{keyCnt}/{m}"
            else:
                cacheKey = None

            if cacheKey is not None and cacheKey in countCache:
                return countCache[cacheKey]

            sum = 0
            for i in range(1, m+1):
                sum += countMsgs(keyCnt-i, m)    

            if cacheKey is not None:
                countCache[cacheKey] = sum

            return sum

        totalMsgs = 1
        # scan continuous keys in pressedKeys
        lo = 0
        hi = 0
        key = pressedKeys[hi]
        n = len(pressedKeys)

        while hi <= len(pressedKeys):
            if DEBUG:
                print(f"    lo={lo} hi={hi} key={key}")
            if hi <n and pressedKeys[hi] == key:
                hi += 1
            else: # end of continuous keys
                subTotal = countMsgs(hi-lo, keyToLetters[key])
                if DEBUG:
                    print(f"continuous keys={pressedKeys[lo:hi]} cnt={hi-lo} subTotal={subTotal}")  
                   
                totalMsgs = totalMsgs * subTotal
                totalMsgs = totalMsgs % MOD
                lo = hi
                if lo < n:
                    key = pressedKeys[lo]
                else:
                    break

        return totalMsgs


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
        {"n": 1, "pressedKeys": "22233", "expected": 8},
        {"n": 2, "pressedKeys": "222222222222222222222222222222222222", "expected": 82876089},
        {"n": 3, "pressedKeys": "7777", "expected": 8},
        {"n": 4, "pressedKeys": "777333", "expected": 16},
        {"n": 5, "pressedKeys": "222222", "expected": 24},
        {"n": 6, "pressedKeys": "2222", "expected": 7},
        {"n": 7, "pressedKeys": "77777", "expected": 15},
        {"n": 8, "pressedKeys": "444444444444444444444444444444448888888888888888999999999999333333333333333366666666666666662222222222222222666666666666666633333333333333338888888888888888222222222222222244444444444444448888888888888222222222222222288888888888889999999999999999333333333444444664", "expected": 537551452},
        {"n": 9, "pressedKeys": "4444", "expected": 7},
        {"n": 10, "pressedKeys": "6666", "expected": 7},
        {"n": 11, "pressedKeys": "8888", "expected": 7},
        {"n": 12, "pressedKeys": "99999", "expected": 15},
        {"n": 13, "pressedKeys": "5555", "expected": 7},
        {"n": 14, "pressedKeys": "44444444444444444444444444444444", "expected": 181997601},
        {"n": 15, "pressedKeys": "8888888888888888", "expected": 10609},
        {"n": 16, "pressedKeys": "999999999999", "expected": 1490},
        {"n": 17, "pressedKeys": "3333333333333333", "expected": 10609},
        {"n": 18, "pressedKeys": "6666666666666666", "expected": 10609},
        {"n": 19, "pressedKeys": "2222222222222222", "expected": 10609},
        {"n": 20, "pressedKeys": "6666666666666666", "expected": 10609},
        {"n": 21, "pressedKeys": "3333333333333333", "expected": 10609},
        {"n": 22, "pressedKeys": "8888888888888888", "expected": 10609},
        {"n": 23, "pressedKeys": "2222222222222222", "expected": 10609},
        {"n": 24, "pressedKeys": "4444444444444444", "expected": 10609},
        {"n": 25, "pressedKeys": "8888888888888", "expected": 1705},
        {"n": 26, "pressedKeys": "2222222222222222", "expected": 10609},
        {"n": 27, "pressedKeys": "8888888888888", "expected": 1705},
        {"n": 28, "pressedKeys": "9999999999999999", "expected": 20569},
        {"n": 29, "pressedKeys": "333333333", "expected": 149},
        {"n": 30, "pressedKeys": "444444", "expected": 24},
        {"n": 31, "pressedKeys": "66", "expected": 2},
        {"n": 32, "pressedKeys": "4", "expected": 1},
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        pressedKeys = test["pressedKeys"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} pressedKeys={pressedKeys!r}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.countTexts(pressedKeys)
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
