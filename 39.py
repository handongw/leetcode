from typing import List

"""
Given an array of distinct integers candidates and a target integer target,
return a list of all unique combinations of candidates where the chosen numbers
sum to target. The same number may be chosen from candidates an unlimited
number of times. Two combinations are unique if the frequency of at least one
of the chosen numbers is different.

The test suite below is for combinationSum.

1 <= candidates.length <= 30
2 <= candidates[i] <= 40
All elements of candidates are distinct.
1 <= target <= 40

Example 1:
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]

Example 2:
Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]

Example 3:
Input: candidates = [2], target = 1
Output: []
"""


class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        valid_candidates = []

        for num in candidates:
            if num <= target:
                valid_candidates.append(num)

        candidates = valid_candidates
            
        result = []
            
        def loop(index, current_subset, current_sum):
            if current_sum > target:
                return
                
            if index == len(candidates):
                return
            
            if current_sum + candidates[index] == target:
                result.append(current_subset + [candidates[index]])
            
            current_subset.append(candidates[index])
            loop(index, current_subset, current_sum + candidates[index])
            
            current_subset.pop()
            loop(index + 1, current_subset, current_sum)
            
        loop(0, [], 0)
        return result

def _normalize(combos: List[List[int]]) -> List[List[int]]:
    return sorted(sorted(c) for c in combos)


def _brute_combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """Reference solver for building large-test expected output."""
    candidates = sorted(c for c in candidates if c <= target)
    out: List[List[int]] = []

    def dfs(start: int, rem: int, path: List[int]) -> None:
        if rem == 0:
            out.append(path[:])
            return
        for i in range(start, len(candidates)):
            c = candidates[i]
            if c > rem:
                break
            path.append(c)
            dfs(i, rem - c, path)
            path.pop()

    dfs(0, target, [])
    return sorted(sorted(x) for x in out)


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
                f"Unknown argument: {a!r} (use -d and/or 1-based test indices, e.g. 1 2 3)",
                file=sys.stderr,
            )
            sys.exit(2)

    if selected_tests is not None and len(selected_tests) == 0:
        print("Test selection is empty.", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"selected_tests={selected_tests}")

    _large_candidates = list(range(2, 32))

    tests = [
        {
            "n": 1,
            "candidates": [2, 3, 6, 7],
            "target": 7,
            "expected": [[2, 2, 3], [7]],
        },
        {
            "n": 2,
            "candidates": [2, 3, 5],
            "target": 8,
            "expected": [[2, 2, 2, 2], [2, 3, 3], [3, 5]],
        },
        {
            "n": 3,
            "candidates": [2],
            "target": 1,
            "expected": [],
        },
        {
            "n": 4,
            "candidates": [5],
            "target": 5,
            "expected": [[5]],
        },
        {
            "n": 5,
            "candidates": [3, 5],
            "target": 2,
            "expected": [],
        },
        {
            "n": 6,
            "candidates": [2, 4],
            "target": 6,
            "expected": [[2, 2, 2], [2, 4]],
        },
        {
            "n": 7,
            "candidates": [1, 2],
            "target": 3,
            "expected": [[1, 1, 1], [1, 2]],
        },
        {
            "n": 8,
            "candidates": [2, 3],
            "target": 5,
            "expected": [[2, 3]],
        },
        {
            "n": 9,
            "candidates": [7, 3, 2],
            "target": 18,
            "expected": [
                [2, 2, 2, 2, 2, 2, 2, 2, 2],
                [2, 2, 2, 2, 2, 2, 3, 3],
                [2, 2, 2, 2, 3, 7],
                [2, 2, 2, 3, 3, 3, 3],
                [2, 2, 7, 7],
                [2, 3, 3, 3, 7],
                [3, 3, 3, 3, 3, 3],
            ],
        },
        {
            "n": 10,
            "candidates": [8, 7, 4, 3],
            "target": 11,
            "expected": [[3, 4, 4], [3, 8], [4, 7]],
        },
        {
            "n": 11,
            "candidates": [40],
            "target": 40,
            "expected": [[40]],
        },
        {
            "n": 12,
            "candidates": [2, 3, 5],
            "target": 1,
            "expected": [],
        },
        {
            "n": 13,
            "candidates": _large_candidates,  # 30 distinct values, max length
            "target": 40,  # max target; 6131 combinations
            "expected": _brute_combination_sum(_large_candidates, 40),
        },
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        candidates = test["candidates"]
        target = test["target"]
        expected = test["expected"]

        try:
            if len(candidates) > 12:
                cand_repr = f"len={len(candidates)} range=[{min(candidates)}..{max(candidates)}]"
            else:
                cand_repr = str(candidates)
            print(f"\nTEST {test['n']} candidates={cand_repr} target={target}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.combinationSum(candidates, target)
            if _normalize(result) != _normalize(expected):
                print(f"test {test['n']} FAIL")
                print(f"  got:      {result}")
                print(f"  expected: {expected}")
            else:
                print(f"test {test['n']} OK: (count={len(result)})")
        except Exception as e:
            print(f"test {test['n']} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")
