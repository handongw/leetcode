
# Set True to enable trace output inside Solution; False keeps solver quiet.
import traceback
from typing import Any, List


TRACE_PRINT = True
_print = print


def myPrint(*args, **kwargs):
    """Same as built-in print when TRACE_PRINT is True; no-op otherwise."""
    if TRACE_PRINT:
        _print(*args, **kwargs)


class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        endMap = {}
        for i, ch in enumerate(s):
            end = endMap.get(ch)
            if end is None:
                endMap[ch] = i
            else:
                endMap[ch] = max(i, endMap[ch])

        if TRACE_PRINT:
            myPrint(endMap)

        partitions = []
        start=0
        end=0

        for i, ch in enumerate(s):
            end=max(end, endMap[ch])
            if i>=end:
                partitions.append(end-start+1)
                start = i + 1
            
            if TRACE_PRINT:
                myPrint(f" start={start} end={end} i={i} ch={ch} partitions={partitions}")


        return partitions

        

if __name__ == "__main__":
    solver = Solution()

    test_cases = [
        {
            "str": "aa",
            "expected": [2],
        },
        {
            "str": "aa",
            "expected": [2],
        },
        {
            "str": "abc",
            "expected": [1,1,1],
        },
        {
            "str": "aabcc",
            "expected": [2,1,2],
        },
        {
            "str": "aabccbbbaadd",
            "expected": [10,2],
        },
        {
            "str": "aabccbbbaaddc",
            "expected": [13],
        },
        {
            "str": "ababcbacadefegdehijhklij",
            "expected": [9,7,8],
        },
    ]

    # cases = [4]
    cases = None
    import time
    t1 = int(time.time() * 1000)
    succCount = 0
    totalCount = 0
    for idx, case in enumerate(test_cases, start=1):
        if cases is None or idx in cases:
            totalCount += 1
            str = case["str"]
            expected = case["expected"]
            try:
                print(f"\n\nCase {idx}: {str}\n")
                actual = solver.partitionLabels(str)
                print(f"Case {idx}:")
                print(f"  str={str}")
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

