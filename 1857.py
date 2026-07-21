# There is a directed graph of n colored nodes and m edges. The nodes are numbered from 0 to n - 1.

# You are given a string colors where colors[i] is a lowercase English letter representing the color of the ith node in this graph (0-indexed). You are also given a 2D array edges where edges[j] = [aj, bj] indicates that there is a directed edge from node aj to node bj.

# A valid path in the graph is a sequence of nodes x1 -> x2 -> x3 -> ... -> xk such that there is a directed edge from xi to xi+1 for every 1 <= i < k. The color value of the path is the number of nodes that are colored the most frequently occurring color along that path.

# Return the largest color value of any valid path in the given graph, or -1 if the graph contains a cycle.

from typing import List

DEBUG = False

class Solution:
    def largestPathValue(self, colors: str, edges: List[List[int]]) -> int:
        n = len(colors)
        if n <= 0:
            return 0

        adj_list = [[] for _ in range(n)]
        for e in edges:
            adj_list[e[0]].append(e[1])


        def topo_order():
            visited = [0] * n
            topo = []

            def dfs(u):
                visited[u] = 1

                for v in adj_list[u]:
                    if visited[v] == 0:
                        if not dfs(v):
                            print(f"    Found Loop!")
                            return False
                    elif visited[v] == 1:
                        return False    

                visited[u] = 2
                topo.append(u)
                return True

            for v in range(n):
                if visited[v] == 0:
                    if not dfs(v):
                        print(f"    dfs returns false - Found Loop!")
                        return None
            return topo 

        topo_array = topo_order() 
        if not topo_array:
            return -1

        color_set = set(colors)

        if DEBUG:
            print(f"topo_array={topo_array}")
            print(f"color_set={color_set}")

        def node_weight(v, c):
            if colors[v] == c:
                return 1
            else:
                return 0

        def longest_path(c, stack):
            if DEBUG:
                print(f"    longest_path color={c} stack={stack}")
            dp = [-1] * n

            start = stack[-1]
            dp[start] = node_weight(start, c)

            while stack:
                u = stack.pop()
                if dp[u] >= 0:
                    for v in adj_list[u]:
                        dp[v] = max(dp[v], dp[u]+node_weight(v, c))

            print(f"    dp={dp}")
            return max(dp)

        ans = -1
        for c in color_set:
            ans = max(ans, longest_path(c, topo_array))

        return ans

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
    #         "n": 1,
    #         "colors": "abaca",
    #         "edges": [[0,1],[0,2],[2,3],[3,4]],
    #         "expected": 3,
    #     },
    #     {
    #         "n": 1,
    #         "colors": "a",
    #         "edges": [[0,0]],
    #         "expected": -1,
    #     },
        
    # ]

    tests = [
        {
            "n": 1,
            "colors": "a",
            "edges": [],
            "expected": 1,
        },
        {
            "n": 2,
            "colors": "aa",
            "edges": [[0, 1]],
            "expected": 2,
        },
        {
            "n": 3,
            "colors": "ab",
            "edges": [[0, 1]],
            "expected": 1,
        },
        {
            "n": 4,
            "colors": "aaaaa",
            "edges": [[0, 1], [1, 2], [2, 3], [3, 4]],
            "expected": 5,
        },
        {
            "n": 5,
            "colors": "abcde",
            "edges": [[0, 1], [1, 2], [2, 3], [3, 4]],
            "expected": 1,
        },
        {
            "n": 6,
            "colors": "abaca",
            "edges": [[0, 1], [1, 2], [2, 3], [3, 4]],
            "expected": 3,
        },
        {
            "n": 7,
            "colors": "aaaa",
            "edges": [[0, 1], [0, 2], [1, 3], [2, 3]],
            "expected": 3,
        },
        {
            "n": 8,
            "colors": "abaa",
            "edges": [[0, 1], [0, 2], [1, 3], [2, 3]],
            "expected": 3,
        },
        {
            "n": 9,
            "colors": "aabaa",
            "edges": [[0, 2], [1, 2], [2, 3], [2, 4]],
            "expected": 2,
        },
        {
            "n": 10,
            "colors": "aaabbb",
            "edges": [[0, 1], [1, 2], [3, 4], [4, 5]],
            "expected": 3,
        },
        {
            "n": 11,
            "colors": "abcde",
            "edges": [],
            "expected": 1,
        },
        {
            "n": 12,
            "colors": "aaaaa",
            "edges": [[0, 1], [0, 2], [0, 3], [0, 4]],
            "expected": 2,
        },
        {
            "n": 13,
            "colors": "aaaaa",
            "edges": [[1, 0], [2, 0], [3, 0], [4, 0]],
            "expected": 2,
        },
        {
            "n": 14,
            "colors": "aaabaaa",
            "edges": [[0, 1], [1, 2], [2, 3], [3, 4], [0, 5], [5, 6]],
            "expected": 4,
        },
        {
            "n": 15,
            "colors": "aa",
            "edges": [[0, 1], [1, 0]],
            "expected": -1,
        },
        {
            "n": 16,
            "colors": "abc",
            "edges": [[0, 1], [1, 2], [2, 0]],
            "expected": -1,
        },
        {
            "n": 17,
            "colors": "a",
            "edges": [[0, 0]],
            "expected": -1,
        },
        {
            "n": 18,
            "colors": "aaaaaa",
            "edges": [[0, 1], [1, 2], [2, 0], [3, 4], [4, 5]],
            "expected": -1,
        },
        {
            "n": 19,
            "colors": "aaaaaaa",
            "edges": [
                [0, 1], [0, 2],
                [1, 3], [2, 3],
                [3, 4], [3, 5],
                [4, 6], [5, 6],
            ],
            "expected": 5,
        },
        {
            "n": 20,
            "colors": "abaaaa",
            "edges": [
                [0, 1],
                [1, 2],
                [2, 3],
                [0, 4],
                [4, 5],
            ],
            "expected": 3,
        },
        {
            "n": 21,
            "colors": "abbbbaa",
            "edges": [
                [0, 1], [1, 2], [2, 3], [3, 4],
                [0, 5], [5, 6],
            ],
            "expected": 4,
        },
        {
            "n": 22,
            "colors": "abaca",
            "edges": [[0, 1], [0, 2], [2, 3], [2, 4]],
            "expected": 3,
        },
        {
            "n": 23,
            "colors": "aaaba",
            "edges": [[0, 1], [1, 2], [1, 3], [1, 4]],
            "expected": 3,
        },
        {
            "n": 24,
            "colors": "aabbcc",
            "edges": [[0, 2], [1, 2], [2, 4], [2, 5]],
            "expected": 1,
        },
        {
            "n": 25,
            "colors": "aaabaa",
            "edges": [[0, 1], [1, 2], [2, 4], [0, 3], [3, 5]],
            "expected": 4,
        },
        {
            "n": 26,
            "colors": "aaaa",
            "edges": [[0,1],[1,2],[3,0]],
            "expected": 4,

        },
        {
            "n": 27,
            "colors": "aaaaaaaa",
            "edges": [[0,2],[0,6],[2,4],[4,6],[6,7],[1,3],[1,5],[3,5]],
            "expected": 5,
        }
    ]    

    solution = Solution()

    t1 = int(time.time() * 1000)

    for index, test in enumerate(tests, 1):
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        edges = test["edges"]
        colors = test["colors"]
        expected = test["expected"]

        try:
            print(f"\nTEST {index} colors={colors} edges={edges[:20]}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.largestPathValue(colors, edges)
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
