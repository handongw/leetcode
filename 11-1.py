# You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).
# Find two lines that together with the x-axis form a container, such that the container contains the most water.
# Return the maximum amount of water a container can store.
# Notice that you may not slant the container.

from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        maxAreaSoFar = 0

        leftPtr = 0
        rightPtr = len(height)-1
        
        while(leftPtr < rightPtr):
            left_height = height[leftPtr]
            right_height = height[rightPtr]

            # maxAreaSoFar = max(maxAreaSoFar, (rightPtr-leftPtr) * min(left_height, right_height))

            if left_height < right_height:
                maxAreaSoFar = max(maxAreaSoFar, (rightPtr-leftPtr) * left_height)
                leftPtr += 1     # we found the max area starting at leftPtr
            else:
                maxAreaSoFar = max(maxAreaSoFar, (rightPtr-leftPtr) * right_height)
                rightPtr -= 1    # we found the max area ending at rightPtr

        return maxAreaSoFar        
        