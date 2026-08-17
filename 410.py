# Constraints:

# 1 <= nums.length <= 1000
# 0 <= nums[i] <= 106
# 1 <= k <= min(50, nums.length)

from functools import cache
from typing import List

class Solution:
    def splitArray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # assume n >= k

        # compute prefix array
        prefix = [0] * n
        prefix_sum = 0
        for i, v in enumerate(nums):
            prefix_sum += v
            prefix[i] = prefix_sum

        def sum_of_subarray(start_idx, last_idx):
            ''' [lo_idx, hi_idx] are inclusive '''
            if start_idx == 0:
                return prefix[last_idx]
            # if start_idx == last_idx:
            #     return nums[start_idx]
            return prefix[last_idx] - prefix[start_idx-1]            


        @cache
        def sub_array_max(lo_idx,hi_idx):
            ''' [lo_idx, hi_idx] are inclusive '''
            m = nums[lo_idx]
            lo_idx += 1
            while lo_idx <= hi_idx:
                m = max(m, nums[lo_idx])
                lo_idx += 1
            return m    

        @cache
        def min_max_sum(lo_idx, hi_idx, k): 
            ''' [lo_idx, hi_idx] are inclusive '''
            if k == 1:
                return sum_of_subarray(lo_idx, hi_idx) # single sub array

            #e.g. lo_idx=0, hi_idx=3, k=4
            if hi_idx - lo_idx +1 == k:
                return sub_array_max(lo_idx, hi_idx) # only one way to split [lo, hi] sub array
            
            # e.g lo_idx=0, hi_idx=9, k=3
            mid_idx = hi_idx # mid_idx = 9
            result = prefix[n-1]
            while mid_idx >= k+lo_idx-1: # mid_idx >=2
                right_min_max_sum = sum_of_subarray(mid_idx, hi_idx)
                left_min_max_sum = min_max_sum(lo_idx, mid_idx-1, k-1) # mid_idx-1 >= 1, k-1=2
                candidate = max(left_min_max_sum, right_min_max_sum)

                result = min(result, candidate)

                # right_min_max_sum is increasing, left_min_max_sum is decreasin
                if right_min_max_sum >= left_min_max_sum:
                    break

                # if right_min_max_sum >= result: # right_min_max_sum increasing => candidate increasing
                #     break

                mid_idx -= 1

            return result
                    

        return min_max_sum(0, n-1, k)