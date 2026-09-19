from functools import cache
from typing import List

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:

        wordSet = set[str]()
        maxWordLen = 0

        for w in wordDict:
            wordSet.add(w)
            maxWordLen = max(len(w), maxWordLen)

        n = len(s)
        @cache
        def f(start_idx) -> List[str]:
            # print(f"start_idx={start_idx} n={n} maxWordLen={maxWordLen} suffix={s[start_idx:n]} min(n, start_idx+maxWordLen)={min(n, start_idx+maxWordLen)}")
            if start_idx >= n:
                # print(f"    return ['*']")
                return ['*']

            result = []
            for end_idx in range(start_idx+1, min(n+1, start_idx+1+maxWordLen)):
                prefix = s[start_idx:end_idx]
                # print(f"    end_idx={end_idx} prefix={prefix}")
                if prefix in wordSet:
                    # print(f"    prefix {prefix} is in wordset")
                    result2 = f(end_idx)
                    for r2 in result2:
                        if r2 == '*':
                            result.append(prefix)
                        else:
                            result.append(prefix+' '+r2)    
                else:
                    # print(f"    prefix {prefix} not in wordset")
                    pass
            # print(f"s[{start_idx}:n]={s[start_idx:n]} result={result}")        
            return result

        return f(0)
        