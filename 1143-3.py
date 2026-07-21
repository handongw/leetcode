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
        char_set1 = set([c for c in text1])
        char_set2 = set([c for c in text2])

        char_set = char_set1.intersection(char_set2)

        text1_copy = [c for c in text1 if c in char_set]
        text2_copy = [c for c in text2 if c in char_set]  

        if len(text1_copy)==0 or len(text2_copy)==0:
            return 0

        # now text1_copy and text2_copy have same char set              

        # text1_char_index_map = {c: [] for c in char_set}
        text2_char_index_map = {c: [] for c in char_set}
        # for i, c in enumerate(text1_copy):
        #     text1_char_index_map[c].append(i)
        for i, c in enumerate(text2_copy):
            text2_char_index_map[c].append(i)

        if DEBUG:
            print(f"char_set={char_set}")    
            print(f"text1_copy={text1_copy}")    
            print(f"text2_copy={text2_copy}")    
            # print(f"text1_char_index_map={text1_char_index_map}")    
            print(f"text2_char_index_map={text2_char_index_map}")    

        # text2_index_table[ch][end_idx] = largest index of ch in text2_copy with index <= end_idx
        n2 = len(text2_copy)
        text2_index_table = {}
        for ch in char_set:
            positions = text2_char_index_map[ch]
            table = [None] * n2
            p = -1
            for end_idx in range(n2):
                while p + 1 < len(positions) and positions[p + 1] <= end_idx:
                    p += 1
                if p >= 0:
                    table[end_idx] = positions[p]
            text2_index_table[ch] = table

        matrix = [ [ -1 for idx2 in range(len(text2_copy))]  for idx1 in range(len(text1_copy))]

        def print_matrix():
            rows, cols = len(matrix), len(matrix[0]) if matrix else 0
            if rows == 0 or cols == 0:
                print("matrix: (empty)")
                return
            w = max(len(str(matrix[i][j])) for i in range(rows) for j in range(cols))

            print("matrix (row by row):")
            print("      " + " ".join(f"{j:>{w}}" for j in range(cols)))
            for i in range(rows):
                print(f"{i:>4}  " + " ".join(f"{matrix[i][j]:>{w}}" for j in range(cols)))

        # end of initialization

        for idx1 in range(len(text1_copy)):
            ch1 = text1_copy[idx1]

            for idx2 in range(len(text2_copy)):
                ch2 = text2_copy[idx2]

                if idx1 == 0:
                    if idx2 == 0:
                        matrix[idx1][idx2] = 1 if ch1 == ch2 else 0
                    else:
                        ch1_idx_in_text2 = text2_index_table[ch1][idx2]
                        if ch1_idx_in_text2 is not None:
                            matrix[idx1][idx2] = 1
                        else:    
                            matrix[idx1][idx2] = 0
                else:
                    if matrix[idx1-1][idx2] < 0:
                        raise Exception(f" matrix[{idx1-1}][{idx2}] < 0")

                    if ch1 == ch2 and idx2 > 0:
                        matrix[idx1][idx2] = matrix[idx1-1][idx2-1]+1
                    else:    
                        result1 = matrix[idx1-1][idx2]

                        ch1_idx_in_text2 = text2_index_table[ch1][idx2]
                        if ch1_idx_in_text2 is None:
                            result2 = 0
                        elif ch1_idx_in_text2<=0:
                            result2 = 1
                        else:    
                            if matrix[idx1-1][ch1_idx_in_text2-1] < 0:
                                raise Exception(f"matrix[{idx1-1}][{ch1_idx_in_text2-1}] < 0")
                            result2 = 1 + matrix[idx1-1][ch1_idx_in_text2-1]

                        # f(idx1, idx2) = max( f(idx1-1, idx2), 1+f(idx-1, idx2-k) )    
                        matrix[idx1][idx2] = max( result1, result2)

                    if DEBUG:
                        print(f"    s1={text1_copy[:idx1+1]} s2={text2_copy[:idx2+1]} lcs={matrix[idx1][idx2]}")
                        # if ch1 == ch2 and idx2>0:
                        #     print(f"     matrix[idx1-1][idx2-1]+1 = {matrix[idx1-1][idx2-1]+1} ")
       

        result = matrix[len(text1_copy)-1][len(text2_copy)-1]
        if DEBUG:
            print_matrix()
        return result


if __name__ == '__main__':
    import sys
    import time

    # sys.setrecursionlimit(10000)

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