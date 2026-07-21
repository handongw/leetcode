from typing import List
from functools import cache

class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        total_sum = sum(nums)
        if total_sum % 2 != 0:
            return False
            
        target = total_sum // 2
        nums.sort(reverse=True) # Process largest numbers first
        
        # Precompute suffix sums: suffix_sums[i] is the sum of nums[i] to the end
        suffix_sums = [0] * (len(nums) + 1)
        for i in range(len(nums) - 1, -1, -1):
            suffix_sums[i] = suffix_sums[i + 1] + nums[i]
        
        @cache
        def dfs(index: int, current_target: int) -> bool:
            if current_target == 0:
                return True
                
            # PRUNING 1: If we run out of numbers, or if ALL remaining numbers 
            # combined cannot reach the current_target, turn back immediately.
            if index >= len(nums) or current_target > suffix_sums[index]:
                return False
            
            # PRUNING 2: Only branch into 'include' if the number actually fits
            if nums[index] <= current_target:
                if dfs(index + 1, current_target - nums[index]):
                    return True
            
            # Choice 2: Exclude the number
            return dfs(index + 1, current_target)

        return dfs(0, target)
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
        {"n": 0, "nums": [7, 10, 11, 18, 18, 19, 24, 32, 49], "expected": True},
        {"n": 1, "nums": [1, 5, 11, 5], "expected": True},
        {"n": 2, "nums": [1, 2, 3, 5], "expected": False},
        {"n": 3, "nums": [1, 1], "expected": True},
        {"n": 4, "nums": [1], "expected": False},
        {"n": 5, "nums": [2, 2, 3, 5], "expected": False},
        {"n": 6, "nums": [4, 4, 4, 4, 4], "expected": False},
        {"n": 7, "nums": [1, 2, 3], "expected": True},
        {"n": 8, "nums": [1, 2, 5], "expected": False},
        {"n": 9, "nums": [1, 2, 3, 4, 5, 6, 7], "expected": True},
        {"n": 10, "nums": [100], "expected": False},
        {"n": 11, "nums": [1, 1, 1, 1], "expected": True},
        {"n": 12, "nums": [1, 2, 4, 8, 16, 32], "expected": False},
        {"n": 13, "nums": [3, 3, 3, 3, 3, 3], "expected": True},
        {"n": 14, "nums": [2, 2, 2, 2, 2, 2, 2, 2, 2, 2], "expected": True},
        {"n": 15, "nums": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "expected": False},
        {
            "n": 16,
            "nums": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20],
            "expected": True,
        },
        {
            "n": 17,
            "nums": list(range(1, 101)),
            "expected": True,
        },
        {
            "n": 18,
            "nums": [1] * 200,
            "expected": True,
        },
        {
            "n": 19,
            "nums": [100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,99,97],
            "expected": False,
        },
        {
            "n": 20,
            "nums": [4,4,4,4,4,4,4,4,8,8,8,8,8,8,8,8,12,12,12,12,12,12,12,12,16,16,16,16,16,16,16,16,20,20,20,20,20,20,20,20,24,24,24,24,24,24,24,24,28,28,28,28,28,28,28,28,32,32,32,32,32,32,32,32,36,36,36,36,36,36,36,36,40,40,40,40,40,40,40,40,44,44,44,44,44,44,44,44,48,48,48,48,48,48,48,48,52,52,52,52,52,52,52,52,56,56,56,56,56,56,56,56,60,60,60,60,60,60,60,60,64,64,64,64,64,64,64,64,68,68,68,68,68,68,68,68,72,72,72,72,72,72,72,72,76,76,76,76,76,76,76,76,80,80,80,80,80,80,80,80,84,84,84,84,84,84,84,84,88,88,88,88,88,88,88,88,92,92,92,92,92,92,92,92,96,96,96,96,96,96,96,96,97,99],
            "expected": False,
        },
        {
            "n": 21,
            "nums": [91,29,92,14,53,27,96,97,58,76,56,51,68,18,37,98,30,37,25,65,95,22,34,25,29,37,54,34,43,18,65,31,21,91,9,57,13,72,31,26,36,77,85,70,5,72,93,39,46,50,22,16,6,67,17,41,42,10,56,66,69,53,79,46,14,34,80,31,86,78,35,64,75,88,58,26,56,91,84,38,44,19,49,8,4,78,11,13,10,56,72,97,25,62,97,80,20,63,5,27],
            "expected": True
        },
        {
            "n": 22,
            "nums": [89,49,21,31,74,56,34,23,35,15,74,59,75,47,16,81,1,32,42,75,4,3,54,55,95,65,10,90,15,23,19,30,24,91,3,84,11,76,6,96,78,84,58,80,28,96,11,46,36,84,3,14,32,86,67,8,60,70,65,57,63,15,61,79,66,55,92,44,62,76,19,52,59,72,2,60,75,52,37,100,1,92,1,40,11,68,61,22,88,70,50,82,81,39,80,75,67,31,3,55],
            "expected": True
        },
        {
            "n": 23,
            "nums": [67,95,58,76,19,60,20,17,23,23,67,85,8,67,81,65,73,92,59,97,45,94,26,90,70,45,24,52,25,43,2,83,15,25,66,87,77,11,46,75,46,59,17,84,11,64,9,74,65,78,85,3,87,81,67,37,79,50,14,88,55,45,58,31,75,74,13,2,60,51,94,82,63,90,25,60,86,12,42,78,33,8,50,84,86,71,46,47,15,86,56,64,8,26,34,21,21,24,49,16],
            "expected": True
        },
    ]

    solution = Solution()

    t1 = int(time.time() * 1000)

    for index, test in enumerate(tests, 1):
        if selected_tests is not None and index not in selected_tests:
            continue

        nums = test["nums"]
        expected = test["expected"]

        try:
            print(f"\nTEST {index} nums={nums}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.canPartition(nums)
            if result != expected:
                print(f"test {index} FAIL")
                print(f"  got:      {result}")
                print(f"  expected: {expected}")
            else:
                print(f"test {index} OK: (result={result})")
        except Exception as e:
            print(f"test {index} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")
