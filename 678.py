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
    def printIntermediate(self, intermediate: Dict):
        for k, v in intermediate.items():
            print(f"   {k}={v}")

    def verifyCounts(self, lpCount, rpCount, starCount):
        if lpCount+starCount < rpCount or rpCount+starCount<lpCount:
            return False
        else:
            return True            

    def checkValidString(self, s: str) -> bool:
        lpCount = 0     # left ( count
        rpCount = 0     # right ) count
        starCount = 0  # * count
        charArray = []
        for i, ch in enumerate(s):
            if ch == '*':
                starCount += 1
            elif ch == ')':
                rpCount += 1
            elif ch == '(':
                lpCount += 1 
            charArray.append({"ch":ch, "idx":i, 'lpCount':lpCount, "rpCount":rpCount, 'starCount':starCount})

        intermediate = {"(-count":0, ")-count":0, "*-count":0}      

        intermediate['lpCount']=  lpCount
        intermediate['rpCount'] = rpCount
        intermediate['starCount'] = starCount
        intermediate['str'] = s

        # print(f"  lpCount={lpCount} rpCount={rpCount} starCount={starCount}")
        if not self.verifyCounts(lpCount, rpCount, starCount):
            return False

        ret = self.checkValidCharArray(charArray, [], 0, intermediate, {})

        # self.printIntermediate(intermediate)

        return ret

    def setIntermediate(self, intermediate, index, stackSize, k, v):
        record = intermediate.get(index)
        if record is None:
            record = {}
            intermediate[f"{index}/{stackSize}"] = record
        record[k] = v    

    def getCachedResult(self, intermediate, index, stackSize, k):
        cached = intermediate.get(f"{index}/{stackSize}")
        if cached is None:
            return None
        

        # if cached.get(k) is None:
        #     print(f"   WARN: stackSize={stackSize} k={k} invalid cached={cached}")
        return cached.get(k)    

    def match(self, stack, curr, intermediate):
        if len(stack) <= 0:
            return False

        top = stack[-1]
        left = top["ch"]
        right = curr['ch']
        if left == '(':
            if right == '*' or right == ')':                
                return True
        elif left == '*':
            if right == '*' or right == ')':
                return True

        return False        

    def checkValidCharArray(self, charArray, stack, currIdx, intermediate, extra):
        # intermediate: map 
        # print(f"   stack={stack} currIdx={currIdx} intermediate={intermediate}")

        # stack: contains '(' or '*', which is used as '('

        if currIdx >= len(charArray): # passed last character
            if len(stack) <= 0:
                # print(f"   True at stack={stack} currIdx={currIdx} intermediate={intermediate}")
                return True  # it is valid
            else:
                # print(f"   False at stack={stack} currIdx={currIdx} intermediate={intermediate}")
                return False # it is invalid    

        char = charArray[currIdx]
        # print(f"     char={char}")
        ch = char["ch"]
        stackSize = len(stack)

        # print(f"   ch={ch} currIdx={currIdx} stack={stack}")

        def setStarIdx(extra, currIdx):
            starIndex = extra.get("*-index")
            if starIndex is None:
                extra["*-index"] = currIdx
            else:
                extra["*-index"] = max(currIdx, starIndex)
        
        def getStarIdx():
            starIndex = extra.get("*-index")
            if starIndex is None:
                return -1
            else:
                return starIndex
        
        if ch == '(':
            ret = self.getCachedResult(intermediate, currIdx, stackSize, "ret")
            if ret is None:
                myPrint(f"    {currIdx} {ch} check valid") 

                lpCount = len(stack) + 1 + charArray[-1]["lpCount"] - charArray[currIdx]["lpCount"]
                rpCount = charArray[-1]["rpCount"] - charArray[currIdx]["rpCount"]
                starCount = charArray[-1]["starCount"] - charArray[currIdx]["starCount"]
                if not self.verifyCounts(lpCount, rpCount, starCount):
                    ret = False
                else:    
                    hop = intermediate.get(currIdx)
                    if hop is None:
                        stack.append(char)
                        ret = self.checkValidCharArray(charArray, stack, currIdx+1, intermediate, extra)
                        self.setIntermediate(intermediate, currIdx, stackSize, "ret", ret)          
                        # self.setIntermediate(intermediate, currIdx, stackSize, "stackSize", stackSize)
                    else:
                        myPrint(f"  {currIdx} hopped {hop["hop-to"] - currIdx -1} steps {intermediate["str"][currIdx:hop["hop-to"]]} ")
                        ret = self.checkValidCharArray(charArray, stack, hop["hop-to"], intermediate, extra)
                        self.setIntermediate(intermediate, currIdx, stackSize, "ret", ret)  
            else:
                myPrint(f"    {currIdx} {ch} use cached result {ret}")                
            return ret
        elif ch == ')':    
            # must find a match in stack
            if self.match(stack, char, intermediate):
                top = stack.pop()
                if top["ch"]=='(' and top["idx"]>getStarIdx():
                    intermediate[top["idx"]] = {"hop-to": currIdx+1}
                    myPrint(f"   {top["idx"]} hop {currIdx+1-top["idx"]} {intermediate['str'][top["idx"]:currIdx+1]}")
 
                return self.checkValidCharArray(charArray, stack, currIdx+1, intermediate, extra)    
            else:
                # print(f"   False at stack={stack} currIdx={currIdx} intermediate={intermediate}")
                return False  
        else: # ch is '*': there 3 choices. try each option one by one
            # option 1: treat it as )   
            extra_clone = extra.copy()
            def useAsRP():
                ret = False
                if self.match(stack, char, intermediate):  
                    lpCount = len(stack) + charArray[-1]["lpCount"] - charArray[currIdx]["lpCount"]
                    rpCount = charArray[-1]["rpCount"] - charArray[currIdx]["rpCount"] + 1
                    starCount = charArray[-1]["starCount"] - charArray[currIdx]["starCount"]
                    if not self.verifyCounts(lpCount, rpCount, starCount):
                        ret = False
                    else:
                        stack2 = stack[:]
                        stack2.pop()
                        ret = self.checkValidCharArray(charArray, stack2, currIdx+1, intermediate, extra_clone)  
                
                # print(f"        currIdx={currIdx} try * as ) lpCount={lpCount} rpCount={rpCount} starCount={starCount} ret={ret}")
                return ret
            
            # option 2: treat it as *
            def useAsStar():
                lpCount = len(stack) + charArray[-1]["lpCount"] - charArray[currIdx]["lpCount"]
                rpCount = charArray[-1]["rpCount"] - charArray[currIdx]["rpCount"]
                starCount = charArray[-1]["starCount"] - charArray[currIdx]["starCount"]
                if not self.verifyCounts(lpCount, rpCount, starCount):
                    ret = False
                else:    
                    stack2 = stack[:]
                    ret = self.checkValidCharArray(charArray, stack2, currIdx+1, intermediate, extra_clone)

                # print(f"        currIdx={currIdx} try * as empty string ret={ret}")
                return ret     

            # option 3: treat it as (
            def useAsLP():
                lpCount = len(stack) + 1 + charArray[-1]["lpCount"] - charArray[currIdx]["lpCount"]
                rpCount = charArray[-1]["rpCount"] - charArray[currIdx]["rpCount"]
                starCount = charArray[-1]["starCount"] - charArray[currIdx]["starCount"]
                if not self.verifyCounts(lpCount, rpCount, starCount):
                    ret = False
                else:
                    stack2 = stack[:]
                    stack2.append(char)
                    ret = self.checkValidCharArray(charArray, stack2, currIdx+1, intermediate, extra_clone)
                    # print(f"        currIdx={currIdx} try * as ( ret={ret}")
                return ret

            setStarIdx(extra_clone, currIdx)
            ret = self.getCachedResult(intermediate, currIdx, stackSize, "result")
            if ret is None:
                options = [useAsRP, useAsStar, useAsLP]   

                lpCount = len(stack) + charArray[-1]["lpCount"] - charArray[currIdx]["lpCount"]
                rpCount = charArray[-1]["rpCount"] - charArray[currIdx]["rpCount"]
                starCount = charArray[-1]["starCount"] - charArray[currIdx]["starCount"]
                

                if lpCount < rpCount:
                    options = [useAsLP, useAsStar, useAsRP]
                elif lpCount == rpCount:
                    options = [useAsStar, useAsRP, useAsLP] 

                callCnt = 0
                for fn in options:
                    ret = fn()
                    callCnt += 1
                    if ret:
                        break
                myPrint(f"    {currIdx} {ch} called {callCnt} times.  result {ret}")
                self.setIntermediate(intermediate, currIdx, stackSize, "result", ret)  
            else:
                myPrint(f"    {currIdx} {ch} use cached result {ret}")   

            # print(f"   ch={ch} currIdx={currIdx} stack={stack} result={ret}")        
            return ret    

        

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

    # cases = [10]
    cases = None
    import time
    t1 = int(time.time() * 1000)
    for idx, case in enumerate(test_cases, start=1):
        if cases is None or idx in cases:
            str = case["str"]
            expected = case["expected"]
            try:
                print(f"\n\nCase {idx}: {str}\n")
                actual = solver.checkValidString(str)
                print(f"Case {idx}:")
                print(f"  str={str}")
                print(f"  expected={expected}")
                print(f"  actual  ={actual}")
                print(f"  pass    ={actual == expected}")
                print("\n")
            except Exception as exc:
                print(f"Case {idx} raised an exception: {exc}")
                traceback.print_exc()

    t2 = int(time.time() * 1000)
    print(f"   total time={t2-t1:,} ms")