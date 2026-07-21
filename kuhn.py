from re import DEBUG
from typing import List

DEBUG = True

class BipartiteMatcher:
    """
    Left vertices: 0 .. m-1
    Right vertices: 0 .. n-1

    Left side (workers):      Right side (jobs):

    L0                        R0
    L1                        R1
    L2                        R2
    ...

    adj[u] = list of right vertices that left vertex u can connect to
    """

    def __init__(self, adj: List[List[int]], num_right: int):
        self.adj = adj
        self.m = len(adj)
        self.n = num_right

        # match_right[v] = u that currently owns v
        # -1 means v is free
        self.match_right = [-1] * self.n

    def _dfs(self, u: int, visited: List[bool]) -> bool:
        """
        Try to find an augmenting path starting from left vertex u.
        """
        if DEBUG:
            print(f"    find an increasing path for W[{u}]")
            print(f"    match_right:")
            for i, val in enumerate(self.match_right):
                print(f"        W[{val}] -> J[{i}]")


        for v in self.adj[u]:
            if visited[v]:
                if DEBUG:
                    print(f"        J[{v}] was visted")
                continue

            visited[v] = True

            owner = self.match_right[v]

            # Case 1: v is free
            if owner == -1:
                if DEBUG:
                    print(f"        assign W[{u}] -> J[{v}] because J[{v}] is free")
                self.match_right[v] = u
                return True

            # Case 2: owner can be reassigned
            print(f"        try reassigning W[{owner}]")
            if self._dfs(owner, visited):
                if DEBUG:
                    if DEBUG:
                        i = None
                        for idx, val in enumerate(self.match_right):
                            if val == owner:
                                i = idx
                                break
                   
                        print(f"        assign W[{u}] -> J[{v}] because reassign W[{u}] -> J[{i}]")
                self.match_right[v] = u
                return True

        return False

    def maximum_matching(self) -> int:
        matching = 0

        for u in range(self.m):
            visited = [False] * self.n
            if DEBUG:
                print(f"start assigning W[{u}]")
            if self._dfs(u, visited):
                matching += 1

        return matching

    def get_pairs(self):
        """
        Returns list of (left, right) pairs.
        """
        pairs = []
        for v, u in enumerate(self.match_right):
            if u != -1:
                pairs.append((u, v))
        return pairs

if __name__ == "__main__":

    # Workers              Jobs

    # W0  --------->  J0
    #  |              ^
    #  └----------->  J1

    # W1  --------->  J0
    #  └----------->  J2

    # W2  --------->  J1
    #  ├----------->  J2
    #  └----------->  J3

    # W3  --------->  J2
    #  └----------->  J4

    # W4  --------->  J3    
    
    adj = [
        [0, 1],        # W0
        [0, 2],        # W1
        [1, 2, 3],     # W2
        [2, 4],        # W3
        [3],           # W4
    ]

    matcher = BipartiteMatcher(adj, num_right=5)

    size = matcher.maximum_matching()
    pairs = matcher.get_pairs()

    print(size)   # 3
    print(pairs)  # e.g. [(1, 0), (0, 1), (2, 2)]        