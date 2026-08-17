# 5:11 PM - 5:36 PM


# Constraints:

# nums.length == k
# 1 <= k <= 3500
# 1 <= nums[i].length <= 50
# -105 <= nums[i][j] <= 105
# nums[i] is sorted in non-decreasing order.



import heapq
from typing import List

class Solution:
    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        k = len(nums)
        if k == 1:
            return [nums[0][0], nums[0][0]]

        header_ptrs = [0] * k
        list_lens =[ len(l) for l in nums]

        min_headers = [ (nums[i][0], i)  for i in range(k)] # [val, list_idx]
        max_headers = [ (-nums[i][0], i)  for i in range(k)] # [-val, list_idx]

        heapq.heapify(min_headers)
        heapq.heapify(max_headers)

        max_head_val = -max_headers[0][0]
        max_head_list_idx = max_headers[0][1]
        
        ans = [min_headers[0][0], max_head_val]

        while True:
            interval_size = max_head_val - min_headers[0][0]
            if interval_size < (ans[1] - ans[0]):
                ans[0] = min_headers[0][0]
                ans[1] = max_head_val

            min_head = heapq.heappop(min_headers)   
            list_idx = min_head[1]
            header_ptrs[list_idx] += 1


            if header_ptrs[list_idx] < list_lens[list_idx]:
                new_val = nums[list_idx][header_ptrs[list_idx]]

                heapq.heappush(min_headers, (new_val, list_idx))
                if new_val > max_head_val and max_head_list_idx != list_idx:
                    max_head_val = new_val
                    max_head_list_idx = list_idx
            else:
                break    

        return ans
        