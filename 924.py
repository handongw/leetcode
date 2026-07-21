from collections import deque
from typing import List

DEBUG = False

class Solution:
    def minMalwareSpread(self, graph: List[List[int]], initial: List[int]) -> int:
        n = len(graph)
        malware_set = set(initial)
        visited = [False for _ in range(n)]

        def scc(start_node, memo):
            def update_memo(v):
                memo['cc_size'] = memo['cc_size'] + 1
                if v in malware_set:
                    memo['malware_cnt'] = memo['malware_cnt'] + 1
                    memo["smallest_malware"] = min(memo["smallest_malware"], v)
            if DEBUG:
                print(f"    scc(start={start_node}) init memo={memo}")

            q = deque() 
            q.append(start_node)
            visited[start_node] = True
            update_memo(start_node)

            while q:
                u = q.popleft()
                for v in range(n):
                    if v != u and not visited[v] and graph[u][v] == 1:
                        visited[v] = True
                        q.append(v)
                        update_memo(v)

            score = (0 if memo['malware_cnt']>1 else memo['cc_size'], memo['smallest_malware'])            
            if DEBUG:
                print(f"    scc(start={start_node}) return memo={memo} score={score}")
            return score


        candidate = (-1, -n)
        for malware in initial:
            if not visited[malware]:
                saved_nodes, malwareIdx = scc(malware, {"malware_cnt":0, "smallest_malware":float('inf'), "cc_size":0})
                candidate = max(candidate, (saved_nodes, -malwareIdx))

        return -candidate[1]

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
        {"n": 1, "graph": [[1,1,0],[1,1,0],[0,0,1]], "initial":[0,1], "expected": 0},
        {"n": 2, "graph": [[1,0,0],[0,1,0],[0,0,1]], "initial":[0,2], "expected": 0},
        {"n": 3, "graph": [[1,1,1],[1,1,1],[1,1,1]], "initial":[1,2], "expected": 1},
        # 1. One large CC with exactly one malware.
        # Removing it saves everyone.
        {
            "n": 4,
            "graph": [
                [1,1,1,1],
                [1,1,1,1],
                [1,1,1,1],
                [1,1,1,1],
            ],
            "initial": [2],
            "expected": 2,
        },

        # 2. Two isolated malware, different CC sizes.
        # Larger saved component should win.
        {
            "n": 5,
            "graph": [
                [1,1,1,0,0],
                [1,1,1,0,0],
                [1,1,1,0,0],
                [0,0,0,1,1],
                [0,0,0,1,1],
            ],
            "initial": [0,3],
            "expected": 0,
        },

        # 3. Same saved size, tie by malware index.
        {
            "n": 6,
            "graph": [
                [1,1,0,0],
                [1,1,0,0],
                [0,0,1,1],
                [0,0,1,1],
            ],
            "initial": [0,2],
            "expected": 0,
        },

        # 4. Multi-malware CC vs unique-malware CC.
        # Multi-malware CC saves 0.
        {
            "n": 7,
            "graph": [
                [1,1,1,0,0],
                [1,1,1,0,0],
                [1,1,1,0,0],
                [0,0,0,1,1],
                [0,0,0,1,1],
            ],
            "initial": [0,2,3],
            "expected": 3,
        },

        # 5. Every CC has >=2 malware.
        # Everyone saves 0 -> smallest index.
        {
            "n": 8,
            "graph": [
                [1,1,0,0],
                [1,1,0,0],
                [0,0,1,1],
                [0,0,1,1],
            ],
            "initial": [0,1,2,3],
            "expected": 0,
        },

        # 6. Malware encountered during traversal.
        # Entire graph is one CC with 2 malware.
        {
            "n": 9,
            "graph": [
                [1,1,0,0,0],
                [1,1,1,0,0],
                [0,1,1,1,0],
                [0,0,1,1,1],
                [0,0,0,1,1],
            ],
            "initial": [0,4],
            "expected": 0,
        },

        # 7. Several components, only one useful candidate.
        {
            "n": 10,
            "graph": [
                [1,1,0,0,0,0],
                [1,1,0,0,0,0],
                [0,0,1,1,0,0],
                [0,0,1,1,0,0],
                [0,0,0,0,1,1],
                [0,0,0,0,1,1],
            ],
            "initial": [0,1,4],
            "expected": 4,
        },

        # 8. Large unique-malware CC beats smaller-index malware.
        {
            "n": 11,
            "graph": [
                [1,1,0,0,0,0],
                [1,1,0,0,0,0],
                [0,0,1,1,1,1],
                [0,0,1,1,1,1],
                [0,0,1,1,1,1],
                [0,0,1,1,1,1],
            ],
            "initial": [0,2],
            "expected": 2,
        },

        # 9. Isolated nodes mixed with a larger component.
        {
            "n": 12,
            "graph": [
                [1,0,0,0,0],
                [0,1,1,1,0],
                [0,1,1,1,0],
                [0,1,1,1,0],
                [0,0,0,0,1],
            ],
            "initial": [0,1,4],
            "expected": 1,
        },

        # 10. Pathological case:
        # Large CC has 2 malware and is worthless.
        # Tiny CC with one malware is the answer.
        {
            "n": 13,
            "graph": [
                [1,1,1,1,1,0,0],
                [1,1,1,1,1,0,0],
                [1,1,1,1,1,0,0],
                [1,1,1,1,1,0,0],
                [1,1,1,1,1,0,0],
                [0,0,0,0,0,1,1],
                [0,0,0,0,0,1,1],
            ],
            "initial": [0,4,5],
            "expected": 5,
        },
    ]

    solution = Solution()

    t1 = int(time.time() * 1000)

    for index, test in enumerate(tests, 1):
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        graph = test["graph"]
        initial = test["initial"]
        expected = test["expected"]

        try:
            print(f"\nTEST {index}\ngraph={graph[:20]}\ninitial={initial[:20]}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.minMalwareSpread(graph, initial)
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
