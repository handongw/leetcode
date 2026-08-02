from re import DEBUG
from typing import List

DEBUG = False

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        if DEBUG:
            print(f"nums={nums}")    

        n = len(nums) # 2 <= nums.length <= 105
        endOf = [1] * n
        # startOf = [1] * n

        prod = 1
        for i in range(n):
            prod *= nums[i]
            endOf[i] = prod
        if DEBUG:
            print(f"endOf={endOf}")    

        result = [1] * n
        prod = 1
        for i in reversed(range(n)):
            if i == n-1:
                result[i] = endOf[i-1]
            elif i == 0:
                result[i] = prod    
            else:
                result[i] = endOf[i-1] * prod

            prod *= nums[i]

        return result

if __name__ == '__main__':
    sol = Solution()

    nums = [1,2,3,4]
    output = [24,12,8,6]
    result = sol.productExceptSelf(nums)
    print(f"nums={nums} expected={output} result={result}")


