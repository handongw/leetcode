from typing import List

DEBUG = False

# disc[u]:
#   DFS depth when u is first discovered.

# low[u]:
#   After dfs(u) finishes, the smallest disc[]
#   reachable from u's subtree without using u's
#   parent edge.

# Bridge condition:
#   disc[u] < low[v]
#   => v's subtree cannot reach u or above
#   => (u, v) is the only gateway

class Solution:
    def criticalConnections(self, n: int, connections: list[list[int]]) -> list[list[int]]:
        # 1. Build the adjacency list
        adj_list = [[] for _ in range(n)]
        for u, v in connections:
            adj_list[u].append(v)
            adj_list[v].append(u)

        # 2. Initialize tracking arrays
        # disc tracks the discovery time of each node
        # low tracks the lowest discovery time reachable from the node
        disc = [-1] * n 
        low = [-1] * n
        
        timer = 0
        critical_edges = []

        def dfs(u, parent):
            nonlocal timer
            disc[u] = low[u] = timer
            timer += 1

            for v in adj_list[u]:
                if v == parent:
                    continue  # Don't go back the way we came
                
                if disc[v] == -1:
                    # Tree edge: v hasn't been visited yet
                    dfs(v, u)
                    
                    # Update low[u] after returning from v
                    low[u] = min(low[u], low[v])
                    
                    # Bridge condition: If the lowest reachable node from v 
                    # is discovered strictly after u, then u-v is a bridge.
                    if low[v] > disc[u]:
                        critical_edges.append([u, v])
                else:
                    # Back edge: v is already visited, update low[u]
                    low[u] = min(low[u], disc[v])

        # 3. Start DFS from node 0 (the problem guarantees a connected graph)
        dfs(0, -1)

        return critical_edges

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

    tests = [
        # 1. Single edge
        {
            "n": 1,
            "vertex_cnt": 2,
            "connections": [[0, 1]],
            "expected": [[0, 1]],
        },

        # 2. Simple triangle (no bridges)
        {
            "n": 2,
            "vertex_cnt": 3,
            "connections": [[0, 1], [1, 2], [2, 0]],
            "expected": [],
        },

        # 3. Triangle + tail
        {
            "n": 3,
            "vertex_cnt": 4,
            "connections": [[0, 1], [1, 2], [2, 0], [1, 3]],
            "expected": [[1, 3]],
        },

        # 4. Straight chain
        {
            "n": 4,
            "vertex_cnt": 4,
            "connections": [[0, 1], [1, 2], [2, 3]],
            "expected": [[0, 1], [1, 2], [2, 3]],
        },

        # 5. Star
        {
            "n": 5,
            "vertex_cnt": 5,
            "connections": [[0, 1], [0, 2], [0, 3], [0, 4]],
            "expected": [[0, 1], [0, 2], [0, 3], [0, 4]],
        },

        # 6. Square (single cycle)
        {
            "n": 6,
            "vertex_cnt": 4,
            "connections": [[0, 1], [1, 2], [2, 3], [3, 0]],
            "expected": [],
        },

        # 7. Square + tail
        {
            "n": 7,
            "vertex_cnt": 5,
            "connections": [[0, 1], [1, 2], [2, 3], [3, 0], [2, 4]],
            "expected": [[2, 4]],
        },

        # 8. Two cycles connected by one bridge
        {
            "n": 8,
            "vertex_cnt": 6,
            "connections": [
                [0, 1], [1, 2], [2, 0],
                [2, 3],
                [3, 4], [4, 5], [5, 3]
            ],
            "expected": [[2, 3]],
        },

        # 9. Figure-8 (two cycles sharing one vertex)
        {
            "n": 9,
            "vertex_cnt": 5,
            "connections": [
                [0, 1], [1, 2], [2, 0],
                [2, 3], [3, 4], [4, 2]
            ],
            "expected": [],
        },

        # 10. Figure-8 + tail
        {
            "n": 10,
            "vertex_cnt": 6,
            "connections": [
                [0, 1], [1, 2], [2, 0],
                [2, 3], [3, 4], [4, 2],
                [4, 5]
            ],
            "expected": [[4, 5]],
        },

        # 11. Cycle with a chain hanging off
        {
            "n": 11,
            "vertex_cnt": 6,
            "connections": [
                [0, 1], [1, 2], [2, 0],
                [2, 3], [3, 4], [4, 5]
            ],
            "expected": [[2, 3], [3, 4], [4, 5]],
        },

        # 12. Complete graph K4
        {
            "n": 12,
            "vertex_cnt": 4,
            "connections": [
                [0, 1], [0, 2], [0, 3],
                [1, 2], [1, 3], [2, 3]
            ],
            "expected": [],
        },

        # 13. Chain of overlapping triangles (no bridges)
        {
            "n": 13,
            "vertex_cnt": 7,
            "connections": [
                [0, 1], [1, 2], [2, 0],
                [2, 3], [3, 4], [4, 2],
                [4, 5], [5, 6], [6, 4]
            ],
            "expected": [],
        },

        # 14. Cycles connected by single bridges
        {
            "n": 14,
            "vertex_cnt": 9,
            "connections": [
                [0, 1], [1, 2], [2, 0],
                [2, 3],
                [3, 4], [4, 5], [5, 3],
                [5, 6],
                [6, 7], [7, 8], [8, 6]
            ],
            "expected": [[2, 3], [5, 6]],
        },

        # 15. Your "loop of loops" (outer cycle exists)
        {
            "n": 15,
            "vertex_cnt": 8,
            "connections": [
                [0, 1], [1, 2], [2, 0],
                [2, 3], [3, 4], [4, 2],
                [4, 5], [5, 6], [6, 4],
                [6, 7], [7, 1], [1, 6]
            ],
            "expected": [],
        },

        # 16. Root with multiple cyclic children
        {
            "n": 16,
            "vertex_cnt": 7,
            "connections": [
                [0, 1],
                [1, 2], [2, 3], [3, 1],
                [0, 4],
                [4, 5], [5, 6], [6, 4]
            ],
            "expected": [[0, 1], [0, 4]],
        },

        # 17. Deep bridge
        {
            "n": 17,
            "vertex_cnt": 6,
            "connections": [
                [0, 1], [1, 2], [2, 0],
                [1, 3],
                [3, 4], [4, 5], [5, 3]
            ],
            "expected": [[1, 3]],
        },

        # 18. Lollipop graph
        {
            "n": 18,
            "vertex_cnt": 7,
            "connections": [
                [0, 1], [1, 2], [2, 3], [3, 0],
                [3, 4], [4, 5], [5, 6]
            ],
            "expected": [[3, 4], [4, 5], [5, 6]],
        },
        {
            "n": 19,
            "vertex_cnt": 6,
            "connections": [
                [0,1],
                [1,2],
                [2,3],
                [3,1],
                [3,4],
                [4,5],
                [5,3],
            ],
            "expected": [[0,1]],
        }
    ]
    solution = Solution()

    t1 = int(time.time() * 1000)

    for index, test in enumerate(tests, 1):
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        connections = test["connections"]
        vertex_cnt = test["vertex_cnt"]
        expected = test["expected"]

        try:
            print(f"\nTEST {index}\nvertex_cnt={vertex_cnt} connections={connections[:20]}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.criticalConnections(vertex_cnt, connections)
            result.sort()
            if result != expected:
                print(f"test {index} FAIL: n={test['n']}")
                print(f"  got:      {result}")
                print(f"  expected: {expected}")
            else:
                print(f"test {index} OK: n={test['n']} (result={result})")
        except Exception as e:
            print(f"test {index} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")
