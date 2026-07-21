from typing import List

class Solution:
    def canJump(self, nums: List[int]) -> bool:
        print(f"\n\n")
        maxSteps = 0;
        for i in range(len(nums)-1):
            maxSteps = max(maxSteps, nums[i])

        return self.jumpBackward(nums, maxSteps, len(nums)-1, {})

    def jumpBackward(self, nums, maxSteps, destIdx, canReachMap):
        '''Jump backward until we reach start point'''

        # print(f"   destIdx={destIdx} maxSteps={maxSteps} canReachMap={canReachMap}")
        if destIdx == 0:
            return True  # back to the start point
        else:
            prevIdx = destIdx-maxSteps
            if prevIdx < 0:
                prevIdx = 0

            while prevIdx < destIdx:
                flag = canReachMap.get(prevIdx)
                if flag is False:
                    prevIdx += 1
                    continue


                # can we reach destIdx from prevIdx?
                maxJumps = nums[prevIdx]
                if maxJumps >= destIdx - prevIdx:

                    if self.jumpBackward(nums, maxSteps, prevIdx, canReachMap):
                        return True
                
                    
                prevIdx += 1  

            canReachMap[destIdx] = False # can not reach start point from destIdx
            return False          

if __name__ == "__main__":
    solver = Solution()

    test_cases = [
        
        {
            "nums": [2,3,1,1,4],
            "expected": True,
        },
        {
            "nums": [3,2,1,0,4],
            "expected": False,
        },
        {
            "nums": [2,0,6,9,8,4,5,0,8,9,1,2,9,6,8,8,0,6,3,1,2,2,1,2,6,5,3,1,2,2,6,4,2,4,3,0,0,0,3,8,2,4,0,1,2,0,
                     1,4,6,5,8,0,7,9,3,4,6,6,5,8,9,3,4,3,7,0,4,9,0,9,8,4,3,0,7,7,1,9,1,9,4,9,0,1,9,5,7,7,1,5,8,2,
                     8,2,6,8,2,2,7,5,1,7,9,6],
            "expected": False,
        },
        {
            "nums": [1,2],
            "expected": True,
        },
        {
            "nums": [1,2, 3],
            "expected": True,
        },
    ]

    for idx, case in enumerate(test_cases, start=1):
        nums = case["nums"]
        expected = case["expected"]
        try:
            actual = solver.canJump(nums)
            print(f"Case {idx}:")
            print(f"  nums={nums}")
            print(f"  expected={expected}")
            print(f"  actual  ={actual}")
            print(f"  pass    ={actual == expected}")
            print("\n")
        except Exception as exc:
            print(f"Case {idx} raised an exception: {exc}")        