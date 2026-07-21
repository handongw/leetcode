from functools import cache

# twist: You can climb 1 or 2 steps. However, you cannot make two moves of the same size back-to-back. 
# If you just took a 1-step move, your next move must be a 2-step move, and vice-versa.


class Solution:
    def climbStairs(self, n: int) -> int:
        if n<=0:
            return 0
        

        # prevStep is either 0, 1, or 2
        @cache
        def f(prevSteps:int, n:int):
            if prevSteps == 0: # first call
                if n == 1:
                    return 1
                elif n == 2:
                    return 1
                else:
                    return f(1, n-1) + f(2, n-2)        

            if prevSteps == 1:
                if n == 1: # no solution
                    return 0
                elif n == 2:
                    return 1
                else:
                    return f(2, n-2)
            else: # preSteps is 2:
                if n == 1: 
                    return 1
                elif n == 2:
                    return 0
                else:
                    return f(1, n-1)                

        return f(0, n)

        


if __name__ == "__main__":
    import traceback
    import time

    solver = Solution()

    # Twist: steps must alternate 1 and 2 (no two same-size moves in a row).
    # Valid sequences are only of the form 1,2,1,2,... or 2,1,2,1,...
    # For n >= 1: answer is 2 if n % 3 == 0 else 1.
    test_cases = [
        # --- Small / base cases ---
        {
            "name": "n=1 only (1)",
            "n": 1,
            "expected": 1,  # (1)
        },
        {
            "name": "n=2 only (2); (1,1) invalid",
            "n": 2,
            "expected": 1,  # (2)
        },
        {
            "name": "n=3 both patterns",
            "n": 3,
            "expected": 2,  # (1,2), (2,1)
        },
        # --- Period-3 pattern ---
        {
            "name": "n=4 only (1,2,1)",
            "n": 4,
            "expected": 1,  # (1,2,1)
        },
        {
            "name": "n=5 only (2,1,2)",
            "n": 5,
            "expected": 1,  # (2,1,2)
        },
        {
            "name": "n=6 both patterns",
            "n": 6,
            "expected": 2,  # (1,2,1,2), (2,1,2,1)
        },
        {
            "name": "n=7 only (1,2,1,2,1)",
            "n": 7,
            "expected": 1,
        },
        {
            "name": "n=8 only (2,1,2,1,2)",
            "n": 8,
            "expected": 1,
        },
        {
            "name": "n=9 both patterns",
            "n": 9,
            "expected": 2,
        },
        {
            "name": "n=10",
            "n": 10,
            "expected": 1,
        },
        {
            "name": "n=45 (45%3==0)",
            "n": 45,
            "expected": 2,
        },
    ]

    cases = None
    t1 = int(time.time() * 1000)
    succ_count = 0
    total_count = 0
    for idx, case in enumerate(test_cases, start=1):
        if cases is None or idx in cases:
            total_count += 1
            n = case["n"]
            expected = case["expected"]
            try:
                actual = solver.climbStairs(n)
                passed = actual == expected
                print(f"Case {idx}: {'PASS' if passed else 'FAIL'} — {case['name']}")
                if not passed:
                    print(f"  n={n}")
                    print(f"  expected={expected}, actual={actual}")
                print()
                if passed:
                    succ_count += 1
            except Exception as exc:
                print(f"Case {idx} raised an exception: {exc}")
                traceback.print_exc()

    t2 = int(time.time() * 1000)
    print(f"   total time={t2 - t1:,} ms  succ= {succ_count}/{total_count}")
