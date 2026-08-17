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


        dp = [[ {} for _ in range(n)]  for _ in range(k+1)] 

        k_idx = 1
        for hi_idx in range(n):
            state = dp[k_idx][hi_idx]
            state["result"] = prefix[hi_idx]
            # state["cross_idx"] = None
        
        k_idx += 1  # so k_idx >=2 now
        while k_idx <= k:
            for hi_idx in range(k_idx-1, n):
                state = dp[k_idx][hi_idx]

                if hi_idx == k_idx-1: # each sub array has 1 item, so nums[hi_idx] is the new sub array
                    state["result"] = max(dp[k_idx-1][hi_idx-1]["result"], nums[hi_idx])
                else:
                    if nums[hi_idx] >= dp[k_idx-1][hi_idx-1]["result"]: # nums[hi_idx] is big enough to be new sub array
                        state["result"] = nums[hi_idx]
                        state["cross_idx"] = hi_idx # cross_idx is the last index such that sum_of_subarray(cross_idx, hi_idx)>= dp[k_idx-1][cross_idx-1].result
                    else: # nums[hi_idx] is not big enough, need to the balanced cross idx
                        cross_idx = None
                        i = dp[k_idx][hi_idx-1].get("cross_idx", k_idx-1)
                        while i <= hi_idx and sum_of_subarray(i, hi_idx)>=dp[k_idx-1][i-1]["result"]:
                            cross_idx = i
                            i += 1
                        if cross_idx is None: # state[k_idx][hi_idx-1].result is very big
                            state["result"] = dp[k_idx][hi_idx-1]["result"]
                            # print(f'cross_idx is None.  dp[{k_idx}][{hi_idx-1}]["result"]={dp[k_idx][hi_idx-1]["result"]}')
                        else:
                            # print(f"cross_idx={cross_idx} dp[{k_idx-1}][{cross_idx}]={dp[k_idx-1][cross_idx]} sum_of_subarray({cross_idx}, {hi_idx})={sum_of_subarray(cross_idx, hi_idx)} ")
                            
                            state["result"] = min(dp[k_idx-1][cross_idx]["result"], sum_of_subarray(cross_idx, hi_idx))    
                            state["cross_idx"] = cross_idx

            k_idx += 1        

        if n < 20:
            for i in range(k+1):
                print("; ".join([ f"[{i}][{j}]:{dp[i][j]}"  for j in range(n)]))
                     

        return dp[k][n-1]["result"]