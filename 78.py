
from typing import List


class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        """ 
            Given an integer array nums of unique elements, return all possible subsets (the power set).
            The solution set must not contain duplicate subsets. Return the solution in any order.
        """
       
        result = [[]]
        for v in nums:
            n = len(result)
            for j in range(n):
                newItem = result[j][:]
                newItem.append(v)
                result.append(newItem)
        return result


def _subsets_equal(a: List[List[int]], b: List[List[int]]) -> bool:
    """Compare as sets of subsets (order-independent)."""
    sa = {tuple(sorted(x)) for x in a}
    sb = {tuple(sorted(x)) for x in b}
    return sa == sb


if __name__ == '__main__':
    tests = [
        {
            "nums": [1, 2, 3],
            "expected": [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]],
        },
        {
            "nums": [0], 
            "expected": [[], [0]]
        },
    ]

    solution = Solution()

    for index, test in enumerate(tests, 1):
        nums = test["nums"]
        expected = test["expected"]

        try:
            result = solution.subsets(nums)
            ok = _subsets_equal(result, expected)
            if not ok:
                print(f"test {index} FAIL: nums={nums}")
                print(f"  got:      {result}")
                print(f"  expected: {expected}")
            else:
                print(f"test {index} OK: nums={nums} ({len(result)} subsets)")
        except Exception as e:
            print(f"test {index} ERROR: {e}")
            raise
