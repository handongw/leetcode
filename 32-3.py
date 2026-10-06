DEBUG = False

# TC O(n) SC O(1) solution
class Solution:
    def longestValidParentheses(self, s: str) -> int:
        n = len(s)
        longest = 0

        def scan_right_to_left(lo, hi): # s[lo] ... s[hi] inclusive
            if DEBUG:
                print(f"scan right to left [{lo}, {hi}]={s[lo:hi+1]}")
            nonlocal longest
            seq_end = hi
            lp_count = 0
            rp_count = 0
            k = hi
            while k>=lo:
                c = s[k]
                if c == ')':
                    rp_count += 1
                    k -= 1
                else:
                    lp_count += 1
                    if lp_count > rp_count: # encounter illegal LP char
                        longest = max(longest, seq_end-k)
                        # discard consecutive illegal LP chars
                        j = k
                        while j>=lo and s[j] == '(':
                            j -= 1

                        k = j
                        seq_end = j
                        lp_count = rp_count # restore balance of LP and RP chars
                    else:
                        k -= 1
            if seq_end >= lo:
                longest = max(longest, seq_end-lo+1)            

        
        i = 0
        # find first LP, i.e. skip preceeding RP chars
        while i<n and s[i] == ')':
            i += 1

        lp_count = 0
        rp_count = 0
        seq_start = i
        while i<n:
            char = s[i]
            if char == '(':
                lp_count += 1
                i += 1
            else:
                rp_count += 1
                if rp_count > lp_count: # encounter illegal RP char
                    scan_right_to_left(seq_start, i-1)
                    # discard illegal RPs
                    j=i
                    while j<n and s[j]==')':
                        j += 1

                    i = j    
                    seq_start = j
                    rp_count = lp_count
                else:
                    i += 1    

        if seq_start<n: # remaining chunk
            scan_right_to_left(seq_start, n-1)
                    
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
    