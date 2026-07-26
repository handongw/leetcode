# There are n cars on an infinitely long road. The cars are numbered from 0 to n - 1 from left to right and each car is present at a unique point.

# You are given a 0-indexed string directions of length n. directions[i] can be either 'L', 'R', or 'S' denoting whether the ith car is moving towards the left, towards the right, or staying at its current point respectively. Each moving car has the same speed.

# The number of collisions can be calculated as follows:

# When two cars moving in opposite directions collide with each other, the number of collisions increases by 2.
# When a moving car collides with a stationary car, the number of collisions increases by 1.
# After a collision, the cars involved can no longer move and will stay at the point where they collided. Other than that, cars cannot change their state or direction of motion.

# Return the total number of collisions that will happen on the road.

# Constraints:

# 1 <= directions.length <= 105
# directions[i] is either 'L', 'R', or 'S'.

# from collections import deque

class Solution:
    def countCollisions(self, directions: str) -> int:
        history=[]
        answer = 0


        # more optimized implementation
        i = 0
        
        while i < len(directions):
            c = directions[i]
            i += 1
            peek = history[-1] if history else None

            # handle empty history first
            if peek is None and c != 'L':
                history.append(c)
                continue

            if c == 'L': 
                if peek == 'S':  # S <--
                    answer += 1
                    # keep history unchanged
                elif peek == 'R':  # --> <--
                    answer += 2
                    history.pop()

                    # peek and c collide and produce S
                    while history and history[-1] == 'R':
                        answer += 1
                        history.pop()
                    history.append('S')    

                elif peek == 'L': #  <-- <-- wont happen
                    history.pop()

            elif c == 'R': 
                if peek == 'S': # S -->
                    history[-1] = 'R'
                elif peek == 'R': # --> -->
                    history.append('R')
                elif peek == 'L': # <-- -->  wont happen
                    history.pop()
                    history.append('R')
            else: # c is S
                if peek == 'S': # S S
                    pass
                elif peek == 'R': # --> S
                    answer += 1
                    history.pop()

                    # peek and c collide and produce S
                    while history and history[-1] == 'R':
                        answer += 1
                        history.pop()
                    history.append('S')    
                elif peek == 'L': # <-- S  wont happen
                    history.pop()
                    history.append('S')

        return answer


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
        {"n": 1, "directions": "RLRSLL", "expected": 5},
        {"n": 2, "directions": "LLRR", "expected": 0},
        {"n": 3, "directions": "RLRSLL", "expected": 5},
        {"n": 4, "directions": "RRRLS", "expected": 4},
        {"n": 5, "directions": "SLLLSSSRRRL", "expected": 7},
        {"n": 6, "directions": "RLRSLL", "expected": 5},
        {"n": 7, "directions": "SRRLRLRSRLRSSRRLSLRLLRSLSLLSSRRLSRSLSLRRS", "expected": 28},
    ]

    solution = Solution()
    t1 = int(time.time() * 1000)

    for test in tests:
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        directions = test["directions"]
        expected = test["expected"]

        try:
            print(f"\nTEST {test['n']} directions={directions!r}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.countCollisions(directions)
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
 