from collections import deque
from typing import List

DEBUG = False

class Solution:
    def networkBecomesIdle(self, edges: List[List[int]], patience: List[int]) -> int:
        # assume vertex 0 can reach every other vertex

        n = len(patience)
        
        # build adjacent list
        adjacent = [[] for _ in range(n)]
        for e in edges:
            adjacent[e[0]].append(e[1])
            adjacent[e[1]].append(e[0])

        visited = [False] * n
        distances = [0] * n # distance from vertex 0

        q = deque()
        q.append(0)
        visited[0] = True
        
        while q:
            u = q.popleft()
            if DEBUG:
                print(f"    u={u} q={q} adjacent={adjacent[u]}")
            for v in adjacent[u]:
                if not visited[v]:
                    q.append(v)
                    visited[v] = True
                    distances[v] = distances[u] + 1
        if DEBUG:
            print(f"distances={[(i, v) for i, v in enumerate(distances)]}")

        maxIdleTime = 0
        dataServer = 0

        for i in range(1, n):
            dist = distances[i]
            roundtripTime = dist*2

            p = patience[i]

            k = roundtripTime // p

            while(p*k >= roundtripTime):
                k -= 1
              

            # k*p < roundtripTime
            lastCheckMsgTime = k*p + roundtripTime  + 1
            if DEBUG:
                print(f"    server {i}: p={p} round trip={roundtripTime} k={k} last msg arrive time={lastCheckMsgTime}")

            if lastCheckMsgTime > maxIdleTime:
                maxIdleTime = lastCheckMsgTime
                dataServer = i

        if DEBUG:
            print(f"result idle time = {maxIdleTime} server={dataServer}")

        return maxIdleTime


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
        {
            "n": 1,
            "edges": [[0, 1], [1, 2]],
            "patience": [0, 2, 1],
            "expected": 8,
        },
        {
            "n": 2,
            "edges": [[0, 1], [0, 2], [1, 2]],
            "patience": [0, 10, 10],
            "expected": 3,
        },
        {
            "n": 3,
            "edges":[[34,90],[82,5],[184,178],[92,32],[125,98],[149,134],[120,154],[37,129],[30,180],[161,2],[116,20],[42,12],[62,73],[96,162],[174,31],[124,101],[43,82],[87,59],[127,137],[103,7],[58,14],[119,133],[1,15],[84,113],[164,122],[128,104],[141,36],[81,166],[170,182],[89,30],[85,84],[109,1],[28,70],[83,102],[117,60],[31,169],[159,76],[146,67],[151,58],[23,34],[148,184],[179,19],[123,115],[70,21],[78,33],[99,26],[155,71],[104,100],[16,151],[72,147],[95,124],[13,138],[133,53],[60,116],[173,63],[29,56],[80,120],[17,43],[55,110],[6,119],[154,143],[51,172],[14,39],[112,38],[39,32],[35,132],[98,159],[160,107],[73,65],[183,27],[177,78],[136,46],[18,75],[27,91],[71,163],[100,77],[122,51],[178,45],[52,55],[59,160],[12,114],[38,42],[113,4],[163,167],[171,131],[167,183],[7,37],[102,54],[91,156],[40,92],[139,74],[142,145],[147,62],[0,128],[66,165],[111,175],[107,16],[22,80],[92,53],[94,86],[153,24],[74,3],[165,108],[176,130],[181,177],[67,95],[144,117],[15,135],[57,93],[145,8],[8,48],[26,127],[36,171],[126,40],[168,157],[108,121],[56,109],[65,88],[169,35],[130,181],[110,9],[2,22],[137,87],[152,118],[182,174],[53,32],[79,10],[114,47],[63,161],[0,94],[0,32],[76,150],[131,112],[129,105],[121,168],[118,111],[68,83],[69,61],[5,173],[172,149],[20,179],[162,57],[21,158],[166,11],[105,139],[93,44],[97,79],[106,23],[47,123],[46,49],[77,50],[157,153],[138,126],[0,69],[88,97],[24,68],[156,176],[92,39],[48,41],[158,170],[86,146],[61,142],[54,125],[19,148],[175,52],[44,85],[9,103],[135,144],[33,152],[90,66],[140,6],[101,28],[143,136],[75,96],[41,155],[53,39],[115,140],[150,13],[134,72],[180,164],[64,81],[45,106],[49,141],[50,89],[4,99],[11,25],[10,64],[25,17],[3,18],[132,29]],
            "patience":[0,5,4,6,8,6,10,3,11,1,9,1,9,13,9,9,12,3,6,7,2,5,1,4,7,4,18,10,7,9,16,1,24,1,5,15,5,8,11,2,27,4,10,1,3,4,3,8,1,10,12,21,3,2,17,1,1,1,5,3,4,29,11,2,4,2,9,9,12,9,2,10,9,7,5,7,9,3,10,2,7,4,8,3,12,4,16,6,4,22,6,13,20,1,2,8,1,2,5,16,29,16,5,1,27,2,5,22,1,6,4,5,7,5,15,5,4,5,4,6,8,5,8,24,23,17,7,8,3,1,7,5,2,17,4,5,11,9,16,1,12,13,26,1,7,4,18,1,7,12,19,12,1,10,3,3,14,8,15,19,22,1,4,22,14,1,4,1,11,11,13,2,2,1,1,7,8,2,2,1,15,3,4,19,1],
            "expected": 123,
        },
         {
            "n": 4,
            "edges": [[0, 1], [0, 2], [2, 3], [1,3]],
            "patience": [0, 10, 10, 2],
            "expected": 7,
        },
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        edges = test["edges"]
        patience = test["patience"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} edges={edges!r} patience={patience!r}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.networkBecomesIdle(edges, patience)
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
