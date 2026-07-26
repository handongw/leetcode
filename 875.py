DEBUG = False

from typing import List


class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:

        def hours_k (k:int) -> int:
            total = 0
            for p in piles:
                total += (p+k-1) // k # ceil(p/k)
            return total    

        maxPile = 0
        sumPile = 0
        for p in piles:
            maxPile = max(maxPile, p)
            sumPile += p

        lo = sumPile // h
        hi = maxPile
        answer = maxPile

        while lo <= hi:
            mid = (lo+hi) // 2
            hours = hours_k(mid)

            if DEBUG:
                print(f"    lo={lo} k={mid} hi={hi} hours={hours} h={h}")

            if hours > h:
                lo = mid + 1  # it takes too long, need to increase eating speed
            else: # hours <= h
                if DEBUG:
                    print(f"        update answer={answer} => min({answer}, {hours}) = {min(answer, mid)}")
                answer = min(answer, mid) # decrease answer to make it robust
                hi = mid - 1        


        return answer


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
        {"n": 1, "piles": [3, 6, 7, 11], "h": 8, "expected": 4},
        {"n": 2, "piles": [30, 11, 23, 4, 20], "h": 5, "expected": 30},
        {"n": 3, "piles": [30, 11, 23, 4, 20], "h": 6, "expected": 23},
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        piles = test["piles"]
        h = test["h"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} piles={piles!r} h={h}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.minEatingSpeed(piles, h)
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
