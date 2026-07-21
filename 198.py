from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:

        def explore(nums, start, memo):
            if len(nums)-start <= 0:
                amount = 0
            elif len(nums)-start == 1:
                amount = nums[start]
            elif len(nums)-start == 2:
                amount = max(nums[start], nums[start+1])
            else:
                amount = memo.get(start)
                if amount is None:
                    amount1 = nums[start] + explore(nums, start+2, memo)
                    amount2 = nums[start+1] + explore(nums, start+3, memo)


                    if amount1 >= amount2:
                        amount = amount1
                    else:
                        amount = amount2
            memo[start] = amount
            return amount

        return explore(nums, 0, {})

        
