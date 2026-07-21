from typing import List
import bisect

DEBUG = False

class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        nums.sort()
        sum = 0
        for i, n in enumerate(nums):
            sum += n
        if sum == 0:
            return True

        if sum % 2 == 1:
            return False
            
        half_sum = sum // 2

        def count_min_max_items():
            total = 0
            max_count = 0
            for v in nums:
                total += v
                max_count += 1
                if total >= half_sum:
                    break;
            
            min_count = 0   
            total = 0
            for v in reversed(nums):
                total += v
                min_count += 1
                if total >= half_sum:
                    break;

            keys = {}
            for v in nums:
                keys[v] = 1


            # In Python 3.7+ dicts preserve insertion order by default,
            # so list(keys.keys()) will keep the original insert order of unique elements.
            return min_count, max_count, list(keys.keys())
   
                    
        min_count, max_count, uniq_numbers = count_min_max_items()

        # get

        print(f" half sum={half_sum} nums size={len(nums)} avg={sum/len(nums)} min count={min_count} max_count={max_count}"
              f" uniq_numbers={uniq_numbers}")

        def splitNums(nums, idx_set, rem_idx_set, partial_nums, partial_sum, memo):
            if partial_sum == half_sum:
                return True

            key = tuple(partial_nums)

            if partial_sum > half_sum:
                if DEBUG:
                    print(f"    stop {partial_nums}")
                memo["failed"].add(key)            
                return False

            if key in memo["failed"]:
                if DEBUG:
                    print(f"    skip {partial_nums}")
                return False

            memo["failed"].add(key)            
            if DEBUG:
                    print(f"    continue {len(idx_set)} {partial_nums}")
    
            val_set=set()
            for i in range(len(nums)):
                if i not in idx_set and nums[i] not in val_set:
                    if partial_sum+nums[i] > half_sum:
                        if DEBUG:
                            print(f"    stop {partial_nums}")
                        break # nums are sorted. no need to try the remaining larger numbers

                    idx_set2 = idx_set.copy()
                    idx_set2.add(i)
                    rem_idx_set2 = rem_idx_set.copy()
                    rem_idx_set2.remove(i)
                    partial_nums2 = partial_nums[:]
                    partial_nums2.append(nums[i])
                    val_set.add(nums[i])
                    # bisect.insort(partial_nums2, nums[i])
                    result = splitNums(nums, idx_set2, rem_idx_set2, partial_nums2, partial_sum+nums[i], memo)
                    if result:
                        return True
            return False            

        return splitNums(nums, set(), set(range(len(nums))), [], 0, {"failed":set()})

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
            "expected": True,
        },
    ]

    solution = Solution()

    t1 = int(time.time() * 1000)

    for index, test in enumerate(tests, 1):
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        nums = test["nums"]
        expected = test["expected"]

        try:
            print(f"\nTEST {index} nums={nums}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.canPartition(nums)
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
