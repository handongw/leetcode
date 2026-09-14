from typing import List

class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        n = len(nums)
        i = 0
        
        while i < n:
            v = nums[i]
            # Check if v is in the valid target range [1, n]
            if 1 <= v <= n:
                idx = v - 1
                # If target position already has correct value, move on
                if nums[idx] == v:
                    i += 1
                else:
                    # Swap v to its correct target index
                    nums[i], nums[idx] = nums[idx], nums[i]
            else:
                # Out-of-bounds numbers are left alone; advance pointer
                i += 1

        # Find the first index missing its corresponding number (k + 1)
        for k in range(n):
            if nums[k] != k + 1:
                return k + 1

        return n + 1