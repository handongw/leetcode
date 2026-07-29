# Given a string s of '(' , ')' and lowercase English characters.

# Your task is to remove the minimum number of parentheses ( '(' or ')', in any positions )
# so that the resulting parentheses string is valid and return any valid string.

# Formally, a parentheses string is valid if and only if:
# - It is the empty string, contains only lowercase characters, or
# - It can be written as AB (A concatenated with B), where A and B are valid strings, or
# - It can be written as (A), where A is a valid string.


class Solution:
    def minRemoveToMakeValid(self, s: str) -> str:

        stack = []
        discard = []
        for i, c in enumerate(s):
            if c == ')':
                if not stack:
                    discard.append(i)
                else: 
                    stack.pop()
            elif c == '(': # c is '('
                stack.append(i)
            else:
                pass # ignore Engish letter


        # for i in stack:
        #     discard.append(i)

        chars = list(s)
        for i in discard:
            chars[i] = ''
        for i in stack:
            chars[i] = ''
        return ''.join(chars)


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
        # Example 1: "lee(t(co)de)" and "lee(t(c)ode)" also accepted
        {"n": 1, "s": "lee(t(c)o)de)", "expected": "lee(t(c)o)de"},
        {"n": 2, "s": "a)b(c)d", "expected": "ab(c)d"},
        {"n": 3, "s": "))((", "expected": ""},
        # corner cases
        {"n": 4, "s": "", "expected": ""},  # empty
        {"n": 5, "s": "abc", "expected": "abc"},  # no parens
        {"n": 6, "s": "(", "expected": ""},  # lone open
        {"n": 7, "s": ")", "expected": ""},  # lone close
        {"n": 8, "s": "()", "expected": "()"},  # already valid
        {"n": 9, "s": "(())", "expected": "(())"},  # nested valid
        {"n": 10, "s": "(()", "expected": "()"},  # one extra open
        {"n": 11, "s": "())", "expected": "()"},  # one extra close
        {"n": 12, "s": ")(", "expected": ""},  # crossed pair
        {"n": 13, "s": "(((((((", "expected": ""},  # all opens
        {"n": 14, "s": ")))))))", "expected": ""},  # all closes
        {"n": 15, "s": ")a(", "expected": "a"},  # letters with junk wraps
        {"n": 16, "s": "(a(b(c)d)", "expected": "a(b(c)d)"},  # unmatched outer open
        {"n": 17, "s": "(a)b(c", "expected": "(a)bc"},  # trailing unmatched open
        {"n": 18, "s": "))a((b)c(", "expected": "a(b)c"},  # leading closes + trailing open
        {"n": 19, "s": "())(()", "expected": "()()"},  # middle junk close + leftover open
        {"n": 20, "s": "a)b)c)d)e(", "expected": "abcde"},  # many stray closes, one open
        {"n": 21, "s": "((((a))))", "expected": "((((a))))"},  # deep nest already valid
        {"n": 22, "s": "((((a)))", "expected": "(((a)))"},  # deep nest, one extra open
        {"n": 23, "s": "((a))))", "expected": "((a))"},  # deep nest, extra closes
        {"n": 24, "s": ")()()(", "expected": "()()"},  # bookend junk
        {"n": 25, "s": "x(y)z", "expected": "x(y)z"},  # letters outside valid pair
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        s = test["s"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} s={s!r}")
            if DEBUG:
                print(f"  expected={expected!r}")
            result = solution.minRemoveToMakeValid(s)
            if result != expected:
                print(f"test {test['n']} FAIL")
                print(f"  got:      {result!r}")
                print(f"  expected: {expected!r}")
            else:
                print(f"test {test['n']} OK: (result={result!r})")
        except Exception as e:
            print(f"test {test['n']} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")
