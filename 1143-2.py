"""
Given two strings text1 and text2, return the length of their longest common
subsequence. If there is no common subsequence, return 0.

A subsequence of a string is a new string generated from the original string
with some characters (can be none) deleted without changing the relative order
of the remaining characters.

The test suite below is for longestCommonSubsequence.

1 <= text1.length, text2.length <= 1000
text1 and text2 consist of only lowercase English characters.

Example 1:
Input: text1 = "abcde", text2 = "ace"
Output: 3

Example 2:
Input: text1 = "abc", text2 = "abc"
Output: 3

Example 3:
Input: text1 = "abc", text2 = "def"
Output: 0
"""

from functools import cache


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        char_set = set()
        for c in text1:
            char_set.add(c)
        for c in text2:
            char_set.add(c)

        text1_copy = [c for c in text1 if c in char_set]
        text2_copy = [c for c in text2 if c in char_set]                

        text1_char_index_map = {c: [] for c in char_set}
        text2_char_index_map = {c: [] for c in char_set}
        for i, c in enumerate(text1_copy):
            text1_char_index_map[c].append(i)
        for i, c in enumerate(text2_copy):
            text2_char_index_map[c].append(i)

        if DEBUG:
            print(f"text1_copy={text1_copy}")    
            print(f"text2_copy={text2_copy}")    
            print(f"text1_char_index_map={text1_char_index_map}")    
            print(f"text2_char_index_map={text2_char_index_map}")    

        @cache
        def text2_index_of(ch, end_idx):
            for i in reversed(text2_char_index_map[ch]):
                if i<=end_idx:
                    return i
            return None            

        @cache
        def f(text1_end_idx, text2_end_idx):


            ch1 = text1_copy[text1_end_idx]
            # find last index of ch1 in text2 and index <= text2_end_idx    
            ch1_idx_in_text2 = text2_index_of(ch1, text2_end_idx)

            if text1_end_idx>0:
                result1 = f(text1_end_idx-1, text2_end_idx) # result without ch1
            else:
                result1 = 0

            if ch1_idx_in_text2 is None:
                result2 = 0
            elif  ch1_idx_in_text2<=0:    
                result2 = 1
            elif text1_end_idx <=0:
                result2 = 1    
            else:
                result2 = 1+ f(text1_end_idx-1, ch1_idx_in_text2-1) # result ends with ch1

            if DEBUG:
                print(f"text1({text1_end_idx})={text1_copy[:text1_end_idx+1]}")
                print(f"text2({text2_end_idx})={text1_copy[:text2_end_idx+1]}")
                print(f"   result1={result1} result2={result2}")
            return max(result1, result2)                

        return f(len(text1_copy)-1, len(text2_copy)-1)    


if __name__ == '__main__':
    import sys
    import time

    sys.setrecursionlimit(10000)

    def _brute_lcs(text1: str, text2: str) -> int:
        """Reference O(m*n) DP for building large-test expected output."""
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]


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
                f"Unknown argument: {a!r} (use -d and/or 1-based test indices, e.g. 1 2 3)",
                file=sys.stderr,
            )
            sys.exit(2)

    if selected_tests is not None and len(selected_tests) == 0:
        print("Test selection is empty.", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"selected_tests={selected_tests}")

    _long_a = "bsbininodmadyfjorhm"
    _long_b = "fobqrngihbfwflfkz"

    tests = [
        {"n": 1, "text1": "abcde", "text2": "ace", "expected": 3},
        {"n": 2, "text1": "abc", "text2": "abc", "expected": 3},
        {"n": 3, "text1": "abc", "text2": "def", "expected": 0},
        {"n": 4, "text1": "a", "text2": "a", "expected": 1},
        {"n": 5, "text1": "a", "text2": "b", "expected": 0},
        {"n": 6, "text1": "abcd", "text2": "abcd", "expected": 4},
        {"n": 7, "text1": "abcba", "text2": "abcbcba", "expected": 5},
        {"n": 8, "text1": "abc", "text2": "cab", "expected": 2},
        {"n": 9, "text1": "aaaa", "text2": "aa", "expected": 2},
        {"n": 10, "text1": "oxcpqrsvwfuvwsg", "text2": "shmtulqrypy", "expected": 2},
        {"n": 11, "text1": "pmjghexybyrgzczy", "text2": "hafcdqflwrf", "expected": 2},
        {"n": 12, "text1": "ezupkr", "text2": "ubmrapg", "expected": 2},
        {"n": 13, "text1": "bl", "text2": "ybyuicld", "expected": 2},
        {"n": 14, "text1": "abc", "text2": "bac", "expected": 2},
        {"n": 15, "text1": _long_a, "text2": _long_b, "expected": _brute_lcs(_long_a, _long_b)},
        {"n": 16, "text1": "ezupkr", "text2": "ubmrapg", "expected":2},
        {
            "n": 17,
            "text1": "a" * 500 + "b" * 500,
            "text2": "a" * 500 + "c" * 500,
            "expected": _brute_lcs("a" * 500 + "b" * 500, "a" * 500 + "c" * 500),
        },
        {"n": 18, "text1": "pmjghexybyrgzczy", "text2":"hafcdqbgncrcbihkd", "expected": 4}
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        text1 = test["text1"]
        text2 = test["text2"]
        expected = test["expected"]

        try:
            if len(text1) > 20 or len(text2) > 20:
                t1_repr = f"len={len(text1)}"
                t2_repr = f"len={len(text2)}"
            else:
                t1_repr = repr(text1)
                t2_repr = repr(text2)
            print(f"\nTEST {test['n']} text1={t1_repr} text2={t2_repr}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.longestCommonSubsequence(text1, text2)
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