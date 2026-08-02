from re import DEBUG
from typing import List

DEBUG = False

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        if DEBUG:
            print(f"nums={nums}")    

        n = len(nums) # 2 <= nums.length <= 105
        endOf = [1] * n
        startOf = [1] * n

        prod = 1
        for i in range(n):
            prod *= nums[i]
            endOf[i] = prod
        if DEBUG:
            print(f"endOf={endOf}")    

        prod = 1
        for i in reversed(range(n)):
            prod *= nums[i]
            if DEBUG:
                print(f"    startOf nums[{i}]={nums[i]} prod={prod}")
            startOf[i] = prod    
            if DEBUG:
                print(f"    startOf[{i}] = {prod}")
        if DEBUG:        
            print(f"startOf={startOf}")    

        result = [1] * n
        for k in range(n):
            if k<=0:
                result[k] = startOf[1]
            elif k==n-1:
                result[k] = endOf[n-2]
            else:
                result[k] = endOf[k-1] * startOf[k+1]        

        return result

if __name__ == '__main__':
    sol = Solution()

    nums = [1,2,3,4]
    output = [24,12,8,6]
    result = sol.productExceptSelf(nums)
    print(f"nums={nums} expected={output} result={result}")


