# You are given an integer array nums. The absolute sum of a subarray [numsl, numsl+1, ..., numsr-1, numsr] is abs(numsl + numsl+1 + ... + numsr-1 + numsr).
# Return the maximum absolute sum of any (possibly empty) subarray of nums.
# Note that abs(x) is defined as follows:
#     If x is a negative integer, then abs(x) = -x.
#     If x is a non-negative integer, then abs(x) = x.

# Constraints:
#     1 <= nums.length <= 105
#     -104 <= nums[i] <= 104
DEBUG = False

from typing import List


class Solution:
    def maxAbsoluteSum(self, nums: List[int]) -> int:
        # n = len(nums)
        # if n <= 0:
        #     return 0
        # if n == 1:
        #     return abs(nums[0])

        answer = 0
        # dp = [nums[-1], nums[-1]] # [min sum of sub array, max sum of sub array]
        minSubArraySum = 0
        maxSubArraySum = 0

        if DEBUG:
            print(f"dp={(minSubArraySum, maxSubArraySum)} answer={answer}")

        for v in reversed(nums):
            m1 = minSubArraySum + v
            m2 = maxSubArraySum + v



            # answer = max(answer, abs(v), abs(m1), abs(m2))
            minSubArraySum = min(v, m1)
            maxSubArraySum = max(v, m2) 

            answer = max(answer, abs(minSubArraySum), abs(maxSubArraySum))

            if DEBUG:
                print(f"dp={(minSubArraySum, maxSubArraySum)} v={v} answer={answer}")      

        return answer


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
        # examples
        {"n": 1, "nums": [1, -3, 2, 3, -4], "expected": 5},
        {"n": 2, "nums": [2, -5, 1, -4, 3, -2], "expected": 8},
        # all positive / all negative
        {"n": 3, "nums": [1, 2, 3, 4], "expected": 10},
        {"n": 4, "nums": [-1, -2, -3, -4], "expected": 10},
        # single element
        {"n": 5, "nums": [5], "expected": 5},
        {"n": 6, "nums": [-5], "expected": 5},
        # large positive at begin / middle / end
        {"n": 7, "nums": [100, 1, 2], "expected": 103},
        {"n": 8, "nums": [1, 100, 2], "expected": 103},
        {"n": 9, "nums": [1, 2, 100], "expected": 103},
        # large negative at begin / middle / end
        {"n": 10, "nums": [-100, 1, 2], "expected": 100},
        {"n": 11, "nums": [1, -100, 2], "expected": 100},
        {"n": 12, "nums": [1, 2, -100], "expected": 100},
        # large positive/negative surrounded by opposite signs
        {"n": 13, "nums": [-1, 50, -1], "expected": 50},
        {"n": 14, "nums": [1, -50, 1], "expected": 50},
        # zeros / mix where abs comes from negative sum
        {"n": 15, "nums": [0, 0, 0], "expected": 0},
        {"n": 16, "nums": [5, -10, 5], "expected": 10},
        {"n": 17, "nums": [3, -1, 2, -1, 3], "expected": 6},
        {"n": 18, "nums": [-2, -3, 4, -1, -2], "expected": 5},
        {"n": 19, "nums": [10, -3, -4, 7], "expected": 10},
        {"n": 20, "nums": [-10, 3, 4, -7], "expected": 10},
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        nums = test["nums"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} nums={nums!r}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.maxAbsoluteSum(nums)
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
