from typing import List

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        # looking for missing [1...n]
        for i in range(n):
            v = nums[i]
            if v <=0 or v > n:
                nums[i] = -1    # vacant cell
        # print(f"normalized nums={nums}")

        i = 0
        while i < n:
            v = nums[i]
            if v >= 1:
                idx = v-1
                # put v at nums[idx]
                if nums[idx] < 0:
                    nums[idx] = v
                    nums[i] = -1
                    i += 1
                elif nums[idx] == v:
                    if idx == i:
                        # v is at right place. do nothing
                        pass
                    else:
                        # duplicate v
                        nums[i] = -1
                    i += 1
                else:
                    # nums[idx] is occupied by another number between 1..n
                    another_number = nums[idx]
                    nums[idx] = v
                    nums[i] = another_number
            else:
                i += 1        

        # print(f"nums={nums}")
        for k in range(n):
            if nums[k] < 0:
                return k+1
        return n+1        

        