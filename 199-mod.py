# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
from typing import List, Optional
from collections import deque

# Bonus twist: You can see through thin layers. 
# You are standing on the right side, but you can see a node even if it's blocked, 
# as long as it is blocked by fewer than 2 nodes in front of it on that exact same level.



class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if root is None:
            return []

        result: [deque] = []

        def setResult(val, depth):
            if depth < len(result):
                result[depth].append(val)
                if len(result[depth]) > 2:
                    result[depth].popleft()
            elif depth == len(result):
                result.append(deque([val]))
            else:
                raise Exception(f"setResult failed:depth={depth} result.size={len(result)}")        

        def dfs(node:TreeNode, depth:int):
            setResult(node.val, depth)
            if node.left is not None:
                dfs(node.left, depth+1)
            if node.right is not None:
                dfs(node.right, depth+1)

        dfs(root, 0)
        return [val for q in result for val in q]

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
    import sys
    import time

    DEBUG = False
    selected_tests = None  # None: run all; else set of 1-based indices from argv

    for a in sys.argv[1:]:
        if a == "-d":
            DEBUG = True
        elif a.replace(",", "").isdigit() and "," in a:
            if selected_tests is None:
                selected_tests = set()
            for part in a.split(","):
                part = part.strip()
                if part.isdigit():
                    selected_tests.add(int(part))
        elif a.isdigit():
            if selected_tests is None:
                selected_tests = set()
            selected_tests.add(int(a))
        else:
            print(
                f"Unknown argument: {a!r} (use -d and/or 1-based test indices, e.g. 1 2 4)",
                file=sys.stderr,
            )
            sys.exit(2)

    if selected_tests is not None and len(selected_tests) == 0:
        print("Test selection is empty.", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"selected_tests={selected_tests}")

    # Twist: at each level, up to 2 rightmost nodes are visible
    # (blocked by fewer than 2 nodes on the same level).
    tests = [
        {"n": 1, "vals": [1, 2, 3, None, 5, None, 4], "expected": [1, 2, 3, 5, 4]},
        {"n": 2, "vals": [1, 2, 3, 4, None, None, None, 5], "expected": [1, 2, 3, 4, 5]},
        {"n": 3, "vals": [1, None, 3], "expected": [1, 3]},
        {"n": 4, "vals": [], "expected": []},
        {"n": 5, "vals": [1], "expected": [1]},
        {"n": 6, "vals": [1, 2], "expected": [1, 2]},
        {"n": 7, "vals": [1, 2, None, 4], "expected": [1, 2, 4]},  # left deeper than right
        {"n": 8, "vals": [1, 2, 3, 4, 5, 6, 7], "expected": [1, 2, 3, 6, 7]},  # level has 4 nodes -> keep 6,7
        {"n": 9, "vals": [1, None, 2, None, 3], "expected": [1, 2, 3]},  # right-skewed
        {"n": 10, "vals": [1, 2, 3, None, None, 4, 5], "expected": [1, 2, 3, 4, 5]},
        {"n": 11, "vals": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
         "expected": [1, 2, 3, 6, 7, 14, 15]},  # full tree: 2 rightmost per level
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        vals = test["vals"]
        expected = test["expected"]
        root = build_tree(vals)

        try:
            print(f"\nTEST {test['n']} vals={vals}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.rightSideView(root)
            if result != expected:
                print(f"test {test['n']} FAIL")
                print(f"  got:      {result}")
                print(f"  expected: {expected}")
            else:
                print(f"test {test['n']} OK: (result={result})")
        except Exception as e:
            print(f"test {test['n']} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")

