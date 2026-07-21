from functools import cache


class Solution:
    def isMatch(self, s: str, p: str) -> bool:

        # scan p backward to build atomic pattern list
        atomic_pattern_list = []
        i = len(p)-1
        while i>=0:
            if p[i] == '*':
                atomic_pattern_list.append((False, p[i-1]))
                i -= 2
            else:
                atomic_pattern_list.append((True, p[i]))
                i -= 1
        atomic_pattern_list.reverse() 

        @cache
        def f(s_start_idx, ap_start_idx):            
            if s_start_idx == len(s) and ap_start_idx == len(atomic_pattern_list):
                return True
            
            if s_start_idx == len(s):
                return all(not ap[0] for ap in atomic_pattern_list[ap_start_idx:])
            
            if ap_start_idx == len(atomic_pattern_list):
                return False    

            cardinality, ch = atomic_pattern_list[ap_start_idx]
            if cardinality:
                if ch == '.' or ch == s[s_start_idx]:
                    return f(s_start_idx+1, ap_start_idx+1)
                else:
                    return False
            else: # * pattern
                if ch == '.' or ch == s[s_start_idx]:
                    return (f(s_start_idx+1, ap_start_idx+1)    # match s[s_end_idx]
                            or f(s_start_idx+1, ap_start_idx)   # match s[s_end_idx] and stay at current pattern
                            or f(s_start_idx, ap_start_idx+1)   # skip to next pattern
                            )
                else:
                    return f(s_start_idx, ap_start_idx+1)  # skip to next pattern

        return f(0, 0)


if __name__ == "__main__":
    import traceback
    import time

    solver = Solution()

    test_cases = [
        {
            "s": "aa",
            "p": "a",
            "expected": False,
        },
        {
            "s": "aa",
            "p": "a*",
            "expected": True,
        },
        {
            "s": "aab",
            "p": "c*a*b",
            "expected": True,
        },
        {
            "s": "mississippi",
            "p": "mis*is*p*.",
            "expected": False,
        },
        {
            "s": "ab",
            "p": ".*",
            "expected": True,
        },
        {
            "s": "",
            "p": ".*",
            "expected": True,
        },
        {
            "s": "a",
            "p": "ab*",
            "expected": True,
        },
        {
            "s": "abcd",
            "p": "d*",
            "expected": False,
        },
    ]

    # cases = [3]
    cases = None
    t1 = int(time.time() * 1000)
    succCount = 0
    totalCount = 0
    for idx, case in enumerate(test_cases, start=1):
        if cases is None or idx in cases:
            totalCount += 1
            s = case["s"]
            p = case["p"]
            expected = case["expected"]
            try:
                print(f"\n\nCase {idx}: s={s!r} p={p!r}\n")
                actual = solver.isMatch(s, p)
                print(f"Case {idx}:")
                print(f"  s={s!r}")
                print(f"  p={p!r}")
                print(f"  expected={expected}")
                print(f"  actual  ={actual}")
                print(f"  Case {idx} pass    ={actual == expected}")
                print("\n")
                if actual == expected:
                    succCount += 1
            except Exception as exc:
                print(f"Case {idx} raised an exception: {exc}")
                traceback.print_exc()

    t2 = int(time.time() * 1000)
    print(f"   total time={t2-t1:,} ms  succ= {succCount}/{totalCount}")

