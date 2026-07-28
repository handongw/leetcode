# A parentheses string is a non-empty string consisting only of '(' and ')'. It is valid if any of the following conditions is true:

#     It is ().
#     It can be written as AB (A concatenated with B), where A and B are valid parentheses strings.
#     It can be written as (A), where A is a valid parentheses string.

# You are given a parentheses string s and a string locked, both of length n. locked is a binary string consisting only of '0's and '1's. For each index i of locked,

#     If locked[i] is '1', you cannot change s[i].
#     But if locked[i] is '0', you can change s[i] to either '(' or ')'.

# Return true if you can make s a valid parentheses string. Otherwise, return false.

# Constraints:

#     n == s.length == locked.length
#     1 <= n <= 105
#     s[i] is either '(' or ')'.
#     locked[i] is either '0' or '1'.
DEBUG = False

class Solution:
    def canBeValid(self, s: str, locked: str) -> bool:
        if len(s) % 2 != 0:
            return False

        stack = []
        freeCnt = 0
        leftParentheseCnt = 0
        rightParentheseCnt = 0

        # faster version
        for i, c in enumerate(s):
            fixed = locked[i] == '1'

            if fixed:
                if c == "(":
                    leftParentheseCnt += 1
                    stack.append((c, fixed, freeCnt, leftParentheseCnt, rightParentheseCnt))
                else: # c is fixed ')' need to match it
                    rightParentheseCnt += 1
                    if freeCnt+leftParentheseCnt < rightParentheseCnt:
                        return False
                    # stack.append((c, fixed, freeCnt, leftParentheseCnt, rightParentheseCnt))

                    
            else: # unlocked char
                freeCnt += 1

        # scan stack for fixed '('
        while len(stack)>0:
            c1, fixed1, freeCnt1, leftParentheseCnt1, rightParentheseCnt1 = stack.pop()
            if c1 == '(' and fixed1:
                freeCnt2 = freeCnt - freeCnt1
                leftParentheseCnt2 = leftParentheseCnt-leftParentheseCnt1+1
                rightParentheseCnt2 = rightParentheseCnt-rightParentheseCnt1

                if freeCnt2 + rightParentheseCnt2 < leftParentheseCnt2:
                    return False

        return True            



if __name__ == '__main__':
    import sys
    import time

    DEBUG = False
    selected_tests = None  # None: run all; else set of 1-based indices from argv

    for a in sys.argv[1:]:
        if a == "-d":
            DEBUG = True
        elif a.replace(",", "").isdigit() and "," in a:
            if selected_tests is None:
                selected_tests = set()
            for part in a.split(","):
                part = part.strip()
                if part.isdigit():
                    selected_tests.add(int(part))
        elif a.isdigit():
            if selected_tests is None:
                selected_tests = set()
            selected_tests.add(int(a))
        else:
            print(
                f"Unknown argument: {a!r} (use -d and/or 1-based test indices, e.g. 1 2 4)",
                file=sys.stderr,
            )
            sys.exit(2)

    if selected_tests is not None and len(selected_tests) == 0:
        print("Test selection is empty.", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"selected_tests={selected_tests}")

    tests = [
        {"n": 1, "s": "))()))", "locked": "010100", "expected": True},
        {"n": 2, "s": "()()", "locked": "0000", "expected": True},
        {"n": 3, "s": ")", "locked": "0", "expected": False},
        {"n": 4, "s": "(((())(((())", "locked": "111111010111", "expected": True},
        # odd length
        {"n": 5, "s": "(", "locked": "0", "expected": False},
        {"n": 6, "s": "(", "locked": "1", "expected": False},
        {"n": 7, "s": ")))))))", "locked": "0000000", "expected": False},
        # length-2 boundaries
        {"n": 8, "s": "()", "locked": "11", "expected": True},
        {"n": 9, "s": ")(", "locked": "11", "expected": False},
        {"n": 10, "s": ")(", "locked": "00", "expected": True},
        {"n": 11, "s": ")(", "locked": "10", "expected": False},  # locked ')' at start
        {"n": 12, "s": ")(", "locked": "01", "expected": False},  # locked '(' at end
        {"n": 13, "s": "((", "locked": "00", "expected": True},
        {"n": 14, "s": "))", "locked": "00", "expected": True},
        {"n": 15, "s": "((", "locked": "11", "expected": False},
        {"n": 16, "s": "))", "locked": "11", "expected": False},
        {"n": 17, "s": "))", "locked": "01", "expected": True},   # free then locked ')'
        {"n": 18, "s": "))", "locked": "10", "expected": False},  # locked ')' then free
        {"n": 19, "s": "((", "locked": "10", "expected": True},   # locked '(' then free
        {"n": 20, "s": "((", "locked": "01", "expected": False},  # free then locked '('
        # all locked valid / invalid
        {"n": 21, "s": "((()))", "locked": "111111", "expected": True},
        {"n": 22, "s": "()()", "locked": "1111", "expected": True},
        {"n": 23, "s": "(((())", "locked": "111111", "expected": False},
        {"n": 24, "s": "()))))", "locked": "111111", "expected": False},
        {"n": 25, "s": "())(()", "locked": "111111", "expected": False},
        # unlocked must supply enough opposite brackets
        {"n": 26, "s": "((((((", "locked": "111000", "expected": True},
        {"n": 27, "s": "((((((", "locked": "111100", "expected": False},
        {"n": 28, "s": "()))))", "locked": "000111", "expected": True},
        {"n": 29, "s": "()))))", "locked": "001111", "expected": False},
        # locked closes early / locked opens late
        {"n": 30, "s": "))((", "locked": "1100", "expected": False},
        {"n": 31, "s": "))((", "locked": "0011", "expected": False},
        {"n": 32, "s": "))((", "locked": "0000", "expected": True},
        {"n": 33, "s": ")(()))", "locked": "100000", "expected": False},
        {"n": 34, "s": "(((()(", "locked": "000001", "expected": False},
        # all unlocked even length is always True
        {"n": 35, "s": "))))))))", "locked": "00000000", "expected": True},
        {"n": 36, "s": ")()(", "locked": "0000", "expected": True},
        {"n": 37, "s": ")()(", "locked": "1010", "expected": False},
        {"n": 38, "s": ")()(", "locked": "0101", "expected": False},
        {"n": 39, "s": "())(()(()(())()())(())((())(()())((())))))(((((((())(()))))(", 
           "locked": "100011110110011011010111100111011101111110000101001101001111", "expected": False},
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        s = test["s"]
        locked = test["locked"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} s={s!r} locked={locked!r}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.canBeValid(s, locked)
            if result != expected:
                print(f"test {test['n']} FAIL")
                print(f"  got:      {result}")
                print(f"  expected: {expected}")
            else:
                print(f"test {test['n']} OK: (result={result})")
        except Exception as e:
            print(f"test {test['n']} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")
