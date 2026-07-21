# You are given a network of n nodes, labeled from 1 to n. 
# You are also given times, a list of travel times as directed edges times[i] = (ui, vi, wi), 
# where ui is the source node, vi is the target node, and wi is the time it takes for a signal to travel from source to target.

# We will send a signal from a given node k. Return the minimum time it takes for all the n nodes to receive the signal. 
# If it is impossible for all the n nodes to receive the signal, return -1.


from typing import List
import heapq

DEBUG = False

class Solution:
    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        if DEBUG:
            print(f"  times={times}")
        adjacent_list = [[] for _ in range(n)]
        for t in times:
            u, v, time = t
            adjacent_list[u-1].append((v-1, time))
        if DEBUG:
            for u in range(len(adjacent_list)):
                print(f"    adjacent_list[{u}]={adjacent_list[u]}")

        # 2. Initialize shortest paths (Unchanged)
        shortest_path = [float('inf') for _ in range(n)]
        shortest_path[k-1] = 0

        heap = []

        for i in range(n):
            if i==k-1:
                heapq.heappush(heap, (0, i))
            else:
                heapq.heappush(heap, (float('inf'), i))

        while heap:
            time, u = heapq.heappop(heap)
            # DIJKSTRA OPTIMIZATION: Lazy Deletion
            # If we pull an outdated, slower path from the heap, just ignore it.
            if time > shortest_path[u]:
                continue

            for v, time_v in adjacent_list[u]:
                dist_v = shortest_path[u] + time_v 
                if dist_v < shortest_path[v]:
                    shortest_path[v] = dist_v
                    heapq.heappush(heap, (dist_v, v))

        if DEBUG:
            print(f"  shortest path={shortest_path}\n\n")
        answer = max(shortest_path)
        if answer == float('inf'):
            return -1
        return answer
   


if __name__ == "__main__":
    import traceback

    solver = Solution()

    test_cases = [
        {
            "times": [[2, 1, 1], [2, 3, 1], [3, 4, 1]],
            "n": 4,
            "k": 2,
            "expected": 2,
        },
        {
            "times": [[1, 2, 1]],
            "n": 2,
            "k": 1,
            "expected": 1,
        },
        {
            "times": [[1, 2, 1]],
            "n": 2,
            "k": 2,
            "expected": -1,
        },
        {
            "times": [[1, 2, 1], [3, 4, 1]],
            "n": 4,
            "k": 1,
            "expected": -1,
        },
        {
            "times": [],
            "n": 1,
            "k": 1,
            "expected": 0,
        },
        {
            "times": [[1, 2, 5], [1, 3, 2], [3, 2, 1]],
            "n": 3,
            "k": 1,
            "expected": 3,
        },
        {
            "times": [[1, 2, 1], [2, 3, 2], [3, 4, 3]],
            "n": 4,
            "k": 1,
            "expected": 6,
        },
        {
            "times": [
                [1, 2, 4], [1, 3, 4], [2, 4, 6], [3, 4, 5], [1, 4, 15],
            ],
            "n": 4,
            "k": 1,
            "expected": 9,
        },
        {
            "times": [
                [1, 2, 1], [1, 3, 2], [2, 4, 3], [2, 5, 1],
                [3, 6, 4], [3, 7, 2],
            ],
            "n": 7,
            "k": 1,
            "expected": 6,
        },
        {
            "times": [
                [1, 2, 1], [2, 3, 1], [3, 1, 1], [2, 4, 5],
            ],
            "n": 4,
            "k": 1,
            "expected": 6,
        },
        {
            "times": [
                [1, 2, 10], [1, 3, 1], [3, 2, 1], [2, 4, 1],
            ],
            "n": 4,
            "k": 1,
            "expected": 3,
        },
        {
            "times": [
                [3, 1, 2], [3, 2, 1], [3, 4, 3], [3, 5, 4], [3, 6, 5],
            ],
            "n": 6,
            "k": 3,
            "expected": 5,
        },
        {
            "times": [
                [1, 2, 1], [2, 3, 1], [3, 4, 1],
            ],
            "n": 5,
            "k": 1,
            "expected": -1,
        },
        {
            "times": [
                [1, 2, 100], [1, 3, 1], [3, 4, 1], [4, 2, 1], [2, 5, 1],
            ],
            "n": 5,
            "k": 1,
            "expected": 4,
        },
        {
            "times": [
                [1, 2, 2], [1, 3, 5], [2, 3, 1], [2, 4, 3], [3, 4, 1],
                [3, 5, 2], [4, 5, 1], [4, 6, 4], [5, 6, 1], [1, 6, 20],
            ],
            "n": 6,
            "k": 1,
            "expected": 6,
        },
        {
            "times": [
                [1, 2, 1], [2, 3, 1], [4, 5, 1], [3, 4, 10],
            ],
            "n": 5,
            "k": 1,
            "expected": 13,
        },
        {
            "times": [
                [1, 2, 1], [2, 3, 1], [3, 4, 1], [4, 5, 1], [5, 6, 1],
                [6, 7, 1], [7, 8, 1], [8, 9, 1], [9, 10, 1],
            ],
            "n": 10,
            "k": 1,
            "expected": 9,
        },
        {
            "times": [
                [1, 2, 1], [1, 3, 10], [2, 4, 10], [3, 4, 1], [4, 5, 1],
            ],
            "n": 5,
            "k": 1,
            "expected": 12,
        },
        {
            "times": [
                [4, 2, 1], [2, 1, 2], [2, 5, 1], [2, 6, 3],
                [1, 3, 1], [3, 7, 2],
            ],
            "n": 7,
            "k": 4,
            "expected": 6,
        },
        {
            "times": [
                [1, 2, 1], [2, 3, 1], [3, 1, 1], [4, 5, 1], [5, 6, 1],
            ],
            "n": 6,
            "k": 1,
            "expected": -1,
        },
        {
            "times": [
                [1, 2, 7], [1, 3, 1], [3, 4, 1], [4, 2, 1], [2, 3, 5],
            ],
            "n": 4,
            "k": 1,
            "expected": 3,
        },
    ]

    for idx, case in enumerate(test_cases, start=1):
        times = case["times"]
        n = case["n"]
        k = case["k"]
        expected = case["expected"]
        try:
            actual = solver.networkDelayTime(times, n, k)
            print(f"Case {idx}:")
            print(f"  times={times}")
            print(f"  n={n}")
            print(f"  k={k}")
            print(f"  expected={expected}")
            print(f"  actual  ={actual}")
            print(f"  pass    ={actual == expected}")
            print("\n")
        except Exception as exc:
            print(f"Case {idx} raised an exception: {exc}")
            traceback.print_exc()