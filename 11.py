# You are given an integer array height of length n. There are n vertical lines drawn such that the two endpoints of the ith line are (i, 0) and (i, height[i]).
# Find two lines that together with the x-axis form a container, such that the container contains the most water.
# Return the maximum amount of water a container can store.
# Notice that you may not slant the container.

from typing import List

# naive implementation
class Solution:
    def maxArea(self, height: List[int]) -> int:
        maxAreaSoFar = 0

        leftPtr = 0

        while leftPtr < len(height)-1:
            left_height = height[leftPtr]
            rightPtr = leftPtr + 1
            # right_height = height[rightPtr]
            while rightPtr < len(height):
                right_height = height[rightPtr]
                maxAreaSoFar = max(maxAreaSoFar, (rightPtr-leftPtr) * min(left_height, right_height))
                rightPtr += 1
            leftPtr += 1 

        return maxAreaSoFar        