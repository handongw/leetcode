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
        # if root is None:
        #     return 

        stack = []
        if root:
            stack.append(root)
            
        head = tail = TreeNode()  # dummy head

        while stack:
            u = stack.pop()
            tail.right = u
            tail = u

            # we will clear u.left later on
            if u.right: # note: we push right node first so right node is traversed after left node
                stack.append(u.right)
            if u.left:
                stack.append(u.left)

        # clear node.left
        while head:
            head.left = None
            head = head.right
        