# You are given an array of non-overlapping intervals intervals where intervals[i] = [starti, endi] represent the start and the end of the ith interval and intervals is sorted in ascending order by starti. You are also given an interval newInterval = [start, end] that represents the start and end of another interval.

# Two intervals are considered overlapping if they share at least one point.

# Insert newInterval into intervals such that intervals is still sorted in ascending order by starti and intervals still does not have any overlapping intervals (merge overlapping intervals if necessary).

# Return intervals after the insertion.

# Note that you don't need to modify intervals in-place. You can make a new array and return it.

from typing import List


class Solution:
    def insert(self, intervals: List[List[int]], newInterval: List[int]) -> List[List[int]]:
        n = len(intervals)
        if n <= 0:
            return [newInterval]

        # find max k1 such that intervals[k1][0] <= newInterval[0]
        # lo = 0
        # hi = n-1
        # k1 = -1

        # while lo <= hi:
        #     mid = (lo+hi) // 2
        #     midStart = intervals[mid][0]
        #     if midStart > newInterval[0]:
        #         hi = mid - 1
        #     else: # midStart <= newInterval[0]
        #         k1 = mid
        #         lo = mid + 1
        
        # # find min k2 such that intervals[k2][1] >= newInterval[1]
        # lo = 0
        # hi = n - 1
        # k2 = n
        # while lo <= hi:
        #     mid = (lo+hi) // 2
        #     midEnd = intervals[mid][1]
        #     if midEnd >= newInterval[1]:
        #         k2 = mid
        #         hi = mid - 1
        #     else:
        #         lo = mid + 1    
        
        # if k1 == -1: insert new interval at the begin
        # if interval[k1][1] < newInterval[0]: insert new interval after k1-th interval
        # else merge k1-th interval and newInterval

        # if k2 == n: new interval ends at the end
        # if interval[k2][0] > newInterval[1]: insert new interval before k2-th interval
        # else merge k2-th interval and newInterval

        def cmp(item1, item2):
            if item1[1] < item2[0]:
                return -1 # item1 in front of item2
            if item1[0] > item2[1]:
                return 1 # iterm1 is after item2
            else:
                return 0 # item1 and item2 overlap        

        result = []
        newItem = [newInterval[0], newInterval[1]]
        newItemInserted = False

        for i, x in enumerate(intervals):
            pos = cmp(newItem, x)
            if pos < 0:
                if not newItemInserted:
                    result.append(newItem)
                    newItemInserted = True
                result.append(x)
            elif pos > 0:
                result.append(x)
            else:
                newItem[0] = min(newItem[0], x[0])
                newItem[1] = max(newItem[1], x[1])
        if not newItemInserted:
            result.append(newItem)                


        return result


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
            "intervals": [[1, 3], [6, 9]],
            "newInterval": [2, 5],
            "expected": [[1, 5], [6, 9]],
        },
        {
            "n": 2,
            "intervals": [[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]],
            "newInterval": [4, 8],
            "expected": [[1, 2], [3, 10], [12, 16]],
        },
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        intervals = test["intervals"]
        newInterval = test["newInterval"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} intervals={intervals!r} newInterval={newInterval!r}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.insert(intervals, newInterval)
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

