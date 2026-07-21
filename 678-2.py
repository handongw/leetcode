import traceback
from typing import Dict, List

# Set True to enable trace output inside Solution; False keeps solver quiet.
TRACE_PRINT = False
_print = print


def myPrint(*args, **kwargs):
    """Same as built-in print when TRACE_PRINT is True; no-op otherwise."""
    if TRACE_PRINT:
        _print(*args, **kwargs)


# first cut: naive implementation
class Solution:
      

    def checkValidString(self, s: str) -> bool:
        stack = []
        maxHeap = []
        stars = 0

        def stackToStr():
            chs_in_stack = ''.join(item['ch'] for item in stack)
            return chs_in_stack

        for i, ch in enumerate(s):
            if ch == '(':
                lpIdx = len(stack)
                stack.append(ch)
                maxHeap.append(lpIdx)
            elif ch == ')':    
                if len(maxHeap) > 0:
                    lpIdx = maxHeap.pop() 
                    del stack[lpIdx:lpIdx+1]
                elif len(stack) > 0:
                    stack.pop()
                    stars -= 1    
                else:
                    return False
            else:
                lpIdx = len(stack)
                stack.append(ch)
                stars += 1 
            if TRACE_PRINT:         
                myPrint(f"  stack={stackToStr()} maxHeaps={maxHeap} stars={stars}")

        while len(maxHeap) > 0:
            lpIdx = maxHeap[-1]
            if lpIdx < len(stack) -1:
                del stack[lpIdx:lpIdx+2]
                stars -= 1
                maxHeap.pop()
                if TRACE_PRINT:
                    myPrint(f"            stack={stackToStr()} maxHeaps={maxHeap} stars={stars}")
            else:
                break        

        return len(maxHeap) == 0        

        

        

if __name__ == "__main__":
    solver = Solution()

    test_cases = [
        {
            "str": "*",
            "expected": True,
        },
        {
            "str": "()",
            "expected": True,
        },
        {
            "str": "()()",
            "expected": True,
        },
        {
            "str": "(*)",
            "expected": True,
        },
        {
            "str": "(*))",
            "expected": True,
        },
        {
            "str": "((())",
            "expected": False,
        },
        {
            "str": "(((**",
            "expected": False,
        },
        {
            "str": "((((()(()()()*()(((((*)()*(**(())))))(())()())(((())())())))))))(((((())*)))()))(()((*()*(*)))(*)()",
            "expected": True
        },
        {
            "str": "(((((*(()((((*((**(((()()*)()()()*((((**)())*)*)))))))(())(()))())((*()()(((()((()*(())*(()**)()(())",
            "expected": False
        },
        {
            "str": "((((((((((((((((((******************",
            "expected": True
        },
        {
            "str": "**************************************************))))))))))))))))))))))))))))))))))))))))))))))))))",
            "expected": True
        },
        {
            "str": "((((()(()()()*()(((((*)()*(**(())))))(())()())(((())())())))))))(((((())*)))()))(()((*()*(*)))(*)()",
            "expected": True
        },
        {
            "str": "**()))",
            "expected": True
        }
    ]

    # cases = [6,7]
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
                actual = solver.checkValidString(str)
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