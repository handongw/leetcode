# Given an integer array nums, reorder it such that nums[0] < nums[1] > nums[2] < nums[3]....
# You may assume the input array always has a valid answer.
# Constraints:

# 1 <= nums.length <= 5 * 104
# 0 <= nums[i] <= 5000
# It is guaranteed that there will be an answer for the given input nums.

DEBUG = False

from typing import List


class Solution:
    def wiggleSort(self, nums: List[int]) -> None:
        nums2 = sorted(nums)         # Let's get a working version for now
        midIdx = (len(nums)-1) // 2  # left middle of nums length is even
        if DEBUG:
            print(f"nums2={nums2} n={len(nums)} midIdx={midIdx}")

        def reverse_nums(array, lo, hi):
            while lo < hi:
                x = array[lo]
                array[lo] = array[hi]
                array[hi] = x
                lo += 1
                hi -= 1     

        # reverse nums from [0, midIdx]
        reverse_nums(nums2, 0, midIdx)

        # reverse nums from [midIdx+1, n-1]
        if midIdx < len(nums):
            reverse_nums(nums2, midIdx+1, len(nums)-1)

        if DEBUG:
            print(f"reversed nums2={nums2}")    

        #interleave [0, midIdx] and [midIdx+1, n-1]
        for i in range(midIdx+1):
            if DEBUG:
                print(f"nums[{i*2}]=nums2[{i}]={nums2[i]}")
            nums[i*2] = nums2[i] 

        for i in range(midIdx+1, len(nums)):
            if DEBUG:
                print(f"nums[{1 + (i-midIdx-1)*2}]=nums2[{i}]={nums2[i]}")
            nums[1 + (i-midIdx-1)*2] = nums2[i]        


def is_wiggle(nums: List[int]) -> bool:
    """Check nums[0] < nums[1] > nums[2] < nums[3] ..."""
    for i in range(1, len(nums)):
        if i % 2 == 1:
            if not (nums[i - 1] < nums[i]):
                return False
        else:
            if not (nums[i - 1] > nums[i]):
                return False
    return True


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
        {"n": 1, "nums": [1, 5, 1, 1, 6, 4], "expected": [1, 6, 1, 5, 1, 4]},
        {"n": 2, "nums": [1, 3, 2, 2, 3, 1], "expected": [2, 3, 1, 3, 1, 2]},
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        nums = list(test["nums"])
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} nums={test['nums']!r}")
            if DEBUG:
                print(f"  expected={expected}")
            solution.wiggleSort(nums)
            same_multiset = sorted(nums) == sorted(test["nums"])
            valid = same_multiset and is_wiggle(nums)
            if not valid:
                print(f"test {test['n']} FAIL")
                print(f"  got:      {nums}")
                print(f"  expected: {expected} (or any valid wiggle)")
            else:
                print(f"test {test['n']} OK: (result={nums})")
        except Exception as e:
            print(f"test {test['n']} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")
