# You are given an array of positive integers price where price[i] denotes the price of the ith candy and a positive integer k.

# The store sells baskets of k distinct candies. The tastiness of a candy basket is the smallest absolute difference of the prices of any two candies in the basket.

# Return the maximum tastiness of a candy basket.

# Constraints:

# 2 <= k <= price.length <= 105
# 1 <= price[i] <= 109

DEBUG = False

from typing import List


class Solution:
    def maximumTastiness(self, price: List[int], k: int) -> int:
        p = sorted(price)
        n = len(p)
        max_diff = p[n-1] - p[0]
        if DEBUG:
            print(f"n={n} max_diff={max_diff} p={p}")

        if k == 2:
            return max_diff
        # assuming k >= 3 now

        if max_diff < 2: # it does not hurt
            return 0
        

        upper_bound = max_diff // (k-1)  
        if DEBUG:
            print(f"upper_bound={upper_bound}")
        if upper_bound <= 0:
            return 0


        # is there a basket B such at B's tastiness >= u ?
        # startIdx - start index of next price.
        # vacantBasketSlots - num of slots in basket to be filled
        # prevPrice - last price in basket
        # @deprecated
        def hasBasket(startIdx, vacantBasketSlots, prevPrice, u):
            if DEBUG:
                print(f"    hasBasket u={u} prevPrice={prevPrice} vacantBasketSlots={vacantBasketSlots} startIdx={startIdx}")

            while vacantBasketSlots > 0 and startIdx < n:
                while startIdx<n:
                    if p[startIdx] - prevPrice >= u:
                        break
                    else:
                        startIdx += 1

                if DEBUG:
                    print(f"    hasBacket update startIdx={startIdx}")
                if startIdx >= n:
                    if DEBUG:
                        print(f"    hasBacket startIdx >= n. return false")
                    return False   
                
                vacantBasketSlots = vacantBasketSlots - 1
                if vacantBasketSlots <= 0:
                    if DEBUG:
                        print(f"    hasBacket filled basket. return true")
                    return True # no basket
                prevPrice = p[startIdx]
                startIdx += 1

            return False    



        # replacing hasBasket
        def feasible(u):
            prev = p[0]
            remaining = k - 1

            for i in range(1, n):
                if p[i] - prev >= u:
                    prev = p[i]
                    remaining -= 1
                    if remaining == 0:
                        return True

            return False

        # test if we can get an answer >= u using binary search
        low = 0
        hi = upper_bound 
        found = False
        answer = 0
        while low <= hi:
            middle = (hi + low) // 2
            if DEBUG:
                print(f"low={low} hi={hi} middle={middle}")

            found = feasible(middle) 
            if found: # found basket whose tastiness >= middle
                answer = middle
                if DEBUG:
                    print(f"    update answer={answer}")
                low = middle + 1 # is there a better result in upper/right range?
            else:
                hi = middle - 1  # is there a worse result in lower/left range?
           

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
        {"n": 1, "price": [13, 5, 1, 8, 21, 2], "k": 3, "expected": 8},
        {"n": 2, "price": [1, 3, 1], "k": 2, "expected": 2},
        {"n": 3, "price": [7, 7, 7, 7], "k": 2, "expected": 0},
        {"n": 4, "price": [34,116,83,15,150,56,69,42,26], "k":6, "expected": 19}
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        price = test["price"]
        k = test["k"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} price={price} k={k}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.maximumTastiness(price, k)
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
