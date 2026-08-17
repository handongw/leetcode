# Constraints:

# 1 <= s.length <= 3 * 105
# s consists of digits, '+', '-', '(', ')', and ' '.
# s represents a valid expression.
# '+' is not used as a unary operation (i.e., "+1" and "+(2 + 3)" is invalid).
# '-' could be used as a unary operation (i.e., "-1" and "-(2 + 3)" is valid).
# There will be no two consecutive operators in the input.
# Every number and running calculation will fit in a signed 32-bit integer.

from collections import deque


DEBUG = False

class Solution:
    def calculate(self, s: str) -> int:

        # a basic tokenizer/lexer
        lexer_state = 'start'
        token = ''
        tokens = deque()
    
        i = 0
        while i < len(s):
            c = s[i]
            if lexer_state == 'start':
                if c == ' ':
                    i += 1
                    continue

                token = ''

                if c == '(' or c == ')' or c == '+' or c == '-':
                    tokens.append(c)
                    i += 1
                elif c.isdigit():
                    token = token + c
                    lexer_state = 'number'
                    i += 1
            elif lexer_state == 'number':
                if c.isdigit():
                    token = token + c
                    i += 1
                else:
                    tokens.append(int(token))
                    lexer_state = 'start'
            else:
                raise Exception(f"invalid lexer_state={lexer_state}")

        if lexer_state == 'number' and token:
            tokens.append(int(token))

        if DEBUG:
            print(f"   tokens={tokens}") 

        stack = []
        stack.append('$')
        while tokens:
            t = tokens.popleft()
            if t == '(':
                stack.append(t)
            elif isinstance(t, int):
                if stack[-1] == '+' or stack[-1] == '-':
                    op = stack.pop()
                    v1 = stack.pop()
                    if op == '+':
                        stack.append(v1 + t)
                    else:
                        stack.append(v1 - t)    
                elif stack[-1] == 'N': # negate
                    stack.pop()
                    tokens.appendleft(-t) # in case: --3
                else:
                    stack.append(t)    

            elif t == '+':
                stack.append('+')
            elif t == '-':
                if isinstance(stack[-1], int):
                    stack.append(t)
                else:
                    stack.append('N')    
            elif t == ')':
                v = stack.pop()
                stack.pop() # pop '('
                tokens.appendleft(v) # put the new value back to head of tokens

        return stack[-1]

if __name__ == '__main__':
    sol = Solution()

    s = '14'
    output = sol.calculate(s) 
    expected = 14
    print(f"expr={s} output={output} expected={expected} {'PASS' if output==expected else 'FAIL'}  \n\n")

    s = '-14'
    output = sol.calculate(s) 
    expected = -14
    print(f"expr={s} output={output} expected={expected} {'PASS' if output==expected else 'FAIL'}  \n\n")


    s = '1+1'
    output = sol.calculate(s) 
    expected = 2
    print(f"expr={s} output={output} expected={expected} {'PASS' if output==expected else 'FAIL'}  \n\n")

    s = ' 2-1 + 2 '
    output = sol.calculate(s) 
    expected = 3
    print(f"expr={s} output={output} expected={expected} {'PASS' if output==expected else 'FAIL'}  \n\n")

    s = '(1+(4+5+2)-3)+(6+8)'
    output = sol.calculate(s) 
    expected = 23
    print(f"expr={s} output={output} expected={expected} {'PASS' if output==expected else 'FAIL'}  \n\n")

    s = '(7)-(0)+(4)'
    output = sol.calculate(s) 
    expected = 11
    print(f"expr={s} output={output} expected={expected} {'PASS' if output==expected else 'FAIL'}  \n\n")
