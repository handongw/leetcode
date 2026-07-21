from typing import List

"""
Given an integer n, return an array ans of length n + 1 such that for each i (0 <= i <= n), 
ans[i] is the number of 1's in the binary representation of i.

0 <= n <= 105

Input: n = 5
Output: [0,1,1,2,1,2]
Explanation:

0 -->     0
1 -->     1
2 -->    10
3 -->    11

4 -->   100
5 -->   101
6 -->   110
7 -->   111

8 -->  1000
9 -->  1001
10 --> 1010
11 --> 1011
12 --> 1100
13 --> 1101
14 --> 1110
15 --> 1111

16 -->10000

"""
class Solution:
    def countBits(self, n: int) -> List[int]:
        ans = [0]
        if n == 0:
            return ans
        if n == 1:
            ans.append(1)
            return ans

        ans = [0,1, 1]
        # 2**k <= i < 2**(k+1)
        k = 1
        i = 3
        pow_2_k = 2
        pow_2_k_1 = 4 
        while i <= n:
            if i < pow_2_k_1:
                ans.append(ans[i-pow_2_k]+1)
                i += 1
            else:
                k += 1
                pow_2_k = pow_2_k << 1
                pow_2_k_1 = pow_2_k_1 << 1
                ans.append(1)
                i += 1

        return ans

        
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
                f"Unknown argument: {a!r} (use -d and/or 1-based test indices, e.g. 10 11 12)",
                file=sys.stderr,
            )
            sys.exit(2)

    if selected_tests is not None and len(selected_tests) == 0:
        print("Test selection is empty.", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"selected_tests={selected_tests}")

    tests = [
        {"n": 10, "input": 10, "expected": [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2]},
        {"n": 11, "input": 11, "expected": [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3]},
        {"n": 12, "input": 12, "expected": [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2]},
        {"n": 13, "input": 13, "expected": [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3]},
        {"n": 14, "input": 14, "expected": [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3]},
        {"n": 15, "input": 15, "expected": [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4]},
        {"n": 16, "input": 16, "expected": [0, 1, 1, 2, 1, 2, 2, 3, 1, 2, 2, 3, 2, 3, 3, 4, 1]},
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        n_input = test["input"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} input={n_input}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.countBits(n_input)
            if result != expected:
                print(f"test {test['n']} FAIL")
                print(f"  got:      {result}")
                print(f"  expected: {expected}")
            else:
                print(f"test {test['n']} OK: (len={len(result)})")
        except Exception as e:
            print(f"test {test['n']} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")