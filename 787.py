# There are n cities connected by some number of flights. You are given an array flights where flights[i] = [fromi, toi, pricei] indicates that there is a flight from city fromi to city toi with cost pricei.

# You are also given three integers src, dst, and k, return the cheapest price from src to dst with at most k stops. If there is no such route, return -1.

# Constraints:

#     2 <= n <= 100
#     0 <= flights.length <= (n * (n - 1) / 2)
#     flights[i].length == 3
#     0 <= fromi, toi < n
#     fromi != toi
#     1 <= pricei <= 104
#     There will not be any multiple flights between two cities.
#     0 <= src, dst, k < n
#     src != dst


from collections import deque
from typing import List

DEBUG = False

class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:
        adjacent_list = [[] for _ in range(n)]
        for f in flights:
            adjacent_list[f[0]].append((f[1], f[2]))

        # <= k stops restriction: makes it possible that an early promising path rejected later on; 
        # an early bad short path survives at the end.
        # so we need to track best cost as well path steps in cost_state.
        # flights used: 0 at src, at most k+1 to allow k stops; index step+1 needs size k+2
        cost_state = [[float('inf')] * (k + 2) for _ in range(n)]
        cost_state[src][0] = 0

        inQueue = [False for _ in range(n)]

        inQueue[src] = True
        queue = deque([(src, 0)])  # (vertex, steps)

        ans = float('inf')
        while queue:
            u, step = queue.popleft()
            if DEBUG:
                print(f"    cost={cost_state} pop q=({u},{step})")

            inQueue[u] = False
            if u == dst:
                if DEBUG:
                    print(f"    found an candidate answer cost_state[{u}][{step}]={cost_state[u][step]}")
                ans = min(ans, cost_state[u][step])

            for v, price in adjacent_list[u]:
                new_cost = cost_state[u][step] + price

                if step <= k and new_cost < cost_state[v][step+1]:
                    if DEBUG:
                        print(f"        update cost[{v}]=({new_cost},{step+1}) from {cost_state[v]}")
                    cost_state[v][step+1] = new_cost
                    # if not inQueue[v]:
                    queue.append((v, step+1))
                    inQueue[v] = True
                    # parent[v] = u

        return -1 if ans == float('inf') else ans

