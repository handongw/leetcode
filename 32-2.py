class Solution:
    def longestValidParentheses(self, s: str) -> int:
        # Initialize stack with -1 to act as a base boundary for valid sequences
        stack = [-1]
        longest = 0
        
        for i, char in enumerate(s):
            if char == '(':
                stack.append(i)
            else:
                # pop valid sequence first to leave 'invalid' or 'unmatched' chars  in stack, which marks boundary of valid sequences 
                stack.pop() # Match the '('
                
                if not stack:
                    # If stack is empty, this ')' is unmatched. 
                    # It becomes the new base boundary.
                    stack.append(i)
                else:
                    # The current valid length is RP index - index of exposed 'invalid' boundary 
                    longest = max(longest, i - stack[-1])
                    
        return longest

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
    