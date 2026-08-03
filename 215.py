from typing import List
import heapq

# Constraints:
# 1 <= k <= nums.length <= 105
# -104 <= nums[i] <= 104

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        ''' time complexity O(n log k). space complexity O(k) '''
        n = len(nums)

        # put the first k items into a min heap. k_item[0] is current k-th largest value
        k_items = nums[0:k]
        heapq.heapify(k_items)

        for i in range(k, n):            
            if nums[i] > k_items[0]: # k_items[0] is no longer k-th largest value anymore
                heapq.heapreplace(k_items, nums[i]) 

        return k_items[0]

if __name__ == '__main__':
    sol = Solution()

    nums = [3,2,1,5,6,4] 
    k = 2
    expected = 5        
    output = sol.findKthLargest(nums, k)

    print(f"nums={nums} k={k}")
    print(f"    expected={expected} output={output}")
    print(f"    {'PASS' if expected==output else 'FAIL'}\n\n")

    nums =[3,2,3,1,2,4,5,5,6] 
    k = 4
    expected = 4        
    output = sol.findKthLargest(nums, k)

    print(f"nums={nums} k={k}")
    print(f"    expected={expected} output={output}")
    print(f"    {'PASS' if expected==output else 'FAIL'}\n\n")


    nums = [3,2,1,5,6,4] 
    k = 1
    expected = 6        
    output = sol.findKthLargest(nums, k)

    nums = [3,2,1,5,6,4] 
    k = 6
    expected = 1        
    output = sol.findKthLargest(nums, k)