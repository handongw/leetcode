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

        # if n == k:
        #     sum = 0
        #     for v in nums:
        #         sum += v
        #     return sum

        # compute prefix array
        prefix = [0] * n
        sum = 0
        for i, v in enumerate(nums):
            sum += v
            prefix[i] = sum

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
            
            result = prefix[n-1]
            lo = k+lo_idx-1
            hi = hi_idx

            right_min_max_sum = sum_of_subarray(hi, hi_idx)
            left_min_max_sum = min_max_sum(lo_idx, hi-1, k-1) # mid_idx-1 >= 1, k-1=2
            if right_min_max_sum >= left_min_max_sum:
                result = right_min_max_sum # smallest right_min_max_sum >= largest left_min_max_sum
                return result
            else: # right_min_max_sum < left_min_max_sum
                right_min_max_sum = sum_of_subarray(lo, hi_idx)
                left_min_max_sum = min_max_sum(lo_idx, lo-1, k-1) 
                if right_min_max_sum <= left_min_max_sum:
                    result = left_min_max_sum # largest right_min_max_sum <= smallest left_min_max_sum
                    return result

                # right_min_max_sum and left_min_max_sum crossing
                target_mid = 0
                while lo <= hi:
                    mid = (lo + hi) // 2
                    right_min_max_sum = sum_of_subarray(mid, hi_idx)
                    left_min_max_sum = min_max_sum(lo_idx, mid-1, k-1) # mid_idx-1 >= 1, k-1=2
                    # candidate = max(left_min_max_sum, right_min_max_sum)
                    # result = min(result, candidate)

                    # find the largest  mid that right_min_max_sum >= left_min_max_sum
                    if right_min_max_sum < left_min_max_sum: 
                        hi = mid - 1
                    else:
                        lo = mid + 1
                        target_mid = max(target_mid, mid)

                right_min_max_sum = sum_of_subarray(target_mid, hi_idx)
                # left_min_max_sum = min_max_sum(lo_idx, target_mid-1, k-1) # mid_idx-1 >= 1, k-1=2
                candidate = right_min_max_sum
                result = min(result, candidate)

                # right_min_max_sum = sum_of_subarray(target_mid+1, hi_idx)
                left_min_max_sum = min_max_sum(lo_idx, target_mid-1+1, k-1) # mid_idx-1 >= 1, k-1=2
                candidate = left_min_max_sum
                result = min(result, candidate)

                return result


        return min_max_sum(0, n-1, k)