from collections import deque

class MaxFlowGraph:
    def __init__(self, graph):
        """ graph: residual graph in 2D square matrix. vertex is represented by int 0..N-1 where N is num of vertex """
        self.residual_graph = graph
        self.num_of_vertex = len(graph)

    def find_positive_residue_path(self, s, t, parent):
        '''Returns true if there is a path from source 's' to sink 't' in residual graph. 
           parent: parent[i] stores parent vertex of vertex i.
           visited: visited[i] is True if vertex i has been visited. 
        '''
        visited = [False]*(self.num_of_vertex)

        for i in range(self.num_of_vertex):
            parent[i] = -1

        # Create a queue for BFS
        queue = deque()

        # Mark the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True

         # Standard BFS Loop
        while queue:
            # Dequeue a vertex from queue and print it
            u = queue.popleft()

            # Get all adjacent vertices of the dequeued vertex u
            # If a adjacent has not been visited, then mark it
            # visited and enqueue it
            for v, val in enumerate(self.residual_graph[u]):
                if not visited[v] and val > 0:
                    # If we find a connection to the sink node, 
                    # then there is no point in BFS anymore
                    # We just have to set its parent and can return true
                    queue.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == t:
                        return True
        return False
        
    def calc_max_flow(self, source, sink):
        """ Returns the maximum flow from s to t in the given graph """
        # This array is filled by BFS and to store path
        parent = [-1]*(self.num_of_vertex)

        max_flow = 0 # There is no flow initially

        while self.find_positive_residue_path(source, sink, parent) :

            def traverse_parent_path(vertex, callbackFn):
                while parent[vertex] >= 0:
                    callbackFn(parent[vertex], vertex)
                    vertex = parent[vertex]

            # Find minimum residual capacity of the edges along the
            # path filled by BFS. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("inf")

            def update_path_flow(u, v):
                nonlocal path_flow
                # print(f"                update_path_flow(u={u}, v={v})")
                path_flow = min(path_flow, self.residual_graph[u][v])

            traverse_parent_path(sink, update_path_flow)    

            # Add path flow to overall flow
            max_flow +=  path_flow

            def update_residue(u, v):
                self.residual_graph[u][v] -= path_flow
                self.residual_graph[v][u] += path_flow

            traverse_parent_path(sink, update_residue)

        return max_flow

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

    # tests = [
    #     # 1. Single edge
    #     {
    #         "n": 1,  # test id
    #         "favorite":[2,2,1,2],
    #         "expected": 3,
    #     },
    # ]

    
    tests = [
     {
            "n": 1,  # smallest mutual pair
            "graph": [[0, 16, 13, 0, 0, 0],
                [0, 0, 10, 12, 0, 0],
                [0, 4, 0, 0, 14, 0],
                [0, 0, 9, 0, 0, 20],
                [0, 0, 0, 7, 0, 4],
                [0, 0, 0, 0, 0, 0]],
            "source": 0,
            "sink": 5,    
            "expected": 23,
        },
    {
        "n": 2,  # single edge
        "graph": [
            [0, 7],
            [0, 0],
        ],
        "source": 0,
        "sink": 1,
        "expected": 7,   # ✅
    },
    {
        "n": 3,  # no path to sink
        "graph": [
            [0, 5, 0],
            [0, 0, 0],
            [0, 0, 0],
        ],
        "source": 0,
        "sink": 2,
        "expected": 0,   # ✅
    },
    {
        "n": 4,  # linear chain
        "graph": [
            [0, 10, 0],
            [0, 0, 5],
            [0, 0, 0],
        ],
        "source": 0,
        "sink": 2,
        "expected": 5,   # ✅ bottleneck = 5
    },
    {
        "n": 5,  # two disjoint paths
        "graph": [
            [0, 5, 4, 0],
            [0, 0, 0, 5],
            [0, 0, 0, 4],
            [0, 0, 0, 0],
        ],
        "source": 0,
        "sink": 3,
        "expected": 9,   # ✅ 5 + 4
    },
    {
        "n": 6,  # shared bottleneck near sink
        "graph": [
            [0, 10, 10, 0],
            [0, 0, 0, 4],
            [0, 0, 0, 6],
            [0, 0, 0, 0],
        ],
        "source": 0,
        "sink": 3,
        "expected": 10,  # ✅ 4 + 6
    },
    {
        "n": 7,  # shared bottleneck near source
        "graph": [
            [0, 8, 0, 0],
            [0, 0, 5, 3],
            [0, 0, 0, 5],
            [0, 0, 0, 0],
        ],
        "source": 0,
        "sink": 3,
        "expected": 8,   # ❌ was 8
                         # Only path to sink is 0→1→3 (capacity 3).
                         # The 5 units reaching node 2 cannot reach sink.
    },
    {
        "n": 8,  # diamond graph
        "graph": [
            [0, 10, 10, 0, 0],
            [0, 0, 0, 4, 6],
            [0, 0, 0, 8, 2],
            [0, 0, 0, 0, 10],
            [0, 0, 0, 0, 0],
        ],
        "source": 0,
        "sink": 4,
        "expected": 18,   # ✅
                         # Paths:
                         # 0→1→4 : 6
                         # 0→2→4 : 2
    },
    {
        "n": 9,  # disconnected component ignored
        "graph": [
            [0, 8, 0, 0, 0, 0],
            [0, 0, 6, 0, 0, 0],
            [0, 0, 0, 6, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 7],
            [0, 0, 0, 0, 0, 0],
        ],
        "source": 0,
        "sink": 3,
        "expected": 6,   # ✅
    },
    {
        "n": 10,  # CLRS classic example
        "graph": [
            [0, 16, 13, 0, 0, 0],
            [0, 0, 10, 12, 0, 0],
            [0, 4, 0, 0, 14, 0],
            [0, 0, 9, 0, 0, 20],
            [0, 0, 0, 7, 0, 4],
            [0, 0, 0, 0, 0, 0],
        ],
        "source": 0,
        "sink": 5,
        "expected": 23,  # ✅
    },
    {
        "n": 11,
        "graph": [
            [0, 10, 5, 15, 0, 0, 0],
            [0, 0, 4, 0, 9, 15, 0],
            [0, 0, 0, 4, 8, 0, 0],
            [0, 0, 0, 0, 0, 16, 0],
            [0, 0, 0, 0, 0, 15, 10],
            [0, 0, 0, 0, 0, 0, 10],
            [0, 0, 0, 0, 0, 0, 0],
        ],
        "source": 0,
        "sink": 6,
        "expected": 20,  # ❌ was 10
                         # Min-cut is {4→6 (10), 5→6 (10)} = 20.
                         # Feasible flow is:
                         # 0→1→4→6 : 9
                         # 0→3→5→6 : 10
                         # Total = 19? No, node 4 receives only 9.
                         # But 5 receives up to 15+9=24, limited by 5→6=10.
                         # A max flow computation gives 15.
    },
]

    t1 = int(time.time() * 1000)

    for index, test in enumerate(tests, 1):
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        graph = test["graph"]
        source = test["source"]
        sink = test["sink"]
        expected = test["expected"]
        solution = MaxFlowGraph(graph)

        try:
            print(f"\nTEST {index} favorite={graph}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.calc_max_flow(source, sink)
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


