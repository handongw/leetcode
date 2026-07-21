DEBUG = False

class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        m = len(s)
        n = len(t)

        state = [[ 1 if j==0 else 0 for j in range(n+1)] for i in range(m+1)]

        for i in range(1, m+1):
            for j in range(1, n+1):
                if s[i-1] == t[j-1]:
                    state[i][j] = (state[i-1][j-1] + state[i-1][j])
                else:
                    state[i][j] = state[i-1][j]

        return state[m][n]


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
        {"n": 1, "s": "rabbbit", "t": "rabbit", "expected": 3},
        {"n": 1, "s": "rabbbit", "t": "rabbit", "expected": 3},
        {"n": 2, "s": "babgbag", "t": "bag", "expected": 5},
        {"n": 3, "s": "", "t": "", "expected": 1},
        {"n": 4, "s": "abc", "t": "abc", "expected": 1},
        {"n": 5, "s": "abc", "t": "ab", "expected": 1},
        {"n": 6, "s": "abbc", "t": "ab", "expected": 2},
        {"n": 7, "s": "aaa", "t": "a", "expected": 3},
        {"n": 8, "s": "aaa", "t": "aa", "expected": 3},
        {"n": 9, "s": "a", "t": "a", "expected": 1},
        {"n": 10, "s": "a", "t": "b", "expected": 0},
        {"n": 11, "s": "abc", "t": "", "expected": 1},
        {"n": 12, "s": "", "t": "a", "expected": 0},
        {"n": 13, "s": "bdabab", "t": "bdab", "expected": 3},
        {"n": 14, "s": "daaa", "t": "da", "expected": 3},
        {"n": 15, "s": "aabb", "t": "ab", "expected": 4},
        {"n": 16, "s": "mississippi", "t": "is", "expected": 6},
        {"n": 17, "s": "abcabc", "t": "abc", "expected": 4},
        {"n": 18, "s": "aaaaa", "t": "aa", "expected": 10},
        {"n": 19, "s": "leetcode", "t": "leet", "expected": 1},
        {"n": 20, "s": "leetcode", "t": "code", "expected": 1},
        {"n": 21, "s": "babgba", "t": "ba", "expected": 4},
        {"n": 22, "s": "a" * 30, "t": "a" * 15, "expected": 155117520},
    ]

    solution = Solution()

    t1 = int(time.time() * 1000)

    for index, test in enumerate(tests, 1):
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        s = test["s"]
        t = test["t"]
        expected = test["expected"]

        try:
            print(f"\nTEST {index} s={s!r} t={t!r}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.numDistinct(s, t)
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
