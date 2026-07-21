
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
        if not isinstance(val, int):
            raise Exception(f"val is not int: {val}")
        else:
            print(f" new Node {val}")    

# def check_val_type_is_int(node: 'Node') -> bool:
#     """
#     Checks if the `val` attribute of the given `Node` is of type int.
#     """
#     return isinstance(node.val, int)

from typing import Any, Optional

'''
Given a reference of a node in a connected undirected graph.
Return a deep copy (clone) of the graph.
'''

from collections import deque
from typing import Optional

class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if not node:
            return None

        # Decoupled state tracking
        visited = set()
        clones = {}
        
        queue = deque([node])
        visited.add(node)
        clones[node] = Node(node.val)

        while queue:
            current = queue.popleft()
            
            for neighbor in current.neighbors:
                # 1. Traversal Logic
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    
                # 2. Cloning Logic
                if neighbor not in clones:
                    clones[neighbor] = Node(neighbor.val)
                
                clones[current].neighbors.append(clones[neighbor])

        return clones[node]

        def cloneNode(n):
            if n is None:
                return None

            n2 = Node(n.val)
            cloneNodeMap[n.val] = n2

            n2.neighbors = []
            for c in n.neighbors:
                c2 = cloneNodeMap.get(c.val)
                if c2 is None:
                    c2 = cloneNode(c)                    
                n2.neighbors.append(c2)
                cloneNodeMap[c.val] = c2

            return n2

        return cloneNode(node)

from collections import deque

def serialize(node):
    if not node:
        return {}

    visited = set()
    q = deque([node])
    result = {}

    while q:
        cur = q.popleft()
        if cur in visited:
            continue
        visited.add(cur)

        result[cur.val] = sorted([n.val for n in cur.neighbors])

        for nei in cur.neighbors:
            if nei not in visited:
                q.append(nei)

    return result

if __name__ == "__main__":
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)

    n1.neighbors = [n2, n4]
    n2.neighbors = [n1, n3]
    n3.neighbors = [n2, n4]
    n4.neighbors = [n1, n3]

    solution = Solution()
    print(serialize(solution.cloneGraph(n1)))
