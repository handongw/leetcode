# Given an integer num, return three consecutive integers (as a sorted array) that sum to num. 
# If num cannot be expressed as the sum of three consecutive integers, return an empty array.
# 0 <= num <= 1015

from typing import List


class Solution:
    def sumOfThree(self, num: int) -> List[int]:
        if num == 0:
            return [-1, 0, 1]
        if num < 3:
            return []    

        k = (num-3)//3
        if k * 3 == num - 3:
            return [k, k+1, k+2]
        else:
            return []

if __name__ == "__main__":
    sol = Solution()
    
    num = 33
    expected = [10,11,12]
    result = sol.sumOfThree(num)



 