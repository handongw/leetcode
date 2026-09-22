DEBUG = False

class Solution:
    def minWindow(self, s1: str, s2: str) -> str:
        m = len(s2) 
        n = len(s1)

        #   s1[p] ... .....  s1[j]
        #   s2[0] .......... s2[i]
        #
        #   s1[p] ... .........  s1[j]
        #        s2[0] ..... s2[i]

        # state[i][j] = p, where max p>=0 and p<=j-i (j-p>=i) such that s2[:i+1] is sub sequence of s1[p:j+1]
        # state[i][j] = None otherwise
        state = [ [ None for _ in range(n)] for _ in range(m) ]

        # initilaize state[0]
        last_p = None
        for j in range(n):
            if s1[j] == s2[0]:
                state[0][j] = j
                last_p = j
            else:
                state[0][j] = last_p  

        if DEBUG:
            print(f"state[0]={state[0]}")          

        for i in range(1, m):
            last_p = None
            for j in range(i, n):
                if s2[i] == s1[j]:
                    state[i][j] = state[i-1][j-1]
                    last_p = state[i][j]
                    if DEBUG:
                        print(f"    s2[{i}] == s1[{j}] last_p={last_p}")
                else:
                    if DEBUG:
                        print(f"    s2[{i}] != s1[{j}] state[{i}][{j}] = {last_p}")
                    state[i][j] = last_p
            if DEBUG:
                print(f"state[{i}]={state[i]}")          

        answer = (n+1, n+1, n+1)  # (length, start_index) of s1 substring
        for j in range(n):
            p = state[m-1][j]
            if p is not None:
                # return s1[p:j+1]
                answer = min(answer, (j+1-p, p, j+1))
                # if j+1-p < answer[0] or j+1-p==answer[0] and p<answer[1]:
                #     answer = (j+1-p, p, j+1)

        if DEBUG:
            print(f"answer={answer}")
            
        if answer[0] == n+1:        
            return ''        
        else:
            return s1[answer[1]:answer[2] ]    


# Constraints:

# 1 <= s1.length <= 2 * 104
# 1 <= s2.length <= 100
# s1 and s2 consist of lowercase English letters.        