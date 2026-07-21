from typing import List


class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        i = len(nums) -1
        globalMaxSum = 0

        if i < 0:
            return globalMaxSum

        # nums[i] > 0 at this moment

        # globalMaxSum - final result
        # localMaxSum - result of substring that starts at index i
        localMaxSum = globalMaxSum = nums[i]

        i -= 1
        while i >= 0:
            if localMaxSum > 0:
                localMaxSum += nums[i]
            else:
                localMaxSum = nums[i]

            i -= 1    
            globalMaxSum = max(localMaxSum, globalMaxSum)

        return globalMaxSum                 

if __name__ == "__main__":
    solver = Solution()

    test_cases = [
        {
            "nums": [-2,1,-3,4,-1,2,1,-5,4],
            "expected": 6,
        },
        {
            "nums": [1],
            "expected": 1,
        },
        {
            "nums": [5,4,-1,7,8],
            "expected": 23,
        },
        {
            "nums": [-1],
            "expected": -1,
        },
    ]

    for idx, case in enumerate(test_cases, start=1):
        nums = case["nums"]
        expected = case["expected"]
        try:
            actual = solver.maxSubArray(nums)
            print(f"Case {idx}:")
            print(f"  nums={nums}")
            print(f"  expected={expected}")
            print(f"  actual  ={actual}")
            print(f"  pass    ={actual == expected}")
            print("\n")
        except Exception as exc:
            print(f"Case {idx} raised an exception: {exc}")        