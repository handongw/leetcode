# Definition for a binary tree node.
from typing import List, Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def pathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        if root is None:
            return []

        result = []

        def dfs(node, prev_sum, prev_path):
            my_sum = prev_sum + node.val
            my_path = list(prev_path)
            my_path.append(node.val)

            if node.left is None and node.right is None:
                # leaf node
                if my_sum == targetSum:
                    # collect result
                    result.append(my_path)
            else:
                if node.left is not None:
                    dfs(node.left, my_sum, my_path)

                if node.right is not None:
                    dfs(node.right, my_sum, my_path)    

        dfs(root, 0, [])

        return result




def build_tree(vals: List[Optional[int]]) -> Optional[TreeNode]:
    """Build a binary tree from level-order list (None = missing child)."""
    if not vals or vals[0] is None:
        return None
    root = TreeNode(vals[0])
    queue = [root]
    i = 1
    while queue and i < len(vals):
        node = queue.pop(0)
        if i < len(vals) and vals[i] is not None:
            node.left = TreeNode(vals[i])
            queue.append(node.left)
        i += 1
        if i < len(vals) and vals[i] is not None:
            node.right = TreeNode(vals[i])
            queue.append(node.right)
        i += 1
    return root


if __name__ == '__main__':
    sol = Solution()

    tree = [5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1]
    root = build_tree( tree)
    targetSum = 22
    expected = [[5,4,11,2],[5,8,4,5]]

    print(f"tree={tree} target sum={targetSum}")
    output = sol.pathSum(root, targetSum)
    print(f"    expected={expected}")
    print(f"    output  ={output}")
    print(f"    {'PASS' if output==expected else 'FAIL'}\n\n")



    tree =[1,2,3]
    root = build_tree( tree)
    targetSum = 5
    expected = []

    print(f"tree={tree} target sum={targetSum}")
    output = sol.pathSum(root, targetSum)
    print(f"    expected={expected}")
    print(f"    output  ={output}")
    print(f"    {'PASS' if output==expected else 'FAIL'}\n\n")


