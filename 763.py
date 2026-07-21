
# Set True to enable trace output inside Solution; False keeps solver quiet.
import traceback
from typing import Any, List


TRACE_PRINT = False
_print = print


def myPrint(*args, **kwargs):
    """Same as built-in print when TRACE_PRINT is True; no-op otherwise."""
    if TRACE_PRINT:
        _print(*args, **kwargs)


class Solution:
    def partitionLabels(self, s: str) -> List[int]:

        # charArray = [ch for i, ch in enumerate[str](s)]

        groups = {}

        def getFinalRoot(grp):
            """return final root of grp"""
            r = grp["root"]
            while r is not None:
                if r["root"] is None:
                    return r
                else:
                    r = r["root"]
            return r        

        def shortRootPath(grp, parent):
            """grp.root points to final root"""
            if parent['root'] is None:
                return
            else:
                grp["root"] = getFinalRoot(parent)


        def addGroup(ch, idx):
            grp = groups.get(ch)
            if grp is None: # see ch the first time; ch is the last char encountered so far
                grp = {"lo": idx, "max": idx, "root":None}
                groups[ch] = grp                
                return
            else: # ch was encountered before
                finalRoot = getFinalRoot(grp)

                if finalRoot is None: # ch does not follow another group
                    oldMax = grp["max"]
                    newMax = grp["max"] = idx
                else: # ch follows another group
                    oldMax = finalRoot["max"]
                    newMax = finalRoot["max"] = max(idx, finalRoot["max"])

                if newMax - oldMax >= 2: # there is gap: bring in new follower
                    for j in range(oldMax+1, newMax):
                        chInBtw = s[j]
                        grpInBtw = groups[chInBtw]
                        if grpInBtw["root"] is not grp:
                            grpInBtw["root"] = grp
                            # shortRootPath(grpInBtw, grp)
                            if grp['root'] is not None:                            
                                grp["root"] = getFinalRoot(grp)

            if TRACE_PRINT:
                myPrint(f"  ch={ch} idx={idx} grp={grp}")            


        for i, ch in enumerate[str](s):
            addGroup(ch, i)

        list1 = [ v for v in groups.values() if v["root"] is None   ]
        return [ v["max"]-v["lo"]+1 for v in list1]

        

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

    # cases = [6]
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