if __name__ == "__main__":
    import traceback

    solver = Solution()

    test_cases = [
        # --- LeetCode examples ---
        {
            "name": "LC example 1: k limits hops, must take expensive 1-stop path",
            "n": 4,
            "flights": [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]],
            "src": 0,
            "dst": 3,
            "k": 1,
            "expected": 700,
        },
        {
            "name": "LC example 2: multi-hop cheaper than direct",
            "n": 3,
            "flights": [[0, 1, 100], [1, 2, 100], [0, 2, 500]],
            "src": 0,
            "dst": 2,
            "k": 1,
            "expected": 200,
        },
        {
            "name": "LC example 3: k=0, direct only",
            "n": 3,
            "flights": [[0, 1, 100], [1, 2, 100], [0, 2, 500]],
            "src": 0,
            "dst": 2,
            "k": 0,
            "expected": 500,
        },
        # --- Basic edge cases ---
        {
            "name": "no flights at all",
            "n": 3,
            "flights": [],
            "src": 0,
            "dst": 2,
            "k": 1,
            "expected": -1,
        },
        {
            "name": "single edge, k=0",
            "n": 2,
            "flights": [[0, 1, 42]],
            "src": 0,
            "dst": 1,
            "k": 0,
            "expected": 42,
        },
        {
            "name": "k=0, no direct flight",
            "n": 3,
            "flights": [[0, 1, 1], [1, 2, 1]],
            "src": 0,
            "dst": 2,
            "k": 0,
            "expected": -1,
        },
        {
            "name": "disconnected graph",
            "n": 3,
            "flights": [[0, 1, 5], [2, 1, 5]],
            "src": 0,
            "dst": 2,
            "k": 2,
            "expected": -1,
        },
        # --- k too small ---
        {
            "name": "cheapest path needs 2 stops, k=1",
            "n": 4,
            "flights": [[0, 1, 1], [1, 2, 1], [2, 3, 1]],
            "src": 0,
            "dst": 3,
            "k": 1,
            "expected": -1,
        },
        {
            "name": "cheapest path needs 2 stops, k=2",
            "n": 4,
            "flights": [[0, 1, 1], [1, 2, 1], [2, 3, 1]],
            "src": 0,
            "dst": 3,
            "k": 2,
            "expected": 3,
        },
        {
            "name": "direct exists but chain is cheaper; k=1 still picks direct",
            "n": 4,
            "flights": [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 100]],
            "src": 0,
            "dst": 3,
            "k": 1,
            "expected": 100,
        },
        {
            "name": "direct exists but chain is cheaper; k=2 picks chain",
            "n": 4,
            "flights": [[0, 1, 1], [1, 2, 1], [2, 3, 1], [0, 3, 100]],
            "src": 0,
            "dst": 3,
            "k": 2,
            "expected": 3,
        },
        # --- k-sensitive (cheap path needs more stops) ---
        {
            "name": "cheaper 2-stop path exists but k=1 forces expensive 1-stop",
            "n": 4,
            "flights": [[0, 1, 1], [0, 2, 5], [1, 2, 1], [2, 3, 1]],
            "src": 0,
            "dst": 3,
            "k": 1,
            "expected": 6,
        },
        {
            "name": "same graph, k=2 allows cheaper 2-stop path",
            "n": 4,
            "flights": [[0, 1, 1], [0, 2, 5], [1, 2, 1], [2, 3, 1]],
            "src": 0,
            "dst": 3,
            "k": 2,
            "expected": 3,
        },
        {
            "name": "detour through third city is cheaper; k=1 vs k=2",
            "n": 5,
            "flights": [[0, 1, 5], [1, 2, 5], [0, 3, 2], [3, 1, 2], [1, 4, 1]],
            "src": 0,
            "dst": 4,
            "k": 1,
            "expected": 6,
        },
        {
            "name": "detour through third city is cheaper; k=2",
            "n": 5,
            "flights": [[0, 1, 5], [1, 2, 5], [0, 3, 2], [3, 1, 2], [1, 4, 1]],
            "src": 0,
            "dst": 4,
            "k": 2,
            "expected": 5,
        },
        # --- Cycles (positive weights; cycles should not help) ---
        {
            "name": "cycle in graph, 1-stop path beats direct",
            "n": 3,
            "flights": [[0, 1, 1], [1, 0, 1], [1, 2, 1], [0, 2, 100]],
            "src": 0,
            "dst": 2,
            "k": 1,
            "expected": 2,
        },
        # --- Longer chains ---
        {
            "name": "chain of 4 edges, k exactly enough",
            "n": 5,
            "flights": [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 1]],
            "src": 0,
            "dst": 4,
            "k": 3,
            "expected": 4,
        },
        {
            "name": "chain of 4 edges, k one short",
            "n": 5,
            "flights": [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 1]],
            "src": 0,
            "dst": 4,
            "k": 2,
            "expected": -1,
        },
        # --- Multiple routes same cost ---
        {
            "name": "two equal-cost routes, k=0",
            "n": 3,
            "flights": [[0, 1, 10], [0, 2, 10], [1, 2, 10]],
            "src": 0,
            "dst": 2,
            "k": 0,
            "expected": 10,
        },
        {
            "name": "two equal-cost 1-stop routes",
            "n": 3,
            "flights": [[0, 1, 5], [0, 2, 5], [1, 2, 3], [2, 1, 3]],
            "src": 0,
            "dst": 2,
            "k": 1,
            "expected": 5,
        },
    ]

    for idx, case in enumerate(test_cases, start=1):
        n = case["n"]
        flights = case["flights"]
        src = case["src"]
        dst = case["dst"]
        k = case["k"]
        expected = case["expected"]
        try:
            actual = solver.findCheapestPrice(n, flights, src, dst, k)
            passed = actual == expected
            print(f"Case {idx}: {'PASS' if passed else 'FAIL'} — {case['name']}")
            if not passed:
                print(f"  n={n}, flights={flights}")
                print(f"  src={src}, dst={dst}, k={k}")
                print(f"  expected={expected}, actual={actual}")
            print()
        except Exception as exc:
            print(f"Case {idx} raised an exception: {exc}")
            traceback.print_exc()