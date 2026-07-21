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


class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # matrix[i][j] is (lcs, text2 match idx) of text1[i:] and text2[j:]
        matrix = [ [(0, len(text2))] * len(text2)  for r in range(len(text1))]
        last_text1_index = len(text1) - 1

        # pre fill matrix[row][*]
        lcs, text2_match_idx = (0, len(text2))
        for text2_idx in reversed(range(len(text2))):
            if lcs > 0:
                matrix[last_text1_index][text2_idx] = (lcs, text2_match_idx)
            else:
                if text2[text2_idx] == text1[last_text1_index]:
                    lcs = 1
                    text2_match_idx = text2_idx
                    matrix[last_text1_index][text2_idx] = (lcs, text2_match_idx)
        if DEBUG:
            print(f" matrix[{last_text1_index}]={matrix[last_text1_index]}")            
        
        last_text1_index -= 1
        # fill the remaining row by row
        while last_text1_index >= 0:
            if DEBUG:
                print(f"     text1 suffix={text1[last_text1_index:]}")
            ch1 = text1[last_text1_index]
            prev_text1_index = last_text1_index + 1

            text2_match_idx = len(text2) # lcs and text1 match index for last_text1_index
            for text2_idx in reversed(range(len(text2))):
                prev_lcs, prev_text2_match_idx = matrix[prev_text1_index][text2_idx]
                if DEBUG:
                    print(f"     text2[{text2_idx}:] suffix={text2[text2_idx:]} prev_lcs={prev_lcs}, prev_text2_match_idx={prev_text2_match_idx} ")

                # if prev_text2_match_idx <= text2_idx:
                #     matrix[last_text1_index][text2_idx] = (prev_lcs, prev_text2_match_idx)
                #     continue    

                text2_match_idx = len(text2)
                # find a new char in text2 that matches ch1
                for j in range(prev_text2_match_idx-1, text2_idx-1, -1):
                    if text2[j] == ch1: # found a new char in text2 that matches ch1
                        text2_match_idx = j
                        if DEBUG:
                            print(f"          update text2_match_idx={text2_match_idx}")    
                        break
                if text2_match_idx < len(text2):
                    # update (lcs and text2 match index for last_text1_index)
                    matrix[last_text1_index][text2_idx] = (prev_lcs+1, text2_match_idx)
                else: 
                    for j in range(len(text2)-1, text2_idx, -1):
                        if text2_idx == ch1:
                            text2_match_idx = j
                            break
                    if text2_match_idx < len(text2):
                        # update (lcs and text2 match index for last_text1_index)
                        matrix[last_text1_index][text2_idx] = (1, text2_match_idx)
                    else:
                        matrix[last_text1_index][text2_idx] = (prev_lcs, prev_text2_match_idx) # copy old result

            if DEBUG:
                print(f" matrix[{last_text1_index}]={matrix[last_text1_index]}") 
            last_text1_index -= 1

        return 




if __name__ == '__main__':
    import sys
    import time

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
        {"n": 18, "text1": "oxcpqrsvwf", "text2":"shmtulqrypy", "expected": 2}
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