# Given a string s, rearrange the characters of s so that any two adjacent characters are not the same.
# Return any possible rearrangement of s or return "" if not possible.
# Constraints:

# 1 <= s.length <= 500
# s consists of lowercase English letters.



import heapq
DEBUG = False

class Solution:
    def reorganizeString(self, s: str) -> str:
        histogram = {}
        for c in s:
            histogram.setdefault(c, 0)
            histogram[c] += 1

        if DEBUG:
            print(f"histogram={histogram}")    

        histoArray = [ (-histogram[c], c)  for c in histogram.keys()]
        heapq.heapify(histoArray)  # pick up the largest histo

        result = [None] * len(s)  # None means the slot is not touched yet
        gapPtr = 0
        endPtr = 0

        while histoArray:
            cnt, c = heapq.heappop(histoArray) # handle longest identical char list
            cnt = -cnt
            if DEBUG:
                print(f"    start cnt,c={(cnt, c)}  gapPtr={gapPtr} endPtr={endPtr} histoArray={histoArray}")

            mode = 'append'  #no gaps to fill. append new identical char list
            while gapPtr < endPtr:
                if result[gapPtr] == '*':
                    mode = 'gap'  # need to fill gaps first
                    break;
                else:
                    gapPtr += 1
            if DEBUG:
                print(f"        mode={mode} gapPtr={gapPtr} endPtr={endPtr}")        

            if mode == 'gap':  # lets fill the gap of current gaps first
                # while cnt > 0 and gapPtr < endPtr:
                result[gapPtr] = c
                cnt -= 1
                gapPtr += 2
                if DEBUG:
                    print(f"        end of gap mode. cnt={cnt}")    
                if cnt > 0:
                    heapq.heappush(histoArray, (-cnt, c)) # push left over chars back to heap to be used later on
            else: # mode == append
                for i in range(cnt):
                    if endPtr >= len(s):
                        return ''

                    result[endPtr] = c
                    if i < cnt-1:
                        if endPtr+1 >= len(s):
                            return ''

                        result[endPtr+1] = '*' # mark it as in between vacant slot
                        endPtr += 2
                    else:
                        endPtr += 1

                    # gapPtr is not updated - it will catch up at begin of next iteration over histoArray    
            if DEBUG:
                print(f"    end cnt,c={(cnt, c)}  gapPtr={gapPtr} endPtr={endPtr} histoArray={histoArray}")

        return ''.join(result)

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
        {"n": 1, "s": "aab", "expected": "aba"},
        {"n": 2, "s": "aaab", "expected": ""},
        {"n": 3, "s": "a", "expected": "a"},  # single char
        {"n": 4, "s": "aa", "expected": ""},  # two identical — impossible
        {"n": 5, "s": "aabb", "expected": "abab"},  # equal freqs, must alternate
        {"n": 6, "s": "aabbcc", "expected": "abacbc"},  
        {"n": 7, "s": "aaabbbccc", "expected": "abacacbcb"},  
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
            result = solution.reorganizeString(s)
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
