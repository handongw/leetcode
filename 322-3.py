class Solution:
    def coinChange(self, coins: list[int], amount: int) -> int:
        # Initialize the DP table with a value representing "infinity"
        # (amount + 1 is safe because you can never need more coins than the amount itself)
        dp = [amount + 1] * (amount + 1)
        
        # Base case: 0 coins are needed to make an amount of 0
        dp[0] = 0
        
        # Iterate through every sub-amount from 1 up to our target amount
        for i in range(1, amount + 1):
            for coin in coins:
                # If the coin can fit into the current sub-amount
                if i - coin >= 0:
                    # The minimum coins for 'i' is the minimum of its current value 
                    # OR 1 coin plus the optimal solution for the remainder (i - coin)
                    dp[i] = min(dp[i], dp[i - coin] + 1)
                    
        # If dp[amount] hasn't been changed from its initial value, it's impossible
        return dp[amount] if dp[amount] != (amount + 1) else -1
                
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
        {"n": 1, "coins": [1, 2, 5], "amount": 11, "expected": 3},
        {"n": 2, "coins": [2], "amount": 3, "expected": -1},
        {"n": 3, "coins": [1], "amount": 0, "expected": 0},
        {"n": 4, "coins": [1], "amount": 1, "expected": 1},
        {"n": 5, "coins": [1, 3, 4], "amount": 6, "expected": 2},
        {"n": 6, "coins": [186, 419, 83, 408], "amount": 6249, "expected": 20},
        {"n": 7, "coins": [1, 2147483647], "amount": 2, "expected": 2},
        {"n": 8, "coins": [3, 7], "amount": 5, "expected": -1},
        {"n": 9, "coins": [1, 2, 5, 10, 13], "amount": 30, "expected": 3},
        {"n": 10, "coins": [1, 2, 5], "amount": 100, "expected": 20},
        {"n": 11, "coins": [1, 3, 5], "amount": 8, "expected": 2},
        {"n": 12, "coins": [216,94,15,86], "amount": 5372, "expected": 26},
        {"n": 13, "coins": [5,306,188,467,494], "amount": 7047, "expected": 18},
        {"n": 14, "coins": [5,306,188], "amount": 509, "expected": 5},
        {
            "n": 15,
            "coins": list(range(1, 101)),
            "amount": 1097,
            "expected": 11,
        },
        {
            "n": 16,
            "coins": [2,4,6,8,10,12,14,16,18,20,22,24],
            "amount": 9999,
            "expected": -1,
        },
    ]

    solution = Solution()

    t1 = int(time.time() * 1000)

    for index, test in enumerate(tests, 1):
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        coins = test["coins"]
        amount = test["amount"]
        expected = test["expected"]

        try:
            print(f"\nTEST {index} coins={coins} amount={amount}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.coinChange(coins, amount)
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
