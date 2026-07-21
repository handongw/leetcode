from typing import List


class Solution:
    def missingNumber(self, nums: List[int]) -> int:

        result = len(nums) * (len(nums)+1) // 2
        for i in nums:
            result -= i
        
        return result if result>=0 else 0


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
        {"n": 1, "nums": [3, 0, 1], "expected": 2},
        {"n": 2, "nums": [0, 1], "expected": 2},
        {"n": 3, "nums": [9, 6, 4, 2, 3, 5, 7, 0, 1], "expected": 8},
        {"n": 4, "nums": [0], "expected": 1},
        {"n": 5, "nums": [1], "expected": 0},
        {"n": 6, "nums": [1, 0], "expected": 2},
        {"n": 7, "nums": [2, 0, 1], "expected": 3},
        {"n": 8, "nums": list(range(0, 100))[:-50] + list(range(51, 101)), "expected": 50},  # missing 50 in 0..100
        {"n": 9, "nums": list(range(101))[:-1], "expected": 100},
        {"n": 10, "nums": [0, 2, 3, 4, 5], "expected": 1},
        {"n": 11, "nums": [5, 4, 3, 2, 0], "expected": 1},
        {"n": 12, "nums": [1, 2, 3, 4, 6, 7, 8, 9, 10, 11], "expected": 0},
        {"n": 13, "nums": list(range(500)), "expected": 500},  # missing 500 when len=500, range 0..499 present
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        nums = test["nums"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} nums={nums if len(nums) <= 20 else f'len={len(nums)}'}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.missingNumber(nums)
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
