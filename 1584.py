import heapq
from typing import List

def manhattan_dist(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

class Solution:
    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        if len(points) <= 1:
            return 0

        in_set = set()
        queue = [ ]  # shortest dist to a node in visited
        
        dist = [ float("inf")  for i in range(len(points)) ]
        parent = [-1 for i in range(len(points))]

        # let's start from pointer 0
        # in_set.add(0)
        parent[0] = 0
        dist[0] = 0
        heapq.heappush(queue, (0, 0))

        while queue:
            d, u = heapq.heappop(queue) # expand next shortest point
            in_set.add(u)
            print(f" pop {u} d={d} dist[{u}]={dist[u]} in_set={in_set}")
            
            if d > dist[u]:
                continue  # stale heap record


            for v in range(len(points)):
                if v == u or v in in_set:
                    print(f"        skip v={v}")
                    continue
                                    
                new_dist = manhattan_dist(points[u], points[v])
                if new_dist < dist[v]:
                    print(f"            dist[{v}] new_dist={new_dist} {dist[v]}=>{new_dist} parent[{v}]={u}")
                    dist[v] = new_dist
                    heapq.heappush(queue, (new_dist, v))
                    parent[v] = u
                        

        print(f"    parent={parent} ")
        total_dist = 0
        for i in range(len(points)):
            total_dist += manhattan_dist(points[i], points[parent[i]])
    
        return total_dist

if __name__ == "__main__":
    tests = [
        {
            "points": [[0,0],[2,2],[3,10],[5,2],[7,0]],
            "expected": 20
        },
         {
            "points": [[3,12],[-2,5],[-4,1]],
            "expected": 18
        }
    ]

    sol = Solution()

    for i, t in enumerate(tests, 1):
        points = t["points"]
        expected = t["expected"]
        print(f"\nTest {i} points={points}")
        ans = sol.minCostConnectPoints(points)
        print(f"    answer={ans} expected={expected}")
        print(f"pass={ans == expected}")
