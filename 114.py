# Definition for a binary tree node.
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
        
class Solution:
    def flatten(self, root: Optional[TreeNode]) -> None:
        """
        Do not return anything, modify root in-place instead.
        """
        

        def dfs(parent):
            phead = ptail = parent
            # preserve left and right first
            left = parent.left
            right = parent.right

            # reset parent.left, parenet right
            parent.left = None
            parent.right = None

            if left:
                lhead, ltail = dfs(left)
                ptail.right = lhead
                ptail = ltail
            parent.left = None

            if right:
                rhead, rtail = dfs(right)
                ptail.right = rhead
                ptail = rtail

            return (phead, ptail)

        if root is None:
            return
        dfs(root)        
        