from typing import List


class Solution:
    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        adjMap = {}
        for u, v in tickets:
            adjMap.setdefault(u, []).append(v)
        for k in adjMap.keys():
            adjMap[k].sort(reverse=True)

        currPath = []
        eulerianPath = []

        currPath.append("JFK")
        while currPath:
            adj = adjMap.get(currPath[-1], [])
            if adj:
                nextVertex = adj.pop()
                currPath.append(nextVertex)
            else:
                eulerianPath.append(currPath.pop())    

        eulerianPath.reverse()
        return eulerianPath

if __name__ == "__main__":
    sol = Solution()

    tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
    expected = ["JFK","ATL","JFK","SFO","ATL","SFO"]
    ans = sol.findItinerary(tickets)

    print(f"ans={ans} test={'PASS' if ans==expected else 'FAIL'}")
