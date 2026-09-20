import re

DEBUG = False

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        p = re.sub(r'\*{2,}', '*', p)  # compress multiple * chars to a single * to simplify state transition

        m = len(p)
        n = len(s)
        activePatternSet = set[int]()  # last index of all reachable pattern prefix including epsilon transitions

        if m == 0:
            if n == 0:
                return True
            else:
                return False    

        def print_activePatternSet(patternSet:set[int]):
            result = []
            for lastIdx in patternSet:
                result.append(f"lastIdx={lastIdx} {p[0:lastIdx+1]}")
            print(f"{', '.join(result)}")    
        
        if p[0] == '*':
            activePatternSet.add(0) # epsilon transition. no need to keep S0
        else:
            activePatternSet.add(-1)  # S0 

        for i in range(n):
            c = s[i]

            if DEBUG:
                print(f"start scan {s[0:i+1]}")
                print_activePatternSet(activePatternSet)
                print("\n")

            newActivePatternSet = set[int]()
            def add_active_pattern(lastIdx:int, lastChar:str):
                newActivePatternSet.add(lastIdx)
                if lastChar !='*' and lastIdx+1 < m and p[lastIdx+1] == '*': 
                    newActivePatternSet.add(lastIdx+1)  # epsilon transition

            for lastIdx in activePatternSet:
                lastPatternChar = p[lastIdx] if lastIdx>=0 else ''
                if lastPatternChar == '*':
                    add_active_pattern(lastIdx, lastPatternChar)
                    if lastIdx == m-1:
                        return True

                if lastIdx < m-1:
                    nextPatternChar = p[lastIdx+1]

                    if nextPatternChar == '*' or nextPatternChar == '?' or nextPatternChar == c:
                        add_active_pattern(lastIdx+1, nextPatternChar)

            activePatternSet = newActivePatternSet
            if DEBUG:
                print(f"end scan {s[0:i+1]}")
                print_activePatternSet(activePatternSet)
                print("\n")
            if not activePatternSet:
                return False    
           
        if (m-1) in activePatternSet:
            return True
        else:
            return False                                

                                