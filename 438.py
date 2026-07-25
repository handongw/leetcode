# Given two strings s and p, return an array of all the start indices of p's anagrams in s. 
# You may return the answer in any order

# Constraints:

# 1 <= s.length, p.length <= 3 * 104
# s and p consist of lowercase English letters.
DEBUG = False

from typing import List


class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        plen = len(p)
        if plen > len(s):
            return []

        refHistogram = {}
        for c in p:
            refHistogram.setdefault(c, 0)    
            refHistogram[c] += 1
        if DEBUG:
            print(f"refHistogram={refHistogram}")    

        result = []
        # pointers of sliding window
        lo = 0
        histo = {}
        for i in range(plen):
            c = s[i]
            histo.setdefault(c, 0)
            histo[c] += 1
        if DEBUG:
            print(f"cmp first sub string: {histo}")    
        if histo == refHistogram:
            result.append(lo)

        for hi in range(plen,len(s)):
            c = s[hi]
            histo.setdefault(c, 0)
            histo[c] += 1

            histo[s[lo]] -= 1    # reduce count of s[lo]
            if histo[s[lo]] == 0:
                del histo[s[lo]]
            lo += 1  # shift sliding window    

            if histo == refHistogram:
                result.append(lo)    

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
        {"n": 1, "s": "cbaebabacd", "p": "abc", "expected": [0, 6]},
        {"n": 2, "s": "abab", "p": "ab", "expected": [0, 1, 2]},
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        s = test["s"]
        p = test["p"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} s={s!r} p={p!r}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.findAnagrams(s, p)
            # answer may be returned in any order
            if sorted(result) != sorted(expected):
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
