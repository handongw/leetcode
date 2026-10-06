DEBUG = False

class Solution:
    def longestValidParentheses(self, s: str) -> int:

        longest = 0
        stack: list[int] = []  # index of LP
        sequence_list: list[list[int]] = [] # [start index, end index] of valid sequence

        for idx, char in enumerate(s):
            if char == '(':
                stack.append(idx)
            else: # char is ')'
                if stack:
                    i = stack.pop()
                    sequence_list.append([i, idx])

                    while len(sequence_list)>=2:
                        top1 = sequence_list[-1]
                        top2 = sequence_list[-2]

                        if top2[1] == top1[0]-1: # concatenate two sequences top2[0] ... top2[1], top1[0] ... top1[1]
                            top2[1] = top1[1]
                            sequence_list.pop()
                        elif top1[0] == top2[0]-1 and top2[1]==top1[1]-1: # top1[0], top2[0] .... top2[1], top1[1]
                            top2[0] = top1[0]
                            top2[1] = top1[1]
                            sequence_list.pop()
                        else:
                            break
                    longest = max(longest, sequence_list[-1][1]-sequence_list[-1][0]+1)        
                else: # unmatched ')'
                    sequence_list.clear()
            if DEBUG:
                print(f"longest={longest} stack={stack} sequence_list={sequence_list}")        

        return longest

# "( ) ( ( )"    
# "( ) ( ( ) )"

# ()(())       expected 6
# (()))()(()   expected ?
if __name__ == "__main__":
    DEBUG = True
    
    sol = Solution()
    s = "()(())"

    print(f"TEST s={s}\n")
    answer = sol.longestValidParentheses(s)
    print(f"\nANSWER={answer}\n\n")

    s = "(()))()(()"

    print(f"TEST s={s}\n")
    answer = sol.longestValidParentheses(s)
    print(f"\nANSWER={answer}\n\n")
