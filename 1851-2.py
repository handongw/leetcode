from typing import List


class Solution:
    def minInterval(self, intervals: List[List[int]], queries: List[int]) -> List[int]:
        intervals.sort(key=lambda item: item[0])  # O(nlog(n))

        result = []
        for q in queries:
            x = len(intervals)
            # find smallest index x where q < intervals[x][0]
            left = 0
            right = len(intervals) - 1
            while left <= right:
                mid = left + (right - left) // 2
                if q < intervals[mid][0]:
                    x = mid
                    right = mid - 1
                else:
                    left = mid + 1
            
            if x <= 0:
                result.append(-1)
            else:
                minSize = 1e8
                while True:
                    if intervals[x-1][0] <= q and q<=intervals[x-1][1]:
                        minSize = min(minSize, intervals[x-1][1] - intervals[x-1][0] + 1)
                    x -= 1
                    if x < 0: 
                        break;
                if minSize == 1e8:
                    minSize = -1        
                result.append(minSize)            
            
        return result

if __name__ == "__main__":
    solver = Solution()

    test_cases = [
        {
            "intervals": [[1, 4], [2, 4], [3, 6], [4, 4]],
            "queries": [2, 3, 4, 5],
            "expected": [3, 3, 1, 4],
        },
        {
            "intervals": [[2, 3], [2, 5], [1, 8], [20, 25]],
            "queries": [2, 19, 5, 22],
            "expected": [2, -1, 4, 6],
        },
        {
            "intervals": [[9,9],[1,10],[1,3],[9,10],[8,8]],
            "queries": [1,5,3,10,5],
            "expected": [3,10,3,2,10],
        },
        {
            "intervals": [[9,9],[1,10],[1,3],[9,10],[8,8],[1,5],[3,8],[5,5],[1,6],[1,9]],
            "queries": [8,1,5,1,5,7,1,9,8,1],
            "expected": [1,3,1,3,1,6,3,1,1,3],
        },
    ]

    for idx, case in enumerate(test_cases, start=1):
        intervals = [item[:] for item in case["intervals"]]
        queries = case["queries"][:]
        expected = case["expected"]
        try:
            actual = solver.minInterval(intervals, queries)
            print(f"Case {idx}:")
            print(f"  intervals={intervals}, queries={queries}")
            print(f"  expected={expected}")
            print(f"  actual  ={actual}")
            print(f"  pass    ={actual == expected}")
            print("\n")
        except Exception as exc:
            print(f"Case {idx} raised an exception: {exc}")
