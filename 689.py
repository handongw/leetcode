from typing import List
DEBUG = False

class Solution:
    def maxSumOfThreeSubarrays(self, nums: List[int], k: int) -> List[int]:        
        n = len(nums) # k>=1, n >= 3k

        prefix_sum_array = [0] * (n + 1) # prefix_sum_array[size] = sum of first size numbers
        prefix_sum = 0
        for i in range(1, n+1):
            prefix_sum += nums[i-1]
            prefix_sum_array[i] = prefix_sum
            
        if DEBUG:
            print(f"prefix_sum_array={prefix_sum_array}")    
        
        # NOTE: dp uses more memory than it needs to make it easy to understand the code.
        # t = num of k-length sub arraries
        # nums_size = size of nums prefix sub array
        # dp[t][nums_size] = (max_sum, start_indices) where start_indices is an immutable
        # tuple of starting positions for each of the t subarrays of nums[0:nums_size]
        dp = [[(0, ()) for _ in range(n+1)] for _ in range(4)]

        # populate dp table
        for t in range(1, 4):
            if DEBUG:
                print(f"    t={t}")

            for nums_size in range(k*t, n+1):
                prev_sum, prev_indices = dp[t-1][nums_size-k]
                new_candidate = prev_sum + (prefix_sum_array[nums_size] - prefix_sum_array[nums_size-k])
                curr_sum, _ = dp[t][nums_size-1]
                if DEBUG:
                    print(f"       nums_size={nums_size} new_candidate={new_candidate} current max={curr_sum}")
                if new_candidate > curr_sum:
                    dp[t][nums_size] = (new_candidate, prev_indices + (nums_size-k,))
                else:
                    # immutable tuple state: share the previous object by reference
                    dp[t][nums_size] = dp[t][nums_size-1]
            if DEBUG:
                print(f"    t={t}")
                print(f"    dp={[(i, dp[t][i]) for i in range(n+1)]}\n")

        return list(dp[3][n][1])

# Constraints:

# 1 <= nums.length <= 2 * 104
# 1 <= nums[i] < 216
# 1 <= k <= floor(nums.length / 3)    