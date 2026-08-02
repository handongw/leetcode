from typing import List

DEBUG = False

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums) # 2 <= nums.length <= 105
        if DEBUG:
            print(f"nums={nums}")    

        if n == 2:
            return [nums[1], nums[0]]    

        # endOf = [1] * n
        result = [1] * n
        # startOf = [1] * n

        prod = 1
        for i in range(n-1):
            prod *= nums[i]
            result[i+1] = prod

        prod = nums[n-1]
        for i in reversed(range(n-1)):
            if i == 0:
                result[i] = prod    
            else:
                result[i] = result[i] * prod

            prod *= nums[i]

        return result

if __name__ == '__main__':
    sol = Solution()

    nums = [1,2,3,4]
    output = [24,12,8,6]
    result = sol.productExceptSelf(nums)
    print(f"nums={nums} expected={output} result={result}")


