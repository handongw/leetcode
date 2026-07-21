from typing import List

DEBUG = False

class Solution:
    def criticalConnections(self, n: int, connections: List[List[int]]) -> List[List[int]]:
        adj_list = [[] for _ in range(n)]
        for u,v in connections:
            adj_list[u].append(v)
            adj_list[v].append(u)


        visited_node = [False for _ in range(n)] # used by undirected DFS
        disc = [0 for _ in range(n)] # redundant for debugging
        low = [n for _ in range(n)]
        visited_edge = set()  # prevent edge being visited twice

        def add_visited_edge(u, v):
            if u < v:
                visited_edge.add((u, v))
            else:
                visited_edge.add((v, u))
        def is_edge_visited(u, v):
            if u < v:
                return (u, v) in visited_edge
            else:
                return (v, u) in visited_edge                

        edge_stack = []
        critical_edges = []

        def dfs(u, parent, depth):
            if DEBUG:
                print(f"start dfs u={u} parent={parent}  depth={depth}")
            visited_node[u] = True
            disc[u] = depth
            low[u] = depth

            if DEBUG:
                print(f"    adj_list[{u}]={adj_list[u]}")
            for v in adj_list[u]:
                if v != u and not is_edge_visited(u, v):
                    add_visited_edge(u, v)     # visit (u, v) first time
                    edge_uv_idx = len(edge_stack) # it is used to pop biconnected edges
                    edge_stack.append([u, v])  

                    if visited_node[v]: # u->v is back edge
                        low[u] = min(low[u], disc[v])
                        if DEBUG:
                            print(f"        back edge {u}->{v} low[{u}] = min({low[u]}, {low[v]})")
                    else:
                        if DEBUG:
                            print(f"        tree edge {u}->{v}")
                        dfs(v, u, depth+1)  # continue with tree edge
                        low[u] = min(low[u], low[v])
                        if DEBUG:
                            print(f"        low[{u}] = min({low[u]}, {low[v]})")
                        
                        if DEBUG:
                            print(f"    compare disc[{u}] < low[{v}] = {disc[u]} < {low[v]}")
                        if disc[u] <= low[v]: # v sub stree completed at this time AND v sub tree does not above me
                            if DEBUG:
                                print(f"    disc[{u}]={disc[u]} < low[{v}]={low[v]}  edge_stack_len={edge_uv_idx} len({edge_stack})={len(edge_stack)}")

                            if disc[u] < low[v]: # u is not port of v sub tree
                                if DEBUG:
                                    print(f"        found critical edge: {edge_stack[edge_uv_idx]}")
                                critical_edges.append(edge_stack[edge_uv_idx])
                            
                            if DEBUG:
                                print(f"        pop edges: {edge_stack[edge_uv_idx:]}")
                            del edge_stack[edge_uv_idx:] # pop edges      

            if DEBUG:
                print(f"end dfs u={u} parent={parent} depth={depth} low[{u}]={low[u]}")

        for v in range(n):
            if not visited_node[v]:
                dfs(v, None, 0)
                if len(edge_stack) == 1:
                    if DEBUG:
                        print(f"    found critical edge: {edge_stack[-1]}")
                    critical_edges.append(edge_stack.pop())
                elif len(edge_stack)>1:
                    if DEBUG:
                        print(f"    pop bin connected edges: {edge_stack}")
                    
                    edge_stack.clear()    
                    # raise Exception(f"dfs({v}) len(edge_stack)={len(edge_stack)}")

        if DEBUG:
            print(f"    disc={disc} low={low} visited={visited_node}")
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
