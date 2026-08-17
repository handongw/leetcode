# Constraints:

# 1 <= s.length <= 3 * 105
# s consists of digits, '+', '-', '(', ')', and ' '.
# s represents a valid expression.
# '+' is not used as a unary operation (i.e., "+1" and "+(2 + 3)" is invalid).
# '-' could be used as a unary operation (i.e., "-1" and "-(2 + 3)" is valid).
# There will be no two consecutive operators in the input.
# Every number and running calculation will fit in a signed 32-bit integer.

DEBUG = False

class Solution:
    def calculate(self, s: str) -> int:

        # a basic tokenizer/lexer
        lexer_state = 'start'
        token = ''
        tokens = []
    
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

        token_idx = 0
        def peek_token():
            if token_idx >= len(tokens):
                return '$'
            else:                
                return tokens[token_idx]

        def next_token():
            nonlocal token_idx

            if token_idx<len(tokens):
                t = tokens[token_idx]    
                if DEBUG:
                    print(f"        get tokens[{token_idx}]={t}")
                token_idx += 1
                return t
            else:
                if DEBUG:
                    print(f"        get tokens[{token_idx}]=$")
                return '$'    

        def expr():
            v = term_expr()
            # return v

            if peek_token() == '+' or peek_token()=='-':
                return additive_expr(v)
            else:
                return v

        def parenthesis_expr():
            next_token() # consume '('
            v = expr()
            next_token() # consume ')'
            if DEBUG:
                print(f"    parenthesis ({v})")
            return v

        def additive_expr(v1):
            op = next_token()
            if DEBUG:
                print(f"    {v1} {op} ?s")
            v2 = term_expr()
            if op == '+':
                v = v1 + v2
            else:
                v = v1 - v2

            if DEBUG:
                print(f"    {v1} {op} {v2} = {v}") 

            t = peek_token()
            if t == '+' or t =='-':
                return additive_expr(v)
            else:
                return v            
            

        def term_expr():
            t = peek_token()
            if DEBUG:
                print(f"    term peek {t}")
            if t == '(':
                v = parenthesis_expr()
            elif isinstance(t, int):
                v = next_token()
            elif t == '-':
                v = negate_expr()
            if DEBUG:
                print(f"    term {v}")
            return v    

        def negate_expr():
            next_token() # consume '-'
            v = term_expr()
            if DEBUG:
                print(f"    negate v={v}")
            return -v

        return expr()

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
